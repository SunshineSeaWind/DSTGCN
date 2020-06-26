from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from scipy.stats import pearsonr
import numpy as np
from sklearn import metrics


# 衡量模型的性能
def evaluate(y_predictions: np.ndarray, y_targets: np.ndarray, threshold: float = 0.5):
    """
    :param y_predictions: a 1d array, with length as number of samples
    :param y_targets: a 1d array, with length as number of samples
    :param threshold: threshold, default 0.5
    :return:
    """
    assert y_predictions.shape == y_targets.shape, \
        f'Predictions of shape {y_predictions.shape} while targets of shape {y_predictions.shape}.'
    mse = mean_squared_error(y_targets, y_predictions)
    rmse = mse ** 0.5
    mae = mean_absolute_error(y_targets, y_predictions)
    pcc, p_value = pearsonr(y_predictions, y_targets)

    y_predictions = y_predictions >= threshold
    y_targets = y_targets == 1

    correct = (y_predictions == y_targets).sum()
    accuracy = correct / len(y_predictions)

    tp = ((y_predictions == 1) & (y_targets == 1)).sum()
    fp = ((y_predictions == 1) & (y_targets == 0)).sum()
    fn = ((y_predictions == 0) & (y_targets == 1)).sum()

    if tp + fp != 0:
        precision = tp / (tp + fp)
    else:
        precision = 0.0
    if tp + fn != 0:
        recall = tp / (tp + fn)
    else:
        recall = 0.0
    if precision + recall != 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0.0

    auc = metrics.roc_auc_score(y_targets, y_predictions)

    del y_predictions, y_targets, correct, tp, fp, fn, threshold

    # MSE, RMSE, MAE, PCC, P-VALUE, PRECISION, RECALL, F1-SCORE, AUC
    return {key.upper().replace('_', '-'): val for key, val in locals().items()}
