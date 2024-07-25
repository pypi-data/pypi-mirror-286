from sklearn import decomposition
from .ContinuousModel import ContinuousModel
from ..utils import to_sparse, get_prediction_with_threshold


class NMFSklearn(ContinuousModel):
    '''NMF by scikit-learn.
    '''
    def __init__(self, k, U=None, V=None, beta_loss='frobenius', init_method='nndsvd', solver='cd', tol=1e-4, max_iter=1000, seed=None):
        '''
        Parameters
        ----------
        U, V : numpy.ndarray, spmatrix
            Need to be prepared if `init_method` is 'custom'.
        '''
        self.check_params(k=k, U=U, V=V, beta_loss=beta_loss, init_method=init_method, solver=solver, tol=tol, max_iter=max_iter, seed=seed)
        

    def check_params(self, **kwargs):
        super().check_params(**kwargs)

        # self.set_params(['beta_loss', 'solver'], **kwargs)
        assert self.solver in ['cd', 'mu']
        assert self.beta_loss in ['frobenius', 'kullback-leibler', 'itakura-saito']
        assert self.init_method in [None, 'random', 'nndsvd', 'nndsvda', 'nndsvdar', 'custom']
        
    
    def fit(self, X_train, X_val=None, X_test=None, **kwargs):
        super().fit(X_train, X_val, X_test, **kwargs)

        self._fit()

        # self.predict_X(boolean=False)
        self.X_pd = get_prediction_with_threshold(U=self.U, V=self.V, u=0.5, v=0.5)
        self.finish(show_logs=self.show_logs, save_model=self.save_model, show_result=self.show_result)


    def _fit(self):
        self.model = decomposition.NMF(
            n_components=self.k, 
            init=self.init_method, 
            random_state=self.rng, 
            solver=self.solver,
            beta_loss=self.beta_loss,
            tol=self.tol,
            max_iter=self.max_iter,
            alpha_W=0.0,
            alpha_H="same",
            l1_ratio=0.0,
            verbose=0,
            shuffle=False
        )

        # init guess W and H will only be used when init_method is 'custom'
        if self.init_method == 'custom':
            self.U = self.model.fit_transform(self.X_train, W=self.U, H=self.V.T)
        else:
            self.U = self.model.fit_transform(self.X_train)

        self.V = self.model.components_.T

        self.U, self.V = to_sparse(self.U), to_sparse(self.V)
