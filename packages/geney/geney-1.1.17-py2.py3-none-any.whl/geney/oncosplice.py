from Bio.Seq import Seq
from Bio import pairwise2
from dataclasses import dataclass
from copy import deepcopy
import re
import pandas as pd
from pathlib import Path
import numpy as np
from geney import config_setup
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from collections import namedtuple


from geney.utils import find_files_by_gene_name, reverse_complement, unload_pickle, contains, unload_json, dump_json #, is_monotonic
from geney.Fasta_segment import Fasta_segment

#### SpliceAI Modules
import tensorflow as tf
from keras.models import load_model
from pkg_resources import resource_filename
from spliceai.utils import one_hot_encode

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

sai_paths = ('models/spliceai{}.h5'.format(x) for x in range(1, 6))
sai_models = [load_model(resource_filename('spliceai', x)) for x in sai_paths]

def is_monotonic(A):
    x, y = [], []
    x.extend(A)
    y.extend(A)
    x.sort()
    y.sort(reverse=True)
    if (x == A or y == A):
        return True
    return False

def sai_predict_probs(seq: str, models: list) -> list:
    '''
    Predicts the donor and acceptor junction probability of each
    NT in seq using SpliceAI.

    Let m:=2*sai_mrg_context + L be the input seq length. It is assumed
    that the input seq has the following structure:

          seq = |<sai_mrg_context NTs><L NTs><sai_mrg_context NTs>|

    The returned probability matrix is of size 2XL, where
    the first row is the acceptor probability and the second row
    is the donor probability. These probabilities corresponds to the
    middel <L NTs> NTs of the input seq.
    '''
    x = one_hot_encode(seq)[None, :]
    y = np.mean([models[m].predict(x, verbose=0) for m in range(5)], axis=0)
    return y[0, :, 1:].T


### Variant Modules
class Mutation:
    def __init__(self, mid):
        '''

        :param mid: mutation id in the format of gene:chrom:pos:ref:alt
        Needs only to store the following properties for a given mutation
        gene: the name of the gene
        chrom: the chromosome refernece
        start: the position of the mutation
        file_identifier: some filename that can be used to store related data
        vartype: the variant type

        We want to be able to compare mutations based on location.
        '''

        self.mut_id = mid

        gene, chrom, pos, ref, alt = mid.split(':')
        self.gene = gene
        self.chrom = chrom.strip('chr')
        self.start = int(pos)

        self.file_identifier = self.mut_id.replace(':', '_')
        self.file_identifier_short = f'{self.start}_{ref[:6]}_{alt[:6]}'

        self.ref = ref if ref != '-' else ''
        self.alt = alt if alt != '-' else ''

        if len(self.ref) == len(self.alt) == 1:
            self.vartype = 'SNP'

        elif len(self.ref) == len(self.alt) > 1:
            self.vartype = 'SUB'
        elif self.ref and not self.alt:
            self.vartype = 'DEL'
        elif self.alt and not self.ref:
            self.vartype = 'INS'
        else:
            self.vartype = 'INDEL'

    def __str__(self):
        return self.mut_id

    def __repr__(self):
        return f"Mutation({self.mut_id})"

    def __lt__(self, other):
        return self.start < other.start

class Variations:
    '''
    Unlike a mutation, here we have an epistatic set, or a series of mtuations that are separated by '|' characters
    For such events we want to store them
    '''
    def __init__(self, epistatic_set):
        self.variants = sorted([Mutation(m) for m in epistatic_set.split('|')])
        self.mut_id = epistatic_set
        self.start = self.variants[0].start
        self.positions = [v.start for v in self.variants]
        self.gene = self.variants[0].gene
        self.chrom = self.variants[0].chrom.strip('chr')
        self.file_identifier = f'{self.gene}_{self.chrom}' + '_' + '_'.join(
            [v.file_identifier_short for v in self.variants])
        self.range = max(self.positions) - min(self.positions)

    def __str__(self):
        return '|'.join([m.mut_id for m in self.variants])

    def __repr__(self):
        return f"Variation({', '.join([m.mut_id for m in self.variants])})"

    def __iter__(self):
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_index < len(self.variants):
            x = self.variants[self.current_index]
            self.current_index += 1
            return x
        raise StopIteration

    @property
    def file_identifier_json(self):
        return Path(self.file_identifier + '.json')

    @property
    def as_dict(self):
        return {m.start: m.alt for m in self.variants}

    def verify(self):
        if len(set(self.positions)) != len(self.variants):
            return False
        return True


def generate_mut_variant(seq: str, indices: list, mut: Mutation):
    offset = 1 if not mut.ref else 0
    check_indices = list(range(mut.start, mut.start + len(mut.ref) + offset))
    check1 = all([contains(list(filter((-1).__ne__, indices)), m) for m in check_indices])
    if not check1:
        print(
            f"Mutation {mut} not within transcript bounds: {min(list(filter((-1).__ne__, indices)))} - {max(indices)}.")

        return seq, indices

    rel_start, rel_end = indices.index(mut.start) + offset, indices.index(mut.start) + offset + len(mut.ref)
    acquired_seq = seq[rel_start:rel_end]
    check2 = acquired_seq == mut.ref
    if not check2:
        print(f'Reference allele ({mut.ref}) does not match genome_build allele ({acquired_seq}).')

    if len(mut.ref) == len(mut.alt) > 0:
        temp_indices = list(range(mut.start, mut.start + len(mut.ref)))
    # elif len(mut.ref) > 0 and len(mut.alt) > 0:
    #     temp_indices = [indices[indices.index(mut.start)] + v / 1000 for v in list(range(0, len(mut.alt)))]
    else:
        temp_indices = [indices[indices.index(mut.start)] + v / 1000 for v in list(range(1, len(mut.alt) + 1))]

    new_indices = indices[:rel_start] + temp_indices + indices[rel_end:]
    new_seq = seq[:rel_start] + mut.alt + seq[rel_end:]

    assert len(new_seq) == len(new_indices), f'Error in preserving sequence lengths during variant modification: {mut}, {len(new_seq)}, {len(new_indices)}'
    assert is_monotonic(list(filter((-1).__ne__, new_indices))), f'Modified nucleotide indices are not monotonic.'
    return new_seq, new_indices



class Gene:
    def __init__(self, gene_name, variation=None):
        self.gene_name = gene_name
        self.gene_id = ''
        self.rev = None
        self.chrm = ''
        self.gene_start = 0
        self.gene_end = 0
        self.transcripts = {}
        self.load_from_file(find_files_by_gene_name(gene_name))
        self.variations = variation
        self.primary_tid = None
        tids = [k for k, v in self.transcripts.items() if v['primary_transcript'] and v['transcript_biotype'] == 'protein_coding']
        if tids:
            self.primary_tid = tids[0]
        else:
            self.primary_tid = list(self.transcripts.keys())[0]

    def __repr__(self):
        return f'Gene(gene_name={self.gene_name})'

    def __len__(self):
        return len(self.transcripts)

    def __str__(self):
        return '{gname}, {ntranscripts} transcripts'.format(gname=self.gene_name, ntranscripts=self.__len__())

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __getitem__(self, index):
        return Transcript(list(self.transcripts.values())[index])

    def load_from_file(self, file_name):
        if not file_name.exists():
            raise FileNotFoundError(f"File '{file_name}' not found.")
        self.load_from_dict(dict_data=unload_pickle(file_name))
        return self

    def load_from_dict(self, dict_data=None):
        for k, v in dict_data.items():
            setattr(self, k, v)
        return self

    def transcript(self, tid=None):
        if tid is None:
            tid = self.primary_tid

        if tid not in self.transcripts:
            raise AttributeError(f"Transcript '{tid}' not found in gene '{self.gene_name}'.")
        return Transcript(self.transcripts[tid])

    def run_transcripts(self, primary_transcript=False, protein_coding=False):
        for tid, annotations in self.transcripts.items():
            if primary_transcript and not annotations['primary_transcript']:
                continue
            if protein_coding and annotations['transcript_biotype'] != 'protein_coding':
                continue

            yield Transcript(self.transcripts[tid], variations=self.variations)


