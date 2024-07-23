import matplotlib.pyplot as plt
import numpy as np
from bokeh.palettes import Category20

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import roc_curve, auc

import tiana.file_organizers.file_reading as fr
import threshold_metrics as tm


def confusion_matrix_plotter(*, true_labels_, predictions_,
                             inference_path_, dataset_type_, test_split_,
                             threshold_value_,
                             should_normalize_=None,
                             labels_=None,
                             show_plot_=False, save_plot_=False, small_size=False):
    """
    This function plots the confusion matrix
    :param save_plot_:
    :param true_labels_:
    :param predictions_: 
    :param inference_path_:
    :param dataset_type_:
    :param test_split_: 
    :param threshold_value_: 
    :param should_normalize_: 
    :param labels_: 
    :param show_plot_: 
    :param small_size: Don't use this - not working properly
    :return: 
    """
    if labels_ is None:
        labels_ = ['Not \n Microlensing', 'Microlensing']

    disp = ConfusionMatrixDisplay.from_predictions(true_labels_,
                                                   predictions_,
                                                   display_labels=labels_,
                                                   cmap=plt.cm.Blues,
                                                   normalize=should_normalize_)

    plt.title(f'Confusion Matrix - Threshold: {threshold_value_} | {dataset_type_} ts{test_split_}')

    if save_plot_:
        if small_size:
            plt.rcParams['figure.figsize'] = [4, 4]
            plt.tight_layout()
            if should_normalize_ == 'true':
                plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/normalized_confusion_matrix_'
                            f'{threshold_value_}_ts{test_split_}_small.png', dpi=300)
            else:
                plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/confusion_matrix_'
                            f'{threshold_value_}_ts{test_split_}_small.png', dpi=300)
        else:
            plt.tight_layout()
            if should_normalize_ == 'true':
                plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/normalized_confusion_matrix_'
                            f'{threshold_value_}_ts{test_split_}.png', dpi=300)
            else:
                plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/confusion_matrix_'
                            f'{threshold_value_}_ts{test_split_}.png', dpi=300)
    if show_plot_:
        plt.show()
    plt.close()


def inference_cumulative_distribution(*, inference_with_threshold_df_,
                                      inference_path_, dataset_type_, test_split_,
                                      show_plot_=False, save_plot_=False):
    """
    This function plots the cumulative distribution of the inference
    :param save_plot_:
    :param test_split_:
    :param dataset_type_:
    :param inference_path_:
    :param show_plot_:
    :param inference_with_threshold_df_:
    :return:
    """
    microlensing_df = inference_with_threshold_df_[inference_with_threshold_df_['true_label'] == 1]
    non_microlensing_df = inference_with_threshold_df_[inference_with_threshold_df_['true_label'] == 0]

    # Scores in ascending order:
    microlensing_scores = microlensing_df.sort_values('Score')['Score']
    non_microlensing_scores = non_microlensing_df.sort_values('Score')['Score']

    # Inserting 0 and 1s
    microlensing_scores = np.insert(microlensing_scores, 0, 0)
    microlensing_scores = np.insert(microlensing_scores, len(microlensing_scores), 1)
    non_microlensing_scores = np.insert(non_microlensing_scores, 0, 0)
    non_microlensing_scores = np.insert(non_microlensing_scores, len(non_microlensing_scores), 1)

    # Defining CDF values
    step_microlensing = 1/ (len(microlensing_scores) - 1)
    microlensing_cdf = np.arange(0, 1+step_microlensing/2, step_microlensing)
    step_non_microlensing = 1/(len(non_microlensing_scores) - 1)
    non_microlensing_cdf = np.arange(0, 1+step_non_microlensing/2, step_non_microlensing)

    fig, ax = plt.subplots()
    ax.step(microlensing_scores, microlensing_cdf, label=f'Microlensing: {len(microlensing_scores) - 2}')
    ax.step(non_microlensing_scores, non_microlensing_cdf, label=f'Not Microlensing: {len(non_microlensing_scores) - 2}', color='orange')
    ax.set(xlabel='Neural Network Confidence', ylabel='Cumulative Distribution',
           title=f'Cumulative Distribution {dataset_type_} ts{test_split_}')
    ax.legend()
    if save_plot_:
        plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/cumulative_'
                    f'ts{test_split_}.png', dpi=300)
    if show_plot_:
        plt.show()
    plt.close()


