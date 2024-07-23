import numpy as np
from sklearn.metrics import confusion_matrix


def threshold_prediction_setter(inference_df_, threshold_):
    """
    This sets the "prediction" columns based on the
    threshold
    :param threshold_:
    :return:
    """
    inference_df_['prediction'] = np.where(inference_df_['Score'] >= threshold_, True, False)
    return inference_df_


def performance_calculator(*, true_labels_, predictions_):
    """
    This function return the number of true_negatives, false_positives, false_negatives, true_positives
    :param true_labels_:
    :param predictions_:
    :return: true_negatives, false_positives, false_negatives, true_positives
    """
    true_negatives, false_positives, false_negatives, true_positives = confusion_matrix(true_labels_,
                                                                                        predictions_).ravel()
    return true_positives, false_positives, true_negatives, false_negatives