class Transcript:
    def __init__(self, d=None, variations=None):
        self.transcript_id = None
        self.transcript_start = None                # transcription
        self.transcript_end = None                  # transcription
        self.transcript_upper = None
        self.transcript_lower = None
        self.transcript_biotype = None              # metadata
        self.acceptors, self.donors = [], []        # splicing
        self.TIS, self.TTS = None, None             # translation
        self.transcript_seq, self.transcript_indices = '', []  # sequence data
        self.rev = None                             # sequence data
        self.chrm = ''                              # sequence data
        self.pre_mrna = ''                          # sequence data
        self.orf = ''                               # sequence data
        self.protein = ''                           # sequence data
        self.log = ''                               # sequence data
        self.primary_transcript = None              # sequence data
        self.cons_available = False                 # metadata
        self.cons_seq = ''
        self.cons_vector = ''
        self.variations = None
        if variations:
            self.variations = Variations(variations)

        if d:
            self.load_from_dict(d)


        if self.transcript_biotype == 'protein_coding' and variations is None:
            self.generate_protein()

        else:
            self.generate_pre_mrna()

        if '*' in self.cons_seq:
            self.cons_seq = self.cons_seq.replace('*', '')
            self.cons_vector = np.array(self.cons_vector[:-1])

        if self.cons_seq == self.protein and len(self.cons_vector) == len(self.cons_seq):
            self.cons_available = True

        if self.cons_available == False:
            self.cons_vector = np.ones(len(self.protein))


    def __repr__(self):
        return 'Transcript(transcript_id={tid})'.format(tid=self.transcript_id)

    def __len__(self):
        return len(self.transcript_seq)

    def __str__(self):
        return 'Transcript {tid}, Transcript Type: ' \
               '{protein_coding}, Primary: {primary}'.format(
            tid=self.transcript_id, protein_coding=self.transcript_biotype.replace('_', ' ').title(),
            primary=self.primary_transcript)

    def __eq__(self, other):
        return self.transcript_seq == other.transcript_seq

    def __contains__(self, subvalue):
        '''
        :param subvalue: the substring to search for in the mature mrna transcript
        :return: wehether or not the substring is seen in the mature transcript or not
        '''
        if isinstance(subvalue, str):
            return subvalue in self.transcript_seq
        elif isinstance(subvalue, int):
            return subvalue in self.transcript_indices
        elif isinstance(subvalue, Variations):
            return any([self.transcript_lower <= p <= self.transcript_upper for p in subvalue.positions])

        else:
            print(
                "Pass an integer to check against the span of the gene's coordinates or a string to check against the "
                "pre-mRNA sequence.")
            return False


    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def load_from_dict(self, data):
        '''
        :param data: data is a dictionary containing the needed data to construct the transcript
        :return: itself
        '''
        for k, v in data.items(): # add a line here that ensure the dictionary key is a valid item
            setattr(self, k, v)

        self.transcript_upper, self.transcript_lower = max(self.transcript_start, self.transcript_end), min(self.transcript_start, self.transcript_end)
        self.__arrange_boundaries()#.generate_mature_mrna(inplace=True)
        return self

    @property
    def exons(self):
        '''
        :return: a list of tuples where the first position is the acceptor and the second position is the donor
        '''
        return list(zip([self.transcript_start] + self.acceptors, self.donors + [self.transcript_end]))

    @property
    def exons_pos(self):
        temp = self.exons
        if self.rev:
            temp = [(b, a) for a, b in temp[::-1]]
        return temp

    @property
    def introns(self):
        '''
        :return:  a list of tuples where each first position is a bondary of the first intron, and the second position is the boundary of the end of the intron
        '''
        return list(zip([v for v in self.donors if v != self.transcript_end],
                        [v for v in self.acceptors if v != self.transcript_start]))

    @property
    def introns_pos(self):
        temp = self.introns
        if self.rev:
            temp = [(b, a) for a, b in temp[::-1]]
        return temp


    def reset_acceptors(self, acceptors):
        '''
        :param acceptors: resetting and then reordering the list of acceptors or donors
        :return: itself
        '''
        self.acceptors = acceptors
        return self

    def reset_donors(self, donors):
        '''
        :param donors: resetting and then reordering the list of acceptors or donors
        :return: itself
        '''
        self.donors = donors
        return self

    def reset_transcription_start(self, pos):
        '''
        :param pos: resetting and then reordering the list of acceptors or donors
        :return: itself
        '''
        self.transcription_start = pos
        return self


    def reset_transcription_end(self, pos):
        '''
        :param pos: resetting and then reordering the list of acceptors or donors
        :return: itself
        '''
        self.transcription_end = pos
        return self

    def organize(self):
        '''
        In the case that transcript boundaries or exon boundaires are changed, this needs to be run to ensure the bluepritns are ordered the the mRNA is reobtained.
        :return:
        '''
        self.__arrange_boundaries().generate_mature_mrna(inplace=True)
        self.transcript_upper, self.transcript_lower = max(self.transcript_start, self.transcript_end), min(self.transcript_start, self.transcript_end)

        # if self.__exon_coverage_flag():
        #     raise ValueError(f"Length of exon coverage does not match transcript length.")
        if self.__exon_intron_matchup_flag():
            raise ValueError(f"Unequal number of acceptors and donors.")
        if self.__exon_intron_order_flag():
            raise ValueError(f"Exons / intron order out of position.")
        if self.__transcript_boundary_flag():
            raise ValueError(f"Transcript boundaries must straddle acceptors and donors.")
        return self

    def __arrange_boundaries(self):
        # self.acceptors.append(self.transcript_start)
        # self.donors.append(self.transcript_end)
        self.acceptors = list(set(self.acceptors))
        self.donors = list(set(self.donors))
        self.acceptors.sort(reverse=self.rev)
        self.donors.sort(reverse=self.rev)
        return self


    def __exon_coverage_flag(self):
        if sum([abs(a - b) + 1 for a, b in self.exons]) != len(self):
            return True
        else:
            return False

    def __exon_intron_matchup_flag(self):
        if len(self.acceptors) != len(self.donors):
            return True
        else:
            return False
    def __exon_intron_order_flag(self):
        for b in self.exons_pos:
            if b[0] > b[1]:
                return True
        else:
            return False
    def __transcript_boundary_flag(self):
        if len(self.acceptors) == 0 and len(self.donors) == 0:
            return False

        if self.transcript_lower > min(self.acceptors + self.donors) or self.transcript_upper < max(self.acceptors + self.donors):
            return True
        else:
            return False


    @property
    def exonic_indices(self):
        return [lst for lsts in [list(range(a, b + 1)) for a, b in self.exons_pos] for lst in lsts]


    # Related to transcript seq generation
    def pull_pre_mrna_pos(self):
        fasta_obj = Fasta_segment()
        return fasta_obj.read_segment_endpoints(config_setup['CHROM_SOURCE'] / f'chr{self.chrm}.fasta',
                                                self.transcript_lower,
                                                self.transcript_upper)

    def generate_pre_mrna_pos(self):
        # *_pos functions do not set values into the object.
        seq, indices = self.pull_pre_mrna_pos()
        if self.variations:
            for mutation in self.variations.variants:
                seq, indices = generate_mut_variant(seq, indices, mut=mutation)
        return seq, indices

    def generate_pre_mrna(self, inplace=True):
        pre_mrna, pre_indices = self.__pos2sense(*self.generate_pre_mrna_pos())
        self.pre_mrna = pre_mrna
        self.pre_indices = pre_indices
        if inplace:
            return self
        return pre_mrna, pre_indices

    def __pos2sense(self, mrna, indices):
        if self.rev:
            mrna = reverse_complement(mrna)
            indices = indices[::-1]
        return mrna, indices

    def __sense2pos(self, mrna, indices):
        if self.rev:
            mrna = reverse_complement(mrna)
            indices = indices[::-1]
        return mrna, indices

    def generate_mature_mrna_pos(self, reset=True):
        if reset:
            pre_seq_pos, pre_indices_pos = self.generate_pre_mrna_pos()
            self.pre_mrna, _ = self.__pos2sense(pre_seq_pos, pre_indices_pos)
        else:
            pre_seq_pos, pre_indices_pos = self.__sense2pos(self.pre_mrna, self.pre_indices)

        mature_mrna_pos, mature_indices_pos = '', []
        for i, j in self.exons_pos:
            rel_start, rel_end = pre_indices_pos.index(i), pre_indices_pos.index(j)
            mature_mrna_pos += pre_seq_pos[rel_start:rel_end + 1]
            mature_indices_pos.extend(pre_indices_pos[rel_start:rel_end + 1])
        return mature_mrna_pos, mature_indices_pos

    def generate_mature_mrna(self, inplace=True):
        if inplace:
            self.transcript_seq, self.transcript_indices = self.__pos2sense(*self.generate_mature_mrna_pos())
            return self
        return self.__pos2sense(*self.generate_mature_mrna_pos())

    def generate_protein(self, inplace=True, reset=True):
        if reset:
            self.generate_mature_mrna()

        if not self.TIS or self.TIS not in self.transcript_indices:
            return ''

        rel_start = self.transcript_indices.index(self.TIS)
        orf = self.transcript_seq[rel_start:]
        first_stop_index = next((i for i in range(0, len(orf) - 2, 3) if orf[i:i + 3] in {"TAG", "TAA", "TGA"}), len(orf)-3)
        while first_stop_index % 3 != 0:
            first_stop_index -= 1

        orf = orf[:first_stop_index + 3]
        protein = str(Seq(orf).translate()).replace('*', '')
        if inplace:
            self.orf = orf
            self.protein = protein
            if self.protein != self.cons_seq:
                self.cons_available = False
            return self
        return protein



