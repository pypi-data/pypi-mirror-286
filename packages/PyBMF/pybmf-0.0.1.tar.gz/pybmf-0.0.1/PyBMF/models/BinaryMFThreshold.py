from .ContinuousModel import ContinuousModel
from ..utils import multiply, power, sigmoid, ignore_warnings, subtract, get_prediction, get_prediction_with_threshold, ismat
import numpy as np
from ..solvers import line_search


class BinaryMFThreshold(ContinuousModel):
    '''Binary matrix factorization, thresholding algorithm.

    - solver: (projected) line search
    - for sigmoid link function, use `BinaryMFThresholdExSigmoid`
    - for columnwise thresholds, use `BinaryMFThresholdExColumnwise`
    - for both, use `BinaryMFThresholdExSigmoidColumnwise`
    
    Reference
    ---------
    Binary Matrix Factorization with Applications.
    Algorithms for Non-negative Matrix Factorization.
    '''
    def __init__(self, k, U, V, W='mask', u=0.5, v=0.5, lamda=100, solver="line-search", min_diff=1e-3, max_iter=100, init_method='custom', seed=None):
        '''
        Parameters
        ----------
        u, v : float
            Initial threshold for `U` and `V`.
        lamda : float
            The 'lambda' in sigmoid function.
        '''
        self.check_params(k=k, U=U, V=V, W=W, u=u, v=v, lamda=lamda, solver=solver, min_diff=min_diff, max_iter=max_iter, init_method=init_method, seed=seed)
        

    def check_params(self, **kwargs):
        super().check_params(**kwargs)

        assert self.solver in ['line-search']
        assert self.init_method in ['custom']
        assert ismat(self.W) or self.W in ['mask', 'full']


    def fit(self, X_train, X_val=None, X_test=None, **kwargs):
        super().fit(X_train, X_val, X_test, **kwargs)

        self._fit()
        self.finish(show_logs=self.show_logs, save_model=self.save_model, show_result=self.show_result)


    def init_model(self):
        '''Initialize factors and logging variables.
        '''
        super().init_model()

        self.normalize_UV(method="normalize")

        self._to_dense()
        self._to_float()


    def _fit(self):
        '''The gradient descent method.
        '''
        n_iter = 0
        is_improving = True

        # initial point
        x_last = np.array([self.u, self.v]) # initial point
        p_last = -self.dF(x_last) # descent direction
        new_fval = self.F(x_last) # initial value

        # initial evaluation
        self.X_pd = get_prediction_with_threshold(U=self.U, V=self.V, u=self.u, v=self.v)
        self.evaluate(df_name='updates', head_info={'iter': n_iter, 'u': self.u, 'v': self.v, 'F': new_fval})
        
        while is_improving:
            # update n_iter
            n_iter += 1

            # set xk, pk
            xk = x_last # starting point
            pk = p_last # searching direction
            # pk = pk / np.sqrt(np.sum(pk ** 2)) # debug: normalize

            print("[I] iter: {}, start: [{:.3f}, {:.3f}], direction: [{:.3f}, {:.3f}]".format(n_iter, *xk, *pk))

            alpha, fc, gc, new_fval, old_fval, new_slope = line_search(f=self.F, myfprime=self.dF, xk=xk, pk=pk, maxiter=50)

            if alpha is None:
                print("[W] Search direction is not a descent direction.")
                break

            # get x_last, p_last
            x_last = xk + alpha * pk
            p_last = -new_slope # descent direction

            # refine x_last, p_last and new_fval: projection to [0, 1]
            eps = np.finfo(np.float64).eps
            x_last[x_last <= 0 + eps] = 0 + eps
            x_last[x_last >= 1 - eps] = 1 - eps
            p_last = -self.dF(x_last)
            new_fval = self.F(x_last)

            # update u, v
            self.u, self.v = x_last

            # measurements
            diff = np.abs(new_fval - old_fval) # the difference of function value
            # diff = np.sqrt(np.sum((alpha * pk) ** 2)) # the difference of threshold
            
            self.print_msg("    Wolfe line search iter       : {}".format(n_iter))
            self.print_msg("    num of function evals        : {}".format(fc))
            self.print_msg("    num of gradient evals        : {}".format(gc))
            self.print_msg("    function value update        : {:.3f} -> {:.3f}".format(old_fval, new_fval))
            self.print_msg("    threshold update             : [{:.3f}, {:.3f}] -> [{:.3f}, {:.3f}]".format(*xk, *x_last))
            self.print_msg("    threshold update direction   : [{:.3f}, {:.3f}]".format(*(alpha * pk)))
            self.print_msg("    threshold difference         : {:.6f}".format(diff))

            # evaluate
            self.X_pd = get_prediction_with_threshold(U=self.U, V=self.V, u=self.u, v=self.v)
            self.evaluate(df_name='updates', head_info={'iter': n_iter, 'u': self.u, 'v': self.v, 'F': new_fval})

            # display
            if self.verbose and self.display and n_iter % 10 == 0:
                self.show_matrix(u=self.u, v=self.v, title=f"iter {n_iter}")

            # early stop detection
            is_improving = self.early_stop(n_iter=n_iter, diff=diff)
    

    @ignore_warnings
    def F(self, params):
        '''The objective function.
        Parameters
        ----------
        params : [u, v]

        Returns
        -------
        F : F(u, v)
        '''
        u, v = params

        U = sigmoid(subtract(self.U, u) * self.lamda)
        V = sigmoid(subtract(self.V, v) * self.lamda)

        diff = self.X_train - U @ V.T
        F = 0.5 * np.sum(power(multiply(self.W, diff), 2))
        return F
    

    @ignore_warnings
    def dF(self, params):
        '''The gradient of the objective function.

        Parameters
        ----------
        params : [u, v]

        Returns
        -------
        dF : [dF(u, v)/du, dF(u, v)/dv], the ascend direction
        '''
        u, v = params
        
        U = sigmoid(subtract(self.U, u) * self.lamda)
        V = sigmoid(subtract(self.V, v) * self.lamda)
        
        X_gt = self.X_train
        X_pd = U @ V.T

        dFdX = multiply(self.W, X_gt - X_pd)

        dFdU = dFdX @ V
        dUdu = self.dXdx(self.U, u)
        dFdu = multiply(dFdU, dUdu) # (m, k)

        dFdV = U.T @ dFdX
        dVdv = self.dXdx(self.V, v)
        dFdv = multiply(dFdV, dVdv.T) # (k, n)

        dF = np.array([np.sum(dFdu), np.sum(dFdv)])
        return dF


    # @ignore_warnings
    def dXdx(self, X, x):
        '''The fractional term in the gradient.

                      dU*     dV*     dW*     dH*
        This computes --- and --- (or --- and --- as in the paper).
                      du      dv      dw      dh
        
        Parameters
        ----------
        X : X*, sigmoid(X - x) in the paper
        '''
        diff = subtract(X, x)
        num = np.exp(-self.lamda * subtract(X, x)) * self.lamda
        denom_inv = sigmoid(diff * self.lamda) ** 2

        return num * denom_inv