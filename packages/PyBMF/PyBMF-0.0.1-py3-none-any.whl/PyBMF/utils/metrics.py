from .boolean_utils import multiply, matmul, dot, power, ismat
from .sparse_utils import to_dense, to_triplet, to_sparse
from scipy.sparse import spmatrix, issparse, csr_matrix
import numpy as np
from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score


def get_metrics(gt, pd, metrics, axis=None):
    '''Get results of the metrics all at once.

    Metrics from sklearn.metrics are included as sanity check. Their input must be binary `array`, which makes them slow and less flexible.

    Parameters
    ----------
    gt : array, spmatrix
        Ground truth, can be 1d array, 2d dense or sparse matrix.
    pd : array, spmatrix
        Prediction, can be 1d array, 2d dense or sparse matrix.
        When the input are matrices, row and column-wise measurement can be conducted by defining `axis`.
    metrics : list of str
        The name of metrics.
    axis : int in {0, 1}
        When `axis` == 0, The `result` containing the column-wise measurement has the same length as columns.

    Returns
    -------
    results : list
    '''
    if np.isnan(to_dense(pd, squeeze=True)).any():
        raise TypeError("NaN is found in prediction.")

    functions = {
        'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN,
        'TPR': TPR, 'FPR': FPR, 'TNR': TNR, 'FNR': FNR,
        'PPV': PPV, 'ACC': ACC, 'ERR': ERR, 'F1': F1,
        'Recall': TPR, 'Precision': PPV, 'Accuracy': ACC, 'Error': ERR, # alias
        'RMSE': RMSE, 'MAE': MAE, # real distances
    }
    sklearn_metrics = { 
        'recall_score': recall_score, 'precision_score': precision_score, 
        'accuracy_score': accuracy_score, 'f1_score': f1_score,
    }
    results = []
    for m in metrics:
        if m in functions:
            results.append(functions[m](gt, pd, axis))
        elif m in sklearn_metrics: # must be binary arrays
            gt = to_dense(gt).flatten()
            pd = to_dense(pd).flatten()
            results.append(sklearn_metrics[m](gt, pd))
        else:
            results.append(None)
    return results


def TP(gt, pd, axis=None):
    s = multiply(gt, pd, boolean=True).sum(axis=axis)
    return np.array(s).squeeze()


def FP(gt, pd, axis=None):
    diff = pd - gt
    if issparse(diff):
        s = diff.maximum(0).sum(axis=axis)
        return np.array(s).squeeze()
    else:
        s = np.maximum(diff, 0).sum(axis=axis)
        return s


def TN(gt, pd, axis=None):
    return TP(gt=invert(gt), pd=invert(pd), axis=axis)


def FN(gt, pd, axis=None):
    return FP(gt=pd, pd=gt, axis=axis)


def TPR(gt, pd, axis=None):
    '''sensitivity, recall, hit rate, or true positive rate
    '''
    denom = gt.sum(axis=axis)
    return TP(gt, pd, axis=axis) / denom if denom > 0 else 0


def TNR(gt, pd, axis=None):
    '''specificity, selectivity or true negative rate
    '''
    denom = invert(gt).sum(axis=axis)
    return TN(gt, pd, axis=axis) / denom if denom > 0 else 0


def FPR(gt, pd, axis=None):
    '''fall-out or false positive rate
    '''
    return 1 - TNR(gt, pd, axis=axis)


def FNR(gt, pd, axis=None):
    '''miss rate or false negative rate
    '''
    return 1 - TPR(gt, pd, axis=axis)


def PPV(gt, pd, axis=None):
    '''precision or positive predictive value
    '''
    denom = pd.sum(axis=axis)
    return TP(gt, pd, axis=axis) / denom if denom > 0 else 0


def ACC(gt, pd, axis=None):
    '''Accuracy.
    '''
    if len(pd.shape) == 2:
        n = pd.shape[0] * pd.shape[1] if axis is None else pd.shape[axis]
    else:
        n = len(pd)
    return (TP(gt, pd, axis) + TN(gt, pd, axis)) / n


def ERR(gt, pd, axis=None):
    '''Error rate.
    '''
    return 1 - ACC(gt, pd, axis)


def F1(gt, pd, axis=None):
    '''F1 score.

    tp = TP(gt, pd, axis)
    fp = FP(gt, pd, axis)
    fn = FN(gt, pd, axis)
    return 2 * tp / (2 * tp + fp + fn)
    '''
    precision = PPV(gt, pd, axis)
    recall = TPR(gt, pd, axis)
    denom = precision + recall
    return 2 * precision * recall / denom if denom > 0 else 0


def _get_size(X, axis=None):
    if axis is not None:
        return X.shape[axis]
    else:
        return X.shape[0] * X.shape[1] if len(X.shape) == 2 else len(X)


def RMSE(gt, pd, axis=None):
    N = _get_size(gt, axis=axis)
    rmse = np.sqrt(power(gt - pd, 2).sum(axis) / N)

    return rmse


def MAE(gt, pd, axis=None):
    N = _get_size(gt, axis=axis)
    mae = np.abs(gt - pd).sum(axis) / N

    return mae


def invert(X):
    if issparse(X):
        X = csr_matrix(np.ones(X.shape)) - X
    elif isinstance(X, np.ndarray):
        X = 1 - X
    else:
        raise TypeError
    return X


def description_length(gt, U, V, pd=None, w_model=1.0, w_fp=1.0, w_fn=1.0):
    '''The vanilla description length function.

    Will compute X_pd from U and V if pd is None.
    '''
    pd = matmul(U, V.T, sparse=True, boolean=True) if pd is None else pd
    return w_model * (U.sum() + V.sum()) + w_fp * FP(gt, pd) + w_fn * FN(gt, pd)


def weighted_error(gt, pd, w_fp=0.5, w_fn=None, axis=None):
    '''Coverage cost function to be minimized.
    '''
    w_fn = 1 - w_fp if w_fn is None else w_fn
    return w_fp * FP(gt, pd, axis=axis) + w_fn * FN(gt, pd, axis=axis)


def coverage_score(gt, pd, w_fp=0.5, w_fn=None, axis=None):
    '''Covergage score function to be maximized.

    Measure the coverage of X using Y.

    Parameters
    ----------
    axis : int in {0, 1}, default: None
        The dimension to which the basis belongs.
        When `axis` is None, return the overall coverage score.
        When `axis` is 0, the basis is at dimension 0, thus return the column-wise coverage scores.
    '''
    w_fn = 1 - w_fp if w_fn is None else w_fn
    return - w_fp * FP(gt, pd, axis=axis) + w_fn * TP(gt, pd, axis=axis) # P - weighted_error()