## Missplicing construction
def develop_aberrant_splicing(transcript, aberrant_splicing):
    exon_starts = {v: 1 for v in transcript.acceptors}
    exon_starts.update({transcript.transcript_start: 1})
    exon_starts.update({s: v['absolute'] for s, v in aberrant_splicing['missed_acceptors'].items()})
    exon_starts.update({s: v['absolute'] for s, v in aberrant_splicing['discovered_acceptors'].items()})

    exon_ends = {v: 1 for v in transcript.donors}
    exon_ends.update({transcript.transcript_end: 1})
    exon_ends.update({s: v['absolute'] for s, v in aberrant_splicing['missed_donors'].items()})
    exon_ends.update({s: v['absolute'] for s, v in aberrant_splicing['discovered_donors'].items()})

    nodes = [SpliceSite(pos=pos, ss_type=0, prob=prob) for pos, prob in exon_ends.items()] + \
            [SpliceSite(pos=pos, ss_type=1, prob=prob) for pos, prob in exon_starts.items()]

    nodes = [s for s in nodes if s.prob > 0]
    nodes.sort(key=lambda x: x.pos, reverse=transcript.rev)

    G = nx.DiGraph()
    G.add_nodes_from([n.pos for n in nodes])

    for i in range(len(nodes)):
        trailing_prob, in_between = 0, []
        for j in range(i + 1, len(nodes)):
            curr_node, next_node = nodes[i], nodes[j]
            spread = curr_node.ss_type in in_between
            in_between.append(next_node.ss_type)
            if curr_node.ss_type != next_node.ss_type:
                if spread:
                    new_prob = next_node.prob - trailing_prob
                    if new_prob <= 0:
                        break
                    G.add_edge(curr_node.pos, next_node.pos)
                    G.edges[curr_node.pos, next_node.pos]['weight'] = new_prob
                    trailing_prob += next_node.prob
                else:
                    G.add_edge(curr_node.pos, next_node.pos)
                    G.edges[curr_node.pos, next_node.pos]['weight'] = next_node.prob
                    trailing_prob += next_node.prob

    new_paths, prob_sum = {}, 0
    for i, path in enumerate(nx.all_simple_paths(G, transcript.transcript_start, transcript.transcript_end)):
        curr_prob = path_weight_mult(G, path, 'weight')
        prob_sum += curr_prob
        new_paths[i] = {
            'acceptors': sorted([p for p in path if p in exon_starts.keys() and p != transcript.transcript_start],
                                reverse=transcript.rev),
            'donors': sorted([p for p in path if p in exon_ends.keys() and p != transcript.transcript_end],
                             reverse=transcript.rev),
            'path_weight': curr_prob}

    for i, path in enumerate(nx.all_simple_paths(G, transcript.transcript_end, transcript.transcript_start)):
        curr_prob = path_weight_mult(G, path, 'weight')
        prob_sum += curr_prob
        new_paths[i] = {
            'acceptors': sorted([p for p in path if p in exon_starts.keys() and p != transcript.transcript_start],
                                reverse=transcript.rev),
            'donors': sorted([p for p in path if p in exon_ends.keys() and p != transcript.transcript_end],
                             reverse=transcript.rev),
            'path_weight': curr_prob}


    for i, d in new_paths.items():
        d['path_weight'] = round(d['path_weight'] / prob_sum, 3)
    new_paths = {k: v for k, v in new_paths.items() if v['path_weight'] > 0.01}
    return list(new_paths.values())


def path_weight_mult(G, path, weight):
    multigraph = G.is_multigraph()
    cost = 1
    if not nx.is_path(G, path):
        raise nx.NetworkXNoPath("path does not exist")
    for node, nbr in nx.utils.pairwise(path):
        if multigraph:
            cost *= min(v[weight] for v in G[node][nbr].values())
        else:
            cost *= G[node][nbr][weight]
    return cost

@dataclass
class SpliceSite(object):
    pos: int
    ss_type: int
    prob: float

    def __post_init__(self):
        pass

    def __lt__(self, other):
        return self.pos < other.pos

    def __str__(self):
        print(f"({self.ss_type}, {self.pos}, {self.prob})")


# Missplicing Detection
def find_ss_changes(ref_dct, mut_dct, known_splice_sites, threshold=0.5):
    '''
    :param ref_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the reference sequence
    :param mut_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the mutated sequence
    :param known_splice_sites: the indices (by genomic position) that serve as known splice sites
    :param threshold: the threshold for detection (difference between reference and mutated probabilities)
    :return: two dictionaries; discovered_pos is a dictionary containing all the positions that meat the threshold for discovery
            and deleted_pos containing all the positions that meet the threshold for missing and the condition for missing
    '''

    new_dict = {v: mut_dct.get(v, 0) - ref_dct.get(v, 0) for v in
                list(set(list(ref_dct.keys()) + list(mut_dct.keys())))}

    discovered_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct[k]), 3)} for k, v in
                      new_dict.items() if v >= threshold and k not in known_splice_sites}   # if (k not in known_splice_sites and v >= threshold) or (v > 0.45)}

    deleted_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct.get(k, 0)), 3)} for k, v in
                   new_dict.items() if -v >= threshold and k in known_splice_sites}      #if k in known_splice_sites and v <= -threshold}

    return discovered_pos, deleted_pos

def run_spliceai_seq(seq, indices, threshold=0):
    seq = 'N' * 5000 + seq + 'N' * 5000
    ref_seq_probs_temp = sai_predict_probs(seq, sai_models)
    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
    acceptor_indices = {a: b for a, b in list(zip(indices, ref_seq_acceptor_probs)) if b >= threshold}
    donor_indices = {a: b for a, b in list(zip(indices, ref_seq_donor_probs)) if b >= threshold}
    return acceptor_indices, donor_indices