def inference_cumulative_distribution_per_tag(*, inference_with_threshold_df_,
                                              inference_path_, dataset_type_, test_split_,
                                              show_plot_=False, save_plot_=False):
    """
    This function plots the cumulative distribution of the inference per tags
    :param save_plot_:
    :param test_split_:
    :param dataset_type_:
    :param inference_path_:
    :param show_plot_:
    :param inference_with_threshold_df_:
    :return:
    """
    sumi_tags = ['v', 'n', 'nr', 'm', 'j', '', 'c', 'cf', 'cp', 'cw', 'cs', 'cb']
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    ax.set(xlabel='Neural Network Confidence', ylabel='Cumulative Distribution ',
           title=f'Cumulative Distribution {dataset_type_} ts{test_split_}')
    for sumi_tag, color_index in zip(sumi_tags, np.arange(0, len(sumi_tags))):
        sumi_tag_df = inference_with_threshold_df_[inference_with_threshold_df_['sumi_tag'] == sumi_tag]
        # Scores in ascending order:
        sumi_tag_scores = sumi_tag_df.sort_values('Score')['Score']
        # Inserting 0 and 1s
        sumi_tag_scores = np.insert(sumi_tag_scores, 0, 0)
        sumi_tag_scores = np.insert(sumi_tag_scores, len(sumi_tag_scores), 1)
        # Defining CDF values
        step_sumi_tag = 1 / (len(sumi_tag_scores) - 1)
        sumi_tag_cdf = np.arange(0, 1 + step_sumi_tag / 2, step_sumi_tag)
        # Plotting
        tag_name = fr.meaning_of_sumi_tags(sumi_tag)
        ax.step(sumi_tag_scores, sumi_tag_cdf, label=f'{tag_name}: {len(sumi_tag_cdf) - 2}',
                color=Category20[20][color_index])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    if save_plot_:
        plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/cumulative_'
                    f'ts{test_split_}_per_tag.png', dpi=300)
    if show_plot_:
        plt.show()
    plt.close()


def roc_plotter(*, inference_df_,
                inference_path_, dataset_type_, test_split_,
                show_plot_=False, save_plot_=False):
    """
    From this example https://scikit-learn.org/stable/auto_examples/
    model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py
    :param save_plot_:
    :param show_plot_:
    :param test_split_:
    :param dataset_type_:
    :param inference_path_:
    :param inference_df_:
    :param dataframe_:
    :return:
    """
    # Compute ROC curve and ROC area for each class
    false_positive_rate, true_positive_rate, _ = roc_curve(inference_df_['true_label'], inference_df_['Score'])
    roc_auc = auc(false_positive_rate, true_positive_rate)

    plt.figure()
    plt.plot(false_positive_rate, true_positive_rate,
             color="maroon", lw=3,
             label="ROC curve (area = %0.5f)" % roc_auc)
    # diagonal
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Diagonal Line TPR = FPR")
    # plt.xlim([-0.05, 1.0])
    # plt.ylim([-0.05, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"Receiver Operating Characteristic | {dataset_type_} ts{test_split_}")
    plt.legend(loc="lower right")
    if save_plot_:
        plt.savefig(f'{inference_path_}/{dataset_type_}_inference_plots/ROC_curve_'
                    f'ts{test_split_}.png', dpi=300)
    if show_plot_:
        plt.show()
    plt.close()


if __name__ == '__main__':
    dataset_type = '550k'
    test_split = 0
    threshold_value = 0.5

    inference_folder = '/Users/sishitan/Documents/Scripts/qusi_project/qusi/inferences/'
    inference_file = f'results_ts{test_split}_{dataset_type}_with_tags.csv'

    inference_df = fr.read_inference_with_tags_and_labels(inference_folder + inference_file)
    inference_with_threshold_df = tm.threshold_prediction_setter(inference_df, threshold_value)
    true_labels = inference_with_threshold_df['true_label']
    predictions = inference_with_threshold_df['prediction']

    confusion_matrix_plotter(true_labels_=true_labels, predictions_=predictions,
                             inference_path_=inference_folder, dataset_type_=dataset_type, test_split_=test_split,
                             threshold_value_=threshold_value,
                             save_plot_=True)
    confusion_matrix_plotter(true_labels_=true_labels, predictions_=predictions,
                             inference_path_=inference_folder, dataset_type_=dataset_type, test_split_=test_split,
                             threshold_value_=threshold_value,
                             save_plot_=True, should_normalize_='true')

    true_positives, false_positives, true_negatives, false_negatives = tm.performance_calculator(true_labels_=true_labels,
                                                                                                 predictions_=predictions)
    print('True Positives: ', true_positives)
    print('False Positives: ', false_positives)
    print('True Negatives: ', true_negatives)
    print('False Negatives: ', false_negatives)

    inference_cumulative_distribution(inference_with_threshold_df_=inference_with_threshold_df,
                                      inference_path_=inference_folder, dataset_type_=dataset_type,
                                      test_split_=test_split,
                                      save_plot_=True)
    inference_cumulative_distribution_per_tag(inference_with_threshold_df_=inference_with_threshold_df,
                                              inference_path_=inference_folder, dataset_type_=dataset_type,
                                              test_split_=test_split,
                                              save_plot_=True)

    roc_plotter(inference_df_=inference_df, inference_path_=inference_folder,
                dataset_type_=dataset_type, test_split_=test_split,
                save_plot_=True)
