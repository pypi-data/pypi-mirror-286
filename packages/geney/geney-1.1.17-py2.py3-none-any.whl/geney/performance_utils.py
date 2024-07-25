import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt


# def plot_performance(true_values, predictions):
#     clinsig_map = {'Benign': 0, 'Pathogenic': 1}
#     true_values = [clinsig_map[t] for t in true_values]
#     predictions = scale_predictions(predictions)
#
#     fpr, tpr, thresholds_roc = roc_curve(true_values, predictions)
#
#     # Calculate Precision-Recall curve
#     precision, recall, thresholds_pr = precision_recall_curve(true_values, predictions)
#
#     # Plotting ROC curve
#     plt.figure(figsize=(20, 5))
#
#     plt.subplot(1, 4, 1)
#     plt.plot(fpr, tpr)
#     plt.title('ROC Curve')
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#
#     # Plotting Precision-Recall curve
#     plt.subplot(1, 4, 2)
#     plt.plot(recall, precision)
#     plt.title('Precision-Recall Curve')
#     plt.xlabel('Recall')
#     plt.ylabel('Precision')
#
#     # Plotting Precision vs. Thresholds
#     plt.subplot(1, 4, 3)
#     plt.plot(thresholds_pr, precision[:-1])  # Precision and thresholds have off-by-one lengths
#     plt.title('Precision vs. Threshold')
#     plt.xlabel('Threshold')
#     plt.ylabel('Precision')
#
#     # Plotting Sample Percentage Captured vs. Thresholds
#     plt.subplot(1, 4, 4)
#     # Assuming 'tpr' or another appropriate metric represents the cumulative percentage
#     plt.plot(thresholds_roc, tpr)  # Update 'tpr' with the correct metric if necessary
#     plt.title('Cumulative Percentage vs. Threshold')
#     plt.xlabel('Threshold')
#     plt.ylabel('Cumulative Percentage of Population')
#
#     plt.tight_layout()
#     plt.show()
#
#
#
# def plot_auc_curve(y_true, y_pred_proba):
#     """
#     Plots the AUC curve.
#
#     Args:
#         y_true (array-like): True labels (0 or 1).
#         y_pred_proba (array-like): Predicted probabilities for positive class.
#
#     Returns:
#         None
#     """
#     fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
#     auc_value = roc_auc_score(y_true, y_pred_proba)
#
#     plt.figure(figsize=(8, 6))
#     plt.plot(fpr, tpr, label=f"AUC = {auc_value:.2f}")
#     plt.plot([0, 1], [0, 1], 'k--')
#     plt.xlabel("False Positive Rate")
#     plt.ylabel("True Positive Rate")
#     plt.title("Receiver Operating Characteristic (ROC) Curve")
#     plt.legend()
#     plt.show()
#     return auc_value
#
#
# def optimal_ppv(dataframe, feature_name, plot=False):
#     """
#     Calculates the optimal positive predictive value (PPV) for a given feature.
#
#     Args:
#         dataframe (pd.DataFrame): Input dataframe.
#         feature_name (str): Name of the feature column.
#
#     Returns:
#         float: Optimal PPV.
#     """
#     # Assuming 'target' is the binary target column (0 or 1)
#     threshold_values = pd.qcut(dataframe[feature_name], 100, duplicates='drop')
#     ppv_values = []
#
#     for threshold in threshold_values:
#         predictions = (dataframe[feature_name] >= threshold).astype(int)
#         ppv = precision_score(dataframe['target'], predictions)
#         ppv_values.append(ppv)
#
#     optimal_threshold = threshold_values[np.argmax(ppv_values)]
#     optimal_ppv = max(ppv_values)
#     if plot:
#         plt.figure(figsize=(8, 6))
#         plt.scatter(threshold_values, ppv_values)
#         plt.xlabel("Threshold")
#         plt.ylabel("Positive Predictive Value (PPV)")
#         plt.title("Optimal Positive Predictive Value (PPV)")
#         plt.show()
#
#     return optimal_ppv, optimal_threshold
#
#
# def measure_prediction_quality(prediction_vector, quality_vector):
#     """
#     Measure the quality of the predictions using the quality_vector as the characteristic to check.
#     """
#     pass
#
#
#
# def create_ppv_vector(prediction_vector, true_value_vector):
#     """
#     Create a vector of positive predictive values (PPV) for the prediction_vector using the true_value_vector as the true values.
#     """
#     df = pd.DataFrame({'prediction': prediction_vector, 'true_value': true_value_vector})
#     df.sort_values('prediction', ascending=True, inplace=True)
#     df['bin'] = pd.qcut(df['prediction'], 100, labels=False, duplicates=True, retbins=True)
#     for bin in df.bin.unique():
#         temp_df = df[df.bin >= bin].
#
#
# def group_retention(predictions, predictor):
#     # first i need to get the ratio of values that are retained at particular values
#     predictions.sort_values(predictor, inplace=True)
#     _, thresholds = pd.qcut(predictions[predictor], 100, duplicates='drop')
#     tracker = []
#     for th in thresholds:
#
#