def run_spliceai_transcript(mutations, transcript_data, sai_mrg_context=5000, min_coverage=2500, sai_threshold=0.5):
    positions = mutations.positions
    end_positions = [m.start + len(m.ref) for m in mutations.variants]
    positions.extend(end_positions)

    seq_start_pos = min(positions) - sai_mrg_context - min_coverage
    seq_end_pos = max(positions) + sai_mrg_context + min_coverage

    fasta_obj = Fasta_segment()
    ref_seq, ref_indices = fasta_obj.read_segment_endpoints(
        config_setup['CHROM_SOURCE'] / f'chr{mutations.chrom}.fasta',
        seq_start_pos,
        seq_end_pos)

    transcript_start, transcript_end, rev = transcript_data.transcript_lower, transcript_data.transcript_upper, transcript_data.rev

    # visible_donors = np.intersect1d(transcript_data.donors, ref_indices)
    # visible_acceptors = np.intersect1d(transcript_data.acceptors, ref_indices)

    start_pad = ref_indices.index(transcript_start) if transcript_start in ref_indices else 0
    end_cutoff = ref_indices.index(transcript_end) if transcript_end in ref_indices else len(ref_indices)
    end_pad = len(ref_indices) - end_cutoff
    ref_seq = 'N' * start_pad + ref_seq[start_pad:end_cutoff] + 'N' * end_pad
    ref_indices = [-1] * start_pad + ref_indices[start_pad:end_cutoff] + [-1] * end_pad
    mut_seq, mut_indices = ref_seq, ref_indices

    for mut in mutations:
        mut_seq, mut_indices = generate_mut_variant(seq=mut_seq, indices=mut_indices, mut=mut)

    ref_indices = ref_indices[sai_mrg_context:-sai_mrg_context]
    mut_indices = mut_indices[sai_mrg_context:-sai_mrg_context]
    copy_mut_indices = mut_indices.copy()

    visible_donors = np.intersect1d(transcript_data.donors, ref_indices)
    visible_acceptors = np.intersect1d(transcript_data.acceptors, ref_indices)

    if rev:
        ref_seq = reverse_complement(ref_seq)
        mut_seq = reverse_complement(mut_seq)
        ref_indices = ref_indices[::-1]
        mut_indices = mut_indices[::-1]

    ref_seq_probs_temp = sai_predict_probs(ref_seq, sai_models)
    mut_seq_probs_temp = sai_predict_probs(mut_seq, sai_models)

    ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
    mut_seq_acceptor_probs, mut_seq_donor_probs = mut_seq_probs_temp[0, :], mut_seq_probs_temp[1, :]

    assert len(ref_indices) == len(ref_seq_acceptor_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_acceptor_probs), 'Mut pos not the same'

    iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_acceptor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_acceptor_probs))},
                               visible_acceptors,
                               threshold=sai_threshold)

    assert len(ref_indices) == len(ref_seq_donor_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_donor_probs), 'Mut pos not the same'

    idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_donor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_donor_probs))},
                               visible_donors,
                               threshold=sai_threshold)

    ref_acceptors = {a: b for a, b in list(zip(ref_indices, ref_seq_acceptor_probs))}
    ref_donors = {a: b for a, b in list(zip(ref_indices, ref_seq_donor_probs))}

    lost_acceptors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_acceptors[p]), 3)} for p in visible_acceptors if p not in mut_indices and p not in dap}
    lost_donors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_donors[p]), 3)} for p in visible_donors if p not in mut_indices and p not in ddp}
    dap.update(lost_acceptors)
    ddp.update(lost_donors)

    missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap, 'discovered_donors': idp}
    missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
    return {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in missplicing.items()}


# def run_spliceai(mutations, gene_data, sai_mrg_context=5000, min_coverage=2500, sai_threshold=0.5):
#     positions = mutations.positions
#     seq_start_pos = min(positions) - sai_mrg_context - min_coverage
#     seq_end_pos = max(positions) + sai_mrg_context + min_coverage
#
#     fasta_obj = Fasta_segment()
#     ref_seq, ref_indices = fasta_obj.read_segment_endpoints(
#         config_setup['CHROM_SOURCE'] / f'chr{mutations.chrom}.fasta',
#         seq_start_pos,
#         seq_end_pos)
#
#     gene_start, gene_end, rev = gene_data.gene_start, gene_data.gene_end, gene_data.rev
#
#     mrna_acceptors = sorted(list(set([lst for lsts in
#                                       [mrna.get('acceptors', []) for mrna in gene_data.transcripts.values() if
#                                        mrna['transcript_biotype'] == 'protein_coding'] for lst in lsts])))
#
#     mrna_donors = sorted(list(set([lst for lsts in
#                                    [mrna.get('donors', []) for mrna in gene_data.transcripts.values() if
#                                     mrna['transcript_biotype'] == 'protein_coding'] for lst in lsts])))
#
#     visible_donors = np.intersect1d(mrna_donors, ref_indices)
#     visible_acceptors = np.intersect1d(mrna_acceptors, ref_indices)
#
#     start_pad = ref_indices.index(gene_start) if gene_start in ref_indices else 0
#     end_cutoff = ref_indices.index(gene_end) if gene_end in ref_indices else len(ref_indices)  # - 1
#     end_pad = len(ref_indices) - end_cutoff
#     ref_seq = 'N' * start_pad + ref_seq[start_pad:end_cutoff] + 'N' * end_pad
#     ref_indices = [-1] * start_pad + ref_indices[start_pad:end_cutoff] + [-1] * end_pad
#     mut_seq, mut_indices = ref_seq, ref_indices
#
#     for mut in mutations:
#         mut_seq, mut_indices = generate_mut_variant(seq=mut_seq, indices=mut_indices, mut=mut)
#
#     ref_indices = ref_indices[sai_mrg_context:-sai_mrg_context]
#     mut_indices = mut_indices[sai_mrg_context:-sai_mrg_context]
#
#     copy_mut_indices = mut_indices.copy()
#     if rev:
#         ref_seq = reverse_complement(ref_seq)
#         mut_seq = reverse_complement(mut_seq)
#         ref_indices = ref_indices[::-1]
#         mut_indices = mut_indices[::-1]
#
#     ref_seq_probs_temp = sai_predict_probs(ref_seq, sai_models)
#     mut_seq_probs_temp = sai_predict_probs(mut_seq, sai_models)
#
#     ref_seq_acceptor_probs, ref_seq_donor_probs = ref_seq_probs_temp[0, :], ref_seq_probs_temp[1, :]
#     mut_seq_acceptor_probs, mut_seq_donor_probs = mut_seq_probs_temp[0, :], mut_seq_probs_temp[1, :]
#
#     assert len(ref_indices) == len(ref_seq_acceptor_probs), 'Reference pos not the same'
#     assert len(mut_indices) == len(mut_seq_acceptor_probs), 'Mut pos not the same'
#
#     iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_acceptor_probs))},
#                                {p: v for p, v in list(zip(mut_indices, mut_seq_acceptor_probs))},
#                                visible_acceptors,
#                                threshold=sai_threshold)
#
#     assert len(ref_indices) == len(ref_seq_donor_probs), 'Reference pos not the same'
#     assert len(mut_indices) == len(mut_seq_donor_probs), 'Mut pos not the same'
#
#     idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_donor_probs))},
#                                {p: v for p, v in list(zip(mut_indices, mut_seq_donor_probs))},
#                                visible_donors,
#                                threshold=sai_threshold)
#
#     # lost_acceptors = {p: {'absolute': 0, 'delta': -1} for p in gene_data.acceptors if not contains(copy_mut_indices, p)}
#     # lost_donors = {p: {'absolute': 0, 'delta': -1} for p in gene_data.donors if not contains(copy_mut_indices, p)}
#     # dap.update(lost_acceptors)
#     # ddp.update(lost_donors)
#     missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap, 'discovered_donors': idp}
#     missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
#
#     return {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in missplicing.items()}
#

