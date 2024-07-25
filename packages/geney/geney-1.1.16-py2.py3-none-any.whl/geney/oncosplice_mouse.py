from geney.oncosplice import *
from copy import deepcopy
import pandas as pd
import numpy as np
from geney.Fasta_segment import Fasta_segment
import torch

config_setup = { "BASE": "/tamir2/nicolaslynntest/experimental/oncosplice_mouse",
                 "ONCOSPLICE": "/tamir2/nicolaslynntest/experimental/oncosplice_mouse/oncosplice",
                 "CHROM_SOURCE": "/tamir2/nicolaslynntest/experimental/oncosplice_mouse/chromosomes",
                 "MRNA_PATH": "/tamir2/nicolaslynntest/experimental/oncosplice_mouse/annotations",
                 "MISSPLICING_PATH": "/tamir2/nicolaslynntest/experimental/oncosplice_mouse/missplicing"}


from pkg_resources import resource_filename
from pangolin.model import *


IN_MAP = np.asarray([[0, 0, 0, 0],
                     [1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])
INDEX_MAP = {0:1, 1:2, 2:4, 3:5, 4:7, 5:8, 6:10, 7:11}
model_nums = [1, 3, 5, 7]

models = []
for i in model_nums:
    for j in range(1, 6):
        model = Pangolin(L, W, AR)
        if torch.cuda.is_available():
            model.cuda()
            weights = torch.load(resource_filename("pangolin","models/final.%s.%s.3" % (j, i)))
        else:
            weights = torch.load(resource_filename("pangolin","models/final.%s.%s.3" % (j, i)),
                                 map_location=torch.device('cpu'))
        model.load_state_dict(weights)
        model.eval()
        models.append(model)

def one_hot_encode(seq, strand='+'):
    seq = seq.upper().replace('A', '1').replace('C', '2')
    seq = seq.replace('G', '3').replace('T', '4').replace('N', '0')
    if strand == '+':
        seq = np.asarray(list(map(int, list(seq))))
    elif strand == '-':
        seq = np.asarray(list(map(int, list(seq[::-1]))))
        seq = (5 - seq) % 5  # Reverse complement
    return IN_MAP[seq.astype('int8')]


def run_pangolin_seq(seq):
    seq = one_hot_encode(seq, '+').T
    seq = torch.from_numpy(np.expand_dims(seq, axis=0)).float()

    if torch.cuda.is_available():
        seq = seq.to(torch.device("cuda"))

    score = []
    for j, model_num in enumerate(model_nums):
        # score = []
        # Average across 5 models
        for model in models[5*j:5*j+5]:
            with torch.no_grad():
                score.append(model(seq)[0][INDEX_MAP[model_num],:].cpu().numpy())
    return np.mean(score, axis=0)

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


def run_pangolin_comparison(mutations, transcript_data, sai_mrg_context=5000, min_coverage=2500, sai_threshold=0.5):
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

    visible_donors = np.intersect1d(transcript_data.donors, ref_indices)
    visible_acceptors = np.intersect1d(transcript_data.acceptors, ref_indices)

    if rev:
        ref_seq = reverse_complement(ref_seq)
        mut_seq = reverse_complement(mut_seq)
        ref_indices = ref_indices[::-1]
        mut_indices = mut_indices[::-1]

    ref_seq_probs = run_pangolin_seq(ref_seq)
    mut_seq_probs = run_pangolin_seq(mut_seq)


    assert len(ref_indices) == len(ref_seq_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_probs), 'Mut pos not the same'

    iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_probs))},
                               visible_acceptors,
                               threshold=sai_threshold)


    idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_probs))},
                               visible_donors,
                               threshold=sai_threshold)


    ref_acceptors = {a: b for a, b in list(zip(ref_indices, ref_seq_probs))}
    ref_donors = {a: b for a, b in list(zip(ref_indices, ref_seq_probs))}

    lost_acceptors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_acceptors[p]), 3)} for p in visible_acceptors if p not in mut_indices and p not in dap}
    lost_donors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_donors[p]), 3)} for p in visible_donors if p not in mut_indices and p not in ddp}
    dap.update(lost_acceptors)
    ddp.update(lost_donors)

    missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap, 'discovered_donors': idp}
    missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
    return {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in missplicing.items()}


class PredictPangolin:
    def __init__(self, mutation, gene_data,
                threshold=0.5, context=5000, coverage=2500):
        self.modification = mutation
        self.threshold = threshold
        self.transcript_id = gene_data.transcript_id
        self.spliceai_db = config_setup['MISSPLICING_PATH'] / f'spliceai_epistatic'
        self.missplicing = {}
        self.missplicing = run_pangolin_comparison(self.modification, transcript_data=gene_data, sai_mrg_context=context, min_coverage=coverage, sai_threshold=0.1)


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

    def apply_sai_threshold(self, splicing_dict=None, threshold=None):
        splicing_dict = self.missplicing if not splicing_dict else splicing_dict
        threshold = self.threshold if not threshold else threshold
        new_dict = {}
        for event, details in splicing_dict.items():
            for e, d in details.items():
                if abs(d['delta']) >= threshold:
                    return splicing_dict
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


def oncosplice(mut_id, sai_threshold=0.5, protein_coding=True, primary_transcript=False, per_transcript_missplicing=False, window_length=13, save_spliceai_results=False, force_spliceai=False):
    mutation = Variations(mut_id)
    try:
        reference_gene = Gene(mutation.gene)
    except FileNotFoundError:
        return pd.DataFrame()

    reference_gene_proteines = {g.protein: g.transcript_id for g in reference_gene.run_transcripts()}
    mutated_gene = Gene(mutation.gene, mut_id)


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


