from .BaseModel import BaseModel
import numpy as np
from ..utils import binarize, matmul, to_dense, to_sparse, ismat
from scipy.sparse import csr_matrix


class ContinuousModel(BaseModel):
    '''Continuous binary matrix factorization.
    
    Reference
    ---------
    Binary Matrix Factorization with Applications
    Algorithms for Non-negative Matrix Factorization
    '''
    def __init__(self):
        raise NotImplementedError("This is a template class.")
    

    def init_model(self):
        '''The `BaseModel.init_model()` for continuous models.
        '''
        if hasattr(self, 'init_method') and self.init_method == 'custom':
            # using custom factors, just init logging variables
            self._init_logs()
        else:
            # init factors and logging variables
            self._init_factors()
            self._init_logs()

        if hasattr(self, 'W'):
            self.init_W()


    def init_W(self):
        '''Initialize masking weights. Turning codenames into matrix.

        'mask' :
            W will be assigned 1 for any entrance in X_train, no matter if the value is 1, or 0 added through negative sampling.
        'full' :
            W is full 1 matrix.

        TODO: to avoid dense W as much as possible
        TODO: to support dense X_train
        '''
        # assert self.W in ['mask', 'full'] or ismat(self.W)

        if isinstance(self.W, str):
            if self.W == 'mask':
                self.W = self.X_train.copy()
                self.W.data = np.ones(self.X_train.data.shape)
            elif self.W == 'full':
                self.W = np.ones((self.m, self.n))

        self.W = to_sparse(self.W, type='csr')
        

    def init_UV(self):
        '''Initialize factors.
        '''
        if self.init_method == "normal":
            avg = np.sqrt(self.X_train.mean() / self.k)
            V = avg * self.rng.standard_normal(size=(self.n, self.k))
            U = avg * self.rng.standard_normal(size=(self.m, self.k))
            self.U, self.V = np.abs(U), np.abs(V)
            self.U[self.U == 0] = np.finfo(np.float64).eps
            self.V[self.V == 0] = np.finfo(np.float64).eps
        elif self.init_method == "uniform":
            avg = np.sqrt(self.X_train.mean() / self.k)
            self.V = self.rng.uniform(low=0, high=avg * 2, size=(self.n, self.k))
            self.U = self.rng.uniform(low=0, high=avg * 2, size=(self.m, self.k))
            self.U[self.U == 0] = np.finfo(np.float64).eps
            self.V[self.V == 0] = np.finfo(np.float64).eps
        elif self.init_method == "custom":
            assert hasattr(self, 'U') and hasattr(self, 'V') # U and V must be provided at this point

        self.U, self.V = to_sparse(self.U), to_sparse(self.V)


    def normalize_UV(self, method='balance'):
        '''Normalize factors.

        Parameters
        ----------
        method : str, ['balance', 'normalize']
            'balance': balance each pair of factors, used in `BinaryMFPenalty`.
            'normalize': normalize to [0, 1], used in `BinaryMFThreshold`.

        Reference
        ---------
        Binary Matrix Factorization with Applications
        '''
        a, c = [self.U.min(), self.U.max()], [self.V.min(), self.V.max()]

        if method == 'balance':
            diag_U = to_dense(np.sqrt(np.max(self.U, axis=0))).flatten()
            diag_V = to_dense(np.sqrt(np.max(self.V, axis=0))).flatten()
            for i in range(self.k):
                self.U[:, i] = self.U[:, i] * diag_V[i] / diag_U[i]
                self.V[:, i] = self.V[:, i] * diag_U[i] / diag_V[i]
        elif method == 'normalize':
            # for i in range(self.k):
            #     self.U[:, i] = self.U[:, i] / self.U[:, i].max()
            #     self.V[:, i] = self.V[:, i] / self.V[:, i].max()
            self.U, self.V = self.U / self.U.max(), self.V / self.V.max()

        b, d = [self.U.min(), self.U.max()], [self.V.min(), self.V.max()]

        print("[I] Normalized from: U: [{:.4f}, {:.4f}], V: [{:.4f}, {:.4f}]".format(a[0], a[1], c[0], c[1]))
        print("[I] Normalized to  : U: [{:.4f}, {:.4f}], V: [{:.4f}, {:.4f}]".format(b[0], b[1], d[0], d[1]))


    def show_matrix(self, settings=None, u=None, v=None, boolean=True, **kwargs):
        '''Wrapper of `BaseModel.show_matrix()` with thresholds `u` and `v`.
        '''
        if settings is None:
            U = binarize(self.U, u) if boolean and u is not None else self.U
            V = binarize(self.V, v) if boolean and v is not None else self.V
            X = matmul(U, V.T, boolean=boolean)
            settings = [(X, [0, 0], "X"), (U, [0, 1], "U"), (V.T, [1, 0], "V")]
        super().show_matrix(settings, **kwargs)


    # def finish(self, show_logs=True, show_matrix=True, save_model=True):
    #     '''Wrapepr for `BaseModel.finish()`.
    #     '''
    #     super().finish(show_logs, show_matrix, save_model)
    

    def _show_matrix(self):
        '''Wrapper for `BaseModel._show_matrix()`.
        '''
        settings = [(self.X_train, [0, 0], 'gt'), (self.X_pd, [0, 1], 'pd')]
        self.show_matrix(settings, colorbar=True, discrete=False, keep_nan=False)


    def _to_dense(self):
        '''Turn X, W, U and V into dense matrices.

        For temporary use during development.
        '''
        self.X_train = to_dense(self.X_train)
        self.W = to_dense(self.W)
        self.U = to_dense(self.U)
        self.V = to_dense(self.V)
        if self.X_val is not None:
            self.X_val = to_dense(self.X_val)
        if self.X_test is not None:
            self.X_test = to_dense(self.X_test)


    def _to_float(self):
        '''Turn X, W, U and V into float matrices.

        For temporary use during development.
        '''
        self.X_train = self.X_train.astype(np.float64)
        self.W = self.W.astype(np.float64)
        self.U = self.U.astype(np.float64)
        self.V = self.V.astype(np.float64)
        if self.X_val is not None:
            self.X_val = self.X_val.astype(np.float64)
        if self.X_test is not None:
            self.X_test = self.X_test.astype(np.float64)


    def _to_bool(self):
        '''Turn X, W, U and V into bool matrices.

        For temporary use during development.
        '''
        self.X_train = self.X_train.astype(bool)
        self.W = self.W.astype(bool)
        self.U = self.U.astype(bool)
        self.V = self.V.astype(bool)
        if self.X_val is not None:
            self.X_val = self.X_val.astype(bool)
        if self.X_test is not None:
            self.X_test = self.X_test.astype(bool)