class PredictSpliceAI:
    def __init__(self, mutation, gene_data,
                threshold=0.5, force=False,  save_results=False, sai_mrg_context=5000, min_coverage=2500):
        self.modification = mutation
        self.threshold = threshold
        self.transcript_id = gene_data.transcript_id
        self.spliceai_db = config_setup['MISSPLICING_PATH'] / f'spliceai_epistatic'
        self.missplicing = {}

        if self.prediction_file_exists() and not force: # need to do a check for the filename length
            self.missplicing = self.load_sai_predictions()

        if not self.missplicing:
        # else:
            # if isinstance(gene_data, Gene):
            #     self.missplicing = run_spliceai(self.modification, gene_data=gene_data, sai_mrg_context=sai_mrg_context, min_coverage=min_coverage, sai_threshold=0.1)
            #     if save_results:
            #         self.save_sai_predictions()
            #
            # elif isinstance(gene_data, Transcript):
            self.missplicing = run_spliceai_transcript(self.modification, transcript_data=gene_data, sai_mrg_context=sai_mrg_context, min_coverage=min_coverage, sai_threshold=0.1)
            if save_results:
                self.save_sai_predictions()


    def __repr__(self):
        return f'Missplicing({self.modification.mut_id}) --> {self.missplicing}'

    def __str__(self):
        return self.aberrant_splicing
    def __bool__(self):
        for event, details in self.aberrant_splicing.items():
            if details:
                return True
        return False

    def __eq__(self, alt_splicing):
        flag, _ = check_splicing_difference(self.missplicing, alt_splicing, self.threshold)
        return not flag

    def __iter__(self):
        penetrances = [abs(d_in['delta']) for d in self.missplicing.values() for d_in in d.values()] + [0]
        return iter(penetrances)

    @property
    def aberrant_splicing(self):
        return self.apply_sai_threshold(self.missplicing, self.threshold)

    @property
    def prediction_file(self):
        return self.spliceai_db / self.modification.gene / self.modification.file_identifier_json

    def prediction_file_exists(self):
        return self.prediction_file.exists()

    def load_sai_predictions(self):
        missplicing = unload_json(self.prediction_file)
        if self.transcript_id in missplicing:
            missplicing = missplicing[self.transcript_id]
        else:
            return {}

        missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
        missplicing = {outk: {int(k) if k.is_integer() or 'missed' in outk else k: v for k, v in outv.items()} for
                       outk, outv in
                       missplicing.items()}
        return missplicing

    def save_sai_predictions(self):
        self.prediction_file.parent.mkdir(parents=True, exist_ok=True)
        if self.prediction_file_exists():
            missplicing = unload_json(self.prediction_file)
            missplicing[self.transcript_id] = self.missplicing

        else:
            missplicing = {self.transcript_id: self.missplicing}

        # print(missplicing)
        dump_json(self.prediction_file, missplicing)

    def apply_sai_threshold(self, splicing_dict=None, threshold=None):
        splicing_dict = self.missplicing if not splicing_dict else splicing_dict
        threshold = self.threshold if not threshold else threshold
        new_dict = {}
        for event, details in splicing_dict.items():
            for e, d in details.items():
                if abs(d['delta']) >= threshold:
                    return splicing_dict
            # new_dict[event] = {}        #{k: v for k, v in details.items() if abs(v['delta']) >= threshold}
        return new_dict


    def apply_sai_threshold_primary(self, splicing_dict=None, threshold=None):
        splicing_dict = self.missplicing if not splicing_dict else splicing_dict
        threshold = self.threshold if not threshold else threshold
        new_dict = {}
        for event, details in splicing_dict.items():
            new_dict_in = {}
            for e, d in details.items():
                if abs(d['delta']) >= threshold:
                    new_dict_in[e] = d
            new_dict[event] = new_dict_in
        return new_dict

    def get_max_missplicing_delta(self):
        max_delta = 0
        for event, details in self.missplicing.items():
            for e, d in details.items():
                if abs(d['delta']) > max_delta:
                    max_delta = abs(d['delta'])
        return max_delta


def check_splicing_difference(missplicing1, missplicing2, threshold=None):
    flag = False
    true_differences = {}
    for event in ['missed_acceptors', 'missed_donors']:
        td = {}
        dct1 = missplicing1[event]
        dct2 = missplicing2[event]
        for k in list(set(list(dct1.keys()) + list(dct2.keys()))):
            diff = abs(dct1.get(k, {'delta': 0})['delta']) - abs(dct2.get(k, {'delta': 0})['delta'])
            if abs(diff) >= threshold:
                flag = True
                td[k] = diff
        true_differences[event] = td

    for event in ['discovered_acceptors', 'discovered_donors']:
        td = {}
        dct1 = missplicing1[event]
        dct2 = missplicing2[event]
        for k in list(set(list(dct1.keys()) + list(dct2.keys()))):
            diff = abs(dct1.get(k, {'delta': 0})['delta']) - abs(dct2.get(k, {'delta': 0})['delta'])
            if abs(diff) >= threshold:
                flag = True
                td[k] = diff
        true_differences[event] = td

    return flag, true_differences


# Annotating
def OncospliceAnnotator(reference_transcript, variant_transcript, mut):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = find_splice_site_proximity(mut,
                                                                                                  reference_transcript)

    report = {}
    report['primary_transcript'] = reference_transcript.primary_transcript
    report['transcript_id'] = reference_transcript.transcript_id
    report['mut_id'] = mut.mut_id
    report['cons_available'] = int(reference_transcript.cons_available)
    report['protein_coding'] = reference_transcript.transcript_biotype

    report['reference_mrna'] = reference_transcript.transcript_seq
    report['reference_cds_start'] = reference_transcript.TIS
    report['reference_pre_mrna'] = reference_transcript.pre_mrna
    report[
        'reference_orf'] = reference_transcript.orf  # pre_mrna[reference_transcript.transcript_indices.index(reference_transcript.TIS):reference_transcript.transcript_indices.index(reference_transcript.TTS)]
    report['reference_protein'] = reference_transcript.protein
    report['reference_protein_length'] = len(reference_transcript.protein)

    report['variant_mrna'] = variant_transcript.transcript_seq
    report['variant_cds_start'] = variant_transcript.TIS
    report[
        'variant_pre_mrna'] = variant_transcript.pre_mrna  # pre_mrna[variant_transcript.transcript_indices.index(variant_transcript.TIS):variant_transcript.transcript_indices.index(variant_transcript.TTS)]
    report['variant_orf'] = variant_transcript.orf
    report['variant_protein'] = variant_transcript.protein
    report['variant_protein_length'] = len(variant_transcript.protein)

    descriptions = define_missplicing_events(reference_transcript, variant_transcript)
    # print(descriptions)
    report['exon_changes'] = '|'.join([v for v in descriptions if v])
    report['splicing_codes'] = summarize_missplicing_event(*descriptions)
    report['affected_exon'] = affected_exon
    report['affected_intron'] = affected_intron
    report['mutation_distance_from_5'] = distance_from_5
    report['mutation_distance_from_3'] = distance_from_3
    return report


def find_splice_site_proximity(mut, transcript):
    for i, (ex_start, ex_end) in enumerate(transcript.exons):
        if min(ex_start, ex_end) <= mut.start <= max(ex_start, ex_end):
            return i + 1, None, abs(mut.start - ex_start), abs(mut.start - ex_end)

    for i, (in_start, in_end) in enumerate(transcript.introns):
        if min(in_start, in_end) <= mut.start <= max(in_start, in_end):
            return None, i + 1, abs(mut.start - in_end), abs(mut.start - in_start)


