from .ContinuousCollectiveModel import ContinuousCollectiveModel
from .BinaryMFPenalty import BinaryMFPenalty
import numpy as np
from ..utils import concat_Xs_into_X, split_U_into_Us
from ..utils import to_dense, sigmoid, d_sigmoid, matmul, multiply, binarize
from ..utils import RMSE, TPR, PPV, ACC, F1, get_metrics, ismat


class CMF(ContinuousCollectiveModel):
    '''Collective Matrix Factorization.

    Reference
    ---------
    Relational learning via collective matrix factorization.

    TODO: W
    '''
    def __init__(self, k, alpha, Us=None, Ws='full', link=None, lr=0.1, reg=0.1, tol=0.0, max_iter=50, init_method='custom', seed=None):
        '''
        Parameters
        ----------
        k : int
            Rank.
        alpha : list of float
            Importance weights of each matrix.
        Ws : list of ndarray or spmatrix, or str in ['mask', 'full']
        init_method : list of str in ['bmf', 'normal', 'uniform']
        link : list of str in ['linear', 'sigmoid']
        '''
        self.check_params(k=k, alpha=alpha, Us=Us, Ws=Ws, link=link, lr=lr, reg=reg, tol=tol, max_iter=max_iter, init_method=init_method, seed=seed)


    def check_params(self, **kwargs):
        super().check_params(**kwargs)

        assert self.init_method in ['normal', 'uniform', 'custom']


    def fit(self, Xs_train, factors, Xs_val=None, Xs_test=None, **kwargs):
        super().fit(Xs_train, factors, Xs_val, Xs_test, **kwargs)

        self._fit()
    

    def init_model(self):
        '''Initialize factors and logging variables.
        '''
        super().init_model()

        self.init_Us()
        self._to_dense()


    def _fit(self):
        n_iter = 0
        is_improving = True
        while is_improving:
            for f in self.factor_list:
                self.newton_update(f)

            self.predict_Xs()

            error, rec_error, reg_error = self.error()
            rmse = RMSE(self.Ws[0] * self.Xs_train[0], self.Ws[0] * self.Xs_pd[0])

            # early stop
            if n_iter > self.max_iter:
                self.early_stop(n_iter=n_iter)
                is_improving = False
                break

            self.print_msg("error: {:.3e}, rec_error: {:.3e}, reg_error: {:.3e}, rmse: {:.3e}".format(error, rec_error, reg_error, rmse))

            # evaluation, boolean
            # self.predict_Xs(us=0, boolean=True)
            # self.evaluate(df_name='updates_boolean', head_info={'iter': n_iter})
            # if n_iter % 10 == 0:
            #     self.show_matrix(colorbar=True, discrete=True, center=True, clim=[0, 1])

            # evaluation, continuous
            self.predict_Xs()
            self.evaluate(df_name='updates', head_info={'iter': n_iter, 'error': error, 'rec_error': rec_error, 'reg_error': reg_error}, metrics=['RMSE', 'MAE'])
            if n_iter % 10 == 0:
                self.show_matrix(colorbar=True)

            n_iter += 1


    def predict_Xs(self, Us=None):
        super().predict_Xs(Us=Us, us=None, boolean=False)

        for m in range(self.n_matrices):
            if self.link[m] == 'linear':
                pass
            elif self.link[m] == 'logistic':
                self.Xs_pd[m] = sigmoid(self.Xs_pd[m])


    def error(self):
        reg_error = 0
        for f in self.factor_list:
            for m in self.matrices[f]:
                a = self.alpha[m]
                U = self.Us[f].flat
                reg_error += a * self.reg * np.linalg.norm(U) / 2 # l2 norm

        rec_error = 0
        for m in range(self.n_matrices):
            X_gt = self.Xs_train[m]
            X_pd = self.Xs_pd[m]
            W = self.Ws[m]
            a = self.alpha[m]

            diff = multiply(W, X_gt - X_pd)
            rec_error += a * np.sum(diff ** 2)

        error = rec_error + reg_error
        return error, rec_error, reg_error


    def newton_update(self, f):
        b = np.zeros(self.k) # gradient, q(Ui)
        A = np.zeros((self.k, self.k)) # Hessian, q'(Ui)

        dim = self.factor_dims[f]

        for r in range(dim):
            A[:] = 0
            b[:] = 0
            for m in self.matrices[f]:
                if self.alpha[m] == 0:
                    continue

                if f in self.row_factors:
                    X = self.Xs_train[m]
                    U = self.Us[f][r, :]
                    o = self.factors[m][1]
                    V = self.Us[o]

                    XiV = np.dot(X[r, :], V)
                    UiVt = np.dot(U, V.T)

                    if self.link[m] == "linear":
                        UiVtV = np.dot(UiVt, V)
                        Hes = np.dot(np.multiply(V.T, UiVt), V)
                    elif self.link[m] == 'logistic':
                        UiVtV = np.dot(sigmoid(UiVt), V)
                        Hes = np.dot(np.multiply(V.T, d_sigmoid(UiVt)), V)

                    A += self.alpha[m] * Hes
                    b += self.alpha[m] * (UiVtV - XiV)

                elif f in self.col_factors:
                    X = self.Xs_train[m]
                    o = self.factors[m][0]
                    U = self.Us[o]
                    V = self.Us[f][r, :]

                    XiU = np.dot(X[:, r].T, U)
                    UVt = np.dot(U, V.T)

                    if self.link[m] == "linear":
                        UVtU = np.dot(UVt.T, U)
                        Hes = np.dot(np.multiply(U.T, UVt), U)
                    elif self.link[m] == 'logistic':
                        UVtU = np.dot(sigmoid(UVt).T, U)
                        Hes = np.dot(np.multiply(U.T, d_sigmoid(UVt)), U)

                    A += self.alpha[m] * Hes
                    b += self.alpha[m] * (UVtU - XiU)
                
            if np.all(b == 0):
                continue
                
            # regularizer
            A += self.reg * np.eye(self.k, self.k)
            b += self.reg * self.Us[f][r, :].copy() # the previous factor for i-th data

            d = np.dot(b, np.linalg.inv(A))
            self.Us[f][r, :] -= self.lr * d
