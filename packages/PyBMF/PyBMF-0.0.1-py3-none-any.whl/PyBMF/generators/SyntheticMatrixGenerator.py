import numpy as np
from .BaseGenerator import BaseGenerator
from scipy.sparse import lil_matrix


class SyntheticMatrixGenerator(BaseGenerator):
    '''The synthetic Boolean matrix generator.

    This generation procedure is based on the description of PRIMPing paper by Sibylle Hess et al. (2019)
    The scheme is similar to those used by Miettinen and Vreeken (2014); Karaev et al. (2015) and Lucchese et al. (2014)
    '''
    def __init__(self, m, n, k, density=[0.2, 0.2]):
        '''
        Parameters
        ----------
        overlap_flag : bool
            Whether overlap is allowed or not.
        size_range : list of 2 or 4 float
            The lower and upper bounds of factor rectangle size (height_low, height_high, width_low, width_high), 
            or just upper bounds (height_high, width_high).
            The real size limit is the bounds times size m, n divided by k, e.g., [0.2, 2.0] * 1000 / 5.
            Depending on the selection of k, a typical upper size limit is 2.0.
            A complete setting of overlap should hold the format (height_low, height_high, width_low, width_high).
        '''
        super().__init__()
        self.check_params(m=m, n=n, k=k, density=density) # check parameters and print summary

    def generate(self, seed=None):
        self.check_params(seed=seed)
        self.generate_factors()
        self.shuffle() # shuffle factors and multiply
        # self.sorted_index() # todo: get sorted index
        # self.set_factor_info()
        self.to_sparse(type='csr')

    def generate_factors(self):
        self.U = self.generate_factor(self.m, self.k, self.density[0])
        self.V = self.generate_factor(self.n, self.k, self.density[1])

    def generate_factor(self, n, k, density):
        '''Generate a factor matrix

        Parameters
        ----------
        n : int
            Number of rows
        k : int
            Number of columns
        density : float
            Density of 1's on the tail of each column

        Returns
        -------
        array
            The n-by-k factor matrix
        '''        
        X = lil_matrix((n, k))
        l = np.ceil(n / 100).astype(int)
        for c in range(k):
            X[c*l:(c+1)*l, c] = 1
            X[k*l:n, c] = self.rng.binomial(size=n-k*l, n=1, p=density)
        return X
    