def define_missplicing_events(ref, var):
    ref_introns, ref_exons = ref.introns, ref.exons
    var_introns, var_exons = var.introns, var.exons

    num_ref_exons = len(ref_exons)
    num_ref_introns = len(ref_introns)

    partial_exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
         exon_count, (t1, t2) in enumerate(ref_exons)
         if (not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)))
         or (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)))])

    partial_intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
         in var_introns for intron_count, (t1, t2) in enumerate(ref_introns)
         if (not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)))
         or (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)))])

    exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}' for exon_count, (t1, t2) in enumerate(ref_exons)
         if t1 not in var.acceptors and t2 not in var.donors])

    novel_exons = ','.join([f'Novel Exon: {(t1, t2)}' for (t1, t2) in var_exons if
                            t1 not in ref.acceptors and t2 not in ref.donors])

    intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}' for intron_count, (t1, t2) in
         enumerate(ref_introns)
         if t1 not in var.donors and t2 not in var.acceptors])

    return partial_exon_skipping, partial_intron_retention, exon_skipping, novel_exons, intron_retention


def summarize_missplicing_event(pes, pir, es, ne, ir):
    event = []
    if pes:
        event.append('PES')
    if es:
        event.append('ES')
    if pir:
        event.append('PIR')
    if ir:
        event.append('IR')
    if ne:
        event.append('NE')
    if len(event) >= 1:
        return ','.join(event)
    # elif len(event) == 1:
    #     return event[0]
    else:
        return '-'


### Scoring
def find_continuous_gaps(sequence):
    """Find continuous gap sequences in an alignment."""
    return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]


def get_logical_alignment(ref_prot, var_prot):
    """
    Aligns two protein sequences and finds the optimal alignment with the least number of gaps.

    Parameters:
    ref_prot (str): Reference protein sequence.
    var_prot (str): Variant protein sequence.

    Returns:
    tuple: Optimal alignment, number of insertions, and number of deletions.
    """

    if var_prot == '':
        print("here")
        var_prot = ref_prot[0]

    # Perform global alignment
    alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, True))
    if len(alignments) == 0:
        print(ref_prot, var_prot)
        print(alignments)

    # Selecting the optimal alignment
    if len(alignments) > 1:
        # Calculate continuous gaps for each alignment and sum their lengths
        gap_lengths = [sum(end - start for start, end in find_continuous_gaps(al.seqA) + find_continuous_gaps(al.seqB))
                       for al in alignments]
        optimal_alignment = alignments[gap_lengths.index(min(gap_lengths))]
    else:
        optimal_alignment = alignments[0]

    return optimal_alignment


def find_indels_with_mismatches_as_deletions(seqA, seqB):
    """
    Identify insertions and deletions in aligned sequences, treating mismatches as deletions.

    Parameters:
    seqA, seqB (str): Aligned sequences.

    Returns:
    tuple: Two dictionaries containing deletions and insertions.
    """
    if len(seqA) != len(seqB):
        raise ValueError("Sequences must be of the same length")

    mapperA, counter = {}, 0
    for i, c in enumerate(list(seqA)):
        if c != '-':
            counter += 1
        mapperA[i] = counter

    mapperB, counter = {}, 0
    for i, (c1, c2) in enumerate(list(zip(seqA, seqB))):
        if c2 != '-':
            counter += 1
        mapperB[i] = counter

    seqA_array, seqB_array = np.array(list(seqA)), np.array(list(seqB))

    # Find and mark mismatch positions in seqB
    mismatches = (seqA_array != seqB_array) & (seqA_array != '-') & (seqB_array != '-')
    seqB_array[mismatches] = '-'
    modified_seqB = ''.join(seqB_array)

    gaps_in_A = find_continuous_gaps(seqA)
    gaps_in_B = find_continuous_gaps(modified_seqB)

    insertions = {mapperB[start]: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
                  seqB[start:end].strip('-')}
    deletions = {mapperA[start]: seqA[start:end].replace('-', '') for start, end in gaps_in_B if
                 seqA[start:end].strip('-')}

    return deletions, insertions


def parabolic_window(window_size):
    """Create a parabolic window function with a peak at the center."""
    x = np.linspace(-1, 1, window_size)
    return 0.9 * (1 - x ** 2) + 0.1


def transform_conservation_vector(conservation_vector, window=13, factor=4):
    """
    Transforms a 1D conservation vector using different parameters.

    Args:
        conservation_vector (numpy.ndarray): Input 1D vector of conservation values.

    Returns:
        numpy.ndarray: A matrix containing transformed vectors.
    """
    # window = 13
    # factor = 4
    convolving_window = parabolic_window(window)
    transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / np.sum(convolving_window)
    assert len(transformed_vector) == len(conservation_vector), f"Len Ref: {len(conservation_vector)}, Len New: {len(transformed_vector)}"
    # Compute exponential factors
    exp_factors = np.exp(-transformed_vector * factor)

    # Normalize and scale exponential factors
    # exp_factors /= exp_factors.sum()
    return exp_factors


# def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
#     """
#     Identify unmodified positions in a sequence given deletions and insertions.
#
#     :param sequence_length: Length of the sequence.
#     :param deletions: Dictionary of deletions.
#     :param insertions: Dictionary of insertions.
#     :param reach_limit: Limit for considering the effect of insertions/deletions.
#     :return: Array indicating unmodified positions.
#     """
#     unmodified_positions = np.zeros(sequence_length, dtype=float)
#
#     for pos, insertion in insertions.items():
#         # if pos >= sequence_length:
#         #     pos = sequence_length - 1
#         #     add_factor = 1
#
#         reach = min(len(insertion) // 2, reach_limit)
#         front_end, back_end = max(0, pos - reach), min(sequence_length - 1, pos + reach)
#         len_start, len_end = pos - front_end, back_end - pos
#         try:
#             gradient_front = np.linspace(0, 1, len_start, endpoint=False)
#             gradient_back = np.linspace(0, 1, len_end, endpoint=True)[::-1]
#             combined_gradient = np.concatenate([gradient_front, np.array([1]), gradient_back])
#             unmodified_positions[front_end:back_end + 1] = combined_gradient
#
#         except ValueError as e:
#             print(
#                 f"Error: {e} | Lengths: unmodified_positions_slice={back_end - front_end}.")
#             unmodified_positions[front_end:back_end] = np.zeros(back_end - front_end)
#
#     for pos, deletion in deletions.items():
#         deletion_length = len(deletion)
#         unmodified_positions[pos:pos + deletion_length] = 1
#
#     return unmodified_positions

def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
    """
    Identify unmodified positions in a sequence given deletions and insertions.

    :param sequence_length: Length of the sequence.
    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param reach_limit: Limit for considering the effect of insertions/deletions.
    :return: Array indicating unmodified positions.
    """
    unmodified_positions = np.zeros(sequence_length, dtype=float)

    for pos, deletion in deletions.items():
        deletion_length = len(deletion)
        unmodified_positions[pos:pos + deletion_length] = 1

    for pos, insertion in insertions.items():
        reach = min(len(insertion) // 2, reach_limit)
        front_end, back_end = max(0, pos - reach), min(sequence_length, pos + reach)
        # len_start, len_end = pos - front_end, back_end - pos + 1
        # gradient_front = np.linspace(0, 1, len_start, endpoint=False)
        # gradient_back = np.linspace(0, 1, len_end, endpoint=True)[::-1]
        # combined_gradient = np.concatenate([gradient_front, gradient_back])  #np.array([1]),
        # print(len(unmodified_positions[front_end:back_end]), len(combined_gradient))
        unmodified_positions[front_end:back_end] = 1 #combined_gradient

    return unmodified_positions


def calculate_penalty(domains, cons_scores, W, is_insertion=False):
    """
    Calculate the penalty for mutations (either insertions or deletions) on conservation scores.

    :param domains: Dictionary of mutations (inserted or deleted domains).
    :param cons_scores: Conservation scores.
    :param W: Window size.
    :param is_insertion: Boolean flag to indicate if the mutation is an insertion.
    :return: Penalty array.
    """
    penalty = np.zeros(len(cons_scores))
    for pos, seq in domains.items():
        mutation_length = len(seq)
        weight = max(1.0, mutation_length / W)

        if is_insertion:
            reach = min(W // 2, mutation_length // 2)
            penalty[pos - reach:pos + reach] = weight * cons_scores[pos - reach:pos + reach]
        else:  # For deletion
            penalty[pos:pos + mutation_length] = cons_scores[pos:pos + mutation_length] * weight

    return penalty


def calculate_legacy_oncosplice_score(deletions, insertions, cons_vec, W):
    """
    Calculate the legacy Oncosplice score based on deletions, insertions, and conservation vector.

    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param cons_vec: Conservation vector.
    :param W: Window size.
    :return: Legacy Oncosplice score.
    """
    smoothed_conservation_vector = np.exp(np.negative(moving_average_conv(cons_vec, W, 2)))
    del_penalty = calculate_penalty(deletions, smoothed_conservation_vector, W, is_insertion=False)
    ins_penalty = calculate_penalty(insertions, smoothed_conservation_vector, W, is_insertion=True)
    combined_scores = del_penalty + ins_penalty
    return np.max(np.convolve(combined_scores, np.ones(W), mode='same'))


def moving_average_conv(vector, window_size, factor=1):
    """
    Calculate the moving average convolution of a vector.

    Parameters:
    vector (iterable): Input vector (list, tuple, numpy array).
    window_size (int): Size of the convolution window. Must be a positive integer.
    factor (float): Scaling factor for the average. Default is 1.

    Returns:
    numpy.ndarray: Convolved vector as a numpy array.
    """
    if not isinstance(vector, (list, tuple, np.ndarray)):
        raise TypeError("vector must be a list, tuple, or numpy array")
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("window_size must be a positive integer")
    if len(vector) < window_size:
        raise ValueError("window_size must not be greater than the length of vector")
    if factor == 0:
        raise ValueError("factor must not be zero")

    return np.convolve(vector, np.ones(window_size), mode='same') / window_size

def oncosplice(mut_id, sai_threshold=0.5, protein_coding=True, primary_transcript=False, per_transcript_missplicing=False, window_length=13, save_spliceai_results=False, force_spliceai=False):
    mutation = Variations(mut_id)
    try:
        reference_gene = Gene(mutation.gene)
    except FileNotFoundError:
        return pd.DataFrame()

    reference_gene_proteines = {g.protein: g.transcript_id for g in reference_gene.run_transcripts()}
    mutated_gene = Gene(mutation.gene, mut_id)
    # if not per_transcript_missplicing:
    #     missplicing_obj = PredictSpliceAI(mutation, reference_gene, threshold=sai_threshold, force=True, save_results=False)
    #     missplicing = missplicing_obj.missplicing

    results = []
    for variant in mutated_gene.run_transcripts(protein_coding=protein_coding, primary_transcript=primary_transcript):
        reference = reference_gene.transcript(variant.transcript_id)
        if mutation not in reference or reference.protein == '' or len(reference.protein) < window_length:
            continue

        cons_vector = transform_conservation_vector(reference.cons_vector, window=window_length)
        # if per_transcript_missplicing:
        missplicing_obj = PredictSpliceAI(mutation, reference, threshold=sai_threshold, force=force_spliceai, save_results=save_spliceai_results)
        missplicing = missplicing_obj.apply_sai_threshold_primary(threshold=sai_threshold)
        # print(missplicing)
        for i, new_boundaries in enumerate(develop_aberrant_splicing(variant, missplicing)):
            variant_isoform = deepcopy(variant)
            variant_isoform.reset_acceptors(acceptors=new_boundaries['acceptors']).reset_donors(donors=new_boundaries['donors']).organize().generate_protein()
            alignment = get_logical_alignment(reference.protein, variant_isoform.protein)
            deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
            modified_positions = find_modified_positions(len(reference.protein), deleted, inserted)
            temp_cons = np.convolve(cons_vector * modified_positions, np.ones(window_length)) / window_length
            affected_cons_scores = max(temp_cons)
            # temp_cons = np.convolve(cons_vector, np.ones(window_length))
            # print(temp_cons)
            # print(cons_vector)
            percentile = (
                        sorted(cons_vector).index(next(x for x in sorted(cons_vector) if x >= affected_cons_scores)) / len(
                    cons_vector))

            report = OncospliceAnnotator(reference, variant_isoform, mutation)
            report['original_cons'] = reference.cons_vector
            report['oncosplice_score'] = affected_cons_scores
            report['percentile'] = percentile
            report['modified_positions'] = modified_positions
            report['cons_vector'] = cons_vector
            report['isoform_id'] = i
            report['isoform_prevalence'] = new_boundaries['path_weight']
            report['full_missplicing'] = missplicing
            report['missplicing'] = max(missplicing_obj)
            report['reference_resemblance'] = reference_gene_proteines.get(variant_isoform.protein, None)
            results.append(report)

    report = pd.DataFrame(results)
    return report



### Graphical Stuff
def create_figure_story(epistasis, to_file=None):
    g = epistasis.split(':')[0]
    out = oncosplice(epistasis, annotate=True)
    out = out[out.cons_available==1]

    for _, row in out.iterrows():
        max_length = 0
        pos = 0
        for i, k in row.deletions.items():
            if len(k) > max_length:
                pos = i
                max_length = len(k)

        if max_length > 5:
            del_reg = [pos, pos + max_length]
        else:
            del_reg = None

        if row.oncosplice_score == 0:
            mutation_loc = None
        else:
            mutation_loc = pos

        plot_conservation(tid=row.transcript_id,
                          gene=f'{g}, {row.transcript_id}.{row.isoform}',
                          mutation_loc=mutation_loc,
                          target_region=del_reg, mut_name='Epistasis',
                          domain_annotations=get_annotations(row.transcript_id, 300),
                          to_file=to_file)



def plot_conservation(gene_name, tid, gene='', mutation_loc=None, target_region=None, mut_name='Mutation', domain_annotations=[]):
    """
    Plots conservation vectors with protein domain visualization and Rate4Site scores.

    Parameters:
    tid (str): Transcript identifier.
    gene (str): Gene name.
    mutation_loc (int): Position of the mutation.
    target_region (tuple): Start and end positions of the target region.
    mut_name (str): Name of the mutation.
    domain_annotations (list): List of tuples for domain annotations (start, end, label).
    """
    # Access conservation data
    _, cons_vec = unload_pickle(gene_name)['tid']['cons_vector']

    if not cons_vec:
        raise ValueError("The conservation vector is empty.")

    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(max(15, len(cons_vec)/10), 3))  # Dynamic figure size

    # Plotting the conservation vectors in the main plot
    plot_conservation_vectors(ax, cons_vec)

    # Setting up primary axis for the main plot
    setup_primary_axis(ax, gene, len(cons_vec))

    # Create a separate axes for protein domain visualization
    domain_ax = create_domain_axes(fig, len(cons_vec))

    # Draw protein domains
    plot_protein_domains(domain_ax, domain_annotations, len(cons_vec))

    # Plotting Rate4Site scores on secondary y-axis
    plot_rate4site_scores(ax, cons_vec)

    # Plotting mutation location and target region, if provided
    plot_mutation_and_target_region(ax, mutation_loc, target_region, mut_name)

    plt.show()

def plot_conservation_vectors(ax, cons_vec):
    """Plots transformed conservation vectors."""
    temp = transform_conservation_vector(cons_vec, 76)  # Larger window
    temp /= max(temp)
    ax.plot(list(range(len(temp))), temp, c='b', label='Estimated Functional Residues')

    temp = transform_conservation_vector(cons_vec, 6)   # Smaller window
    temp /= max(temp)
    ax.plot(list(range(len(temp))), temp, c='k', label='Estimated Functional Domains')

def setup_primary_axis(ax, gene, length):
    """Configures the primary axis of the plot."""
    ax.set_xlabel(f'AA Position - {gene}', weight='bold')
    ax.set_xlim(0, length)
    ax.set_ylim(0, 1)
    ax.set_ylabel('Relative Importance', weight='bold')
    ax.tick_params(axis='y')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def create_domain_axes(fig, length):
    """Creates an axis for protein domain visualization."""
    domain_ax_height = 0.06
    domain_ax = fig.add_axes([0.125, 0.95, 0.775, domain_ax_height])
    domain_ax.set_xlim(0, length)
    domain_ax.set_xticks([])
    domain_ax.set_yticks([])
    for spine in domain_ax.spines.values():
        spine.set_visible(False)
    return domain_ax

def plot_protein_domains(ax, domain_annotations, length):
    """Plots protein domain annotations."""
    ax.add_patch(Rectangle((0, 0), length, 0.9, facecolor='lightgray', edgecolor='none'))
    for domain in domain_annotations:
        start, end, label = domain
        ax.add_patch(Rectangle((start, 0), end - start, 0.9, facecolor='orange', edgecolor='none', alpha=0.5))
        ax.text((start + end) / 2, 2.1, label, ha='center', va='center', color='black', size=8)

def plot_rate4site_scores(ax, cons_vec):
    """Plots Rate4Site scores on a secondary y-axis."""
    ax2 = ax.twinx()
    c = np.array(cons_vec)
    c = c + abs(min(c))
    c = c/max(c)
    ax2.set_ylim(min(c), max(c)*1.1)
    ax2.scatter(list(range(len(c))), c, color='green', label='Rate4Site Scores', alpha=0.4)
    ax2.set_ylabel('Rate4Site Normalized', color='green', weight='bold')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.spines['right'].set_visible(True)
    ax2.spines['top'].set_visible(False)

def plot_mutation_and_target_region(ax, mutation_loc, target_region, mut_name):
    """Highlights mutation location and target region, if provided."""
    if mutation_loc is not None:
        ax.axvline(x=mutation_loc, ymax=1, color='r', linestyle='--', alpha=0.7)
        ax.text(mutation_loc, 1.04, mut_name, color='r', weight='bold', ha='center')

    if target_region is not None:
        ax.add_patch(Rectangle((target_region[0], 0), target_region[1] - target_region[0], 1, alpha=0.25, facecolor='gray'))
        center_loc = target_region[0] + 0.5 * (target_region[1] - target_region[0])
        ax.text(center_loc, 1.04, 'Deleted Region', ha='center', va='center', color='gray', weight='bold')


def merge_overlapping_regions(df):
    """
    Merges overlapping regions in a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'start', 'end', 'name'

    Returns:
    List: List of merged regions as namedtuples (start, end, combined_name)
    """
    if df.empty:
        return []

    Region = namedtuple('Region', ['start', 'end', 'combined_name'])
    df = df.sort_values(by='start')
    merged_regions = []
    current_region = None

    for _, row in df.iterrows():
        start, end, name = row['start'], row['end'], row['name'].replace('_', ' ')
        if current_region is None:
            current_region = Region(start, end, [name])
        elif start <= current_region.end:
            current_region = Region(current_region.start, max(current_region.end, end), current_region.combined_name + [name])
        else:
            merged_regions.append(current_region._replace(combined_name=', '.join(current_region.combined_name)))
            current_region = Region(start, end, [name])

    if current_region:
        merged_regions.append(current_region._replace(combined_name=', '.join(current_region.combined_name)))

    # Assuming split_text is a function that splits the text appropriately.
    merged_regions = [Region(a, b, split_text(c, 35)) for a, b, c in merged_regions]
    return merged_regions


def split_text(text, width):
    """
    Splits a text into lines with a maximum specified width.

    Parameters:
    text (str): The text to be split.
    width (int): Maximum width of each line.

    Returns:
    str: The text split into lines of specified width.
    """
    lines = re.findall('.{1,' + str(width) + '}', text)
    return '\n'.join(lines)

def get_annotations(target_gene, w=500):
    PROTEIN_ANNOTATIONS = {}
    temp = PROTEIN_ANNOTATIONS[(PROTEIN_ANNOTATIONS['Transcript stable ID'] == PROTEIN_ANNOTATIONS[target_gene]) & (PROTEIN_ANNOTATIONS.length < w)].drop_duplicates(subset=['Interpro Short Description'], keep='first')
    return merge_overlapping_regions(temp)


# def plot_conservation(tid, gene='', mutation_loc=None, target_region=None, mut_name='Mutation', domain_annotations=[], to_file=None):
#     _, cons_vec = access_conservation_data(tid)
#
#     sns.set_theme(style="white")
#     fig, ax = plt.subplots(figsize=(15, 3))  # Adjusted figure size for better layout
#
#     # Plotting the conservation vectors in the main plot
#     temp = transform_conservation_vector(cons_vec, 76)
#     temp /= max(temp)
#     ax.plot(list(range(len(temp))), temp, c='b', label='Estimated Functional Residues')
#     temp = transform_conservation_vector(cons_vec, 6)
#     temp /= max(temp)
#     ax.plot(list(range(len(temp))), temp, c='k', label='Estimated Functional Domains')
#
#     # Setting up primary axis for the main plot
#     ax.set_xlabel(f'AA Position - {gene}', weight='bold')
#     ax.set_xlim(0, len(cons_vec))
#     ax.set_ylim(0, 1)  # Set y-limit to end at 1
#     ax.set_ylabel('Relative Importance', weight='bold')
#     ax.tick_params(axis='y')
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#
#     # Create a separate axes for protein domain visualization above the main plot
#     domain_ax_height = 0.06  # Adjust for thinner protein diagram
#     domain_ax = fig.add_axes([0.125, 0.95, 0.775, domain_ax_height])  # Position higher above the main plot
#     domain_ax.set_xlim(0, len(cons_vec))
#     domain_ax.set_xticks([])
#     domain_ax.set_yticks([])
#     domain_ax.spines['top'].set_visible(False)
#     domain_ax.spines['right'].set_visible(False)
#     domain_ax.spines['left'].set_visible(False)
#     domain_ax.spines['bottom'].set_visible(False)
#
#     # Draw the full-length protein as a base rectangle
#     domain_ax.add_patch(Rectangle((0, 0), len(cons_vec), 0.9, facecolor='lightgray', edgecolor='none'))
#
#     # Overlay domain annotations
#     for domain in domain_annotations:
#         start, end, label = domain
#         domain_ax.add_patch(Rectangle((start, 0), end - start, 0.9, facecolor='orange', edgecolor='none', alpha=0.5))
#         domain_ax.text((start + end) / 2, 2.1, label, ha='center', va='center', color='black', size=8)
#
#     # Plotting Rate4Site scores on secondary y-axis
#     ax2 = ax.twinx()
#     c = np.array(cons_vec)
#     c = c + abs(min(c))
#     c = c/max(c)
#     ax2.set_ylim(min(c), max(c)*1.1)
#     ax2.scatter(list(range(len(c))), c, color='green', label='Rate4Site Scores', alpha=0.4)
#     ax2.set_ylabel('Rate4Site Normalized', color='green', weight='bold')
#     ax2.tick_params(axis='y', labelcolor='green')
#     ax2.spines['right'].set_visible(True)
#     ax2.spines['top'].set_visible(False)
#
#     # Plotting mutation location and target region
#     if mutation_loc is not None:
#         ax.axvline(x=mutation_loc, ymax=1,color='r', linestyle='--', alpha=0.7)
#         ax.text(mutation_loc, 1.04, mut_name, color='r', weight='bold', ha='center')
#
#     if target_region is not None:
#         ax.add_patch(Rectangle((target_region[0], 0), target_region[1] - target_region[0], 1, alpha=0.25, facecolor='gray'))
#         center_loc = target_region[0] + 0.5 * (target_region[1] - target_region[0])
#         ax.text(center_loc, 1.04, 'Deleted Region', ha='center', va='center', color='gray', weight='bold')
#
#     plt.show()
#
