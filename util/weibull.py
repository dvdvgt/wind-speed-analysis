import numpy as np
import scipy
import scipy.optimize
import scipy.special
import functools
import math

class Weibull:
    # https://en.wikipedia.org/wiki/Weibull_distribution
    
    def __init__(self, lambd: float, k: float):
        """
        lambd: scale parameter in (0, infinity)
        k: shape parameter in (0, infinity)
        """
        self.lambd = lambd
        self.k = k

    def pdf(self, X: np.ndarray) -> np.ndarray:
        """
        The probability density function of the Weibull distribution.
        """
        # only consider values > 0 and set rest to zero
        result = np.zeros_like(X)
        non_negative_indices = X > 0
        non_negatives = X[non_negative_indices]
        result[non_negative_indices] = self.k / self.lambd * (non_negatives / self.lambd) ** (self.k - 1) * np.exp(- (non_negatives / self.lambd) ** self.k)
        return result

    def cdf(self, X: np.ndarray) -> np.ndarray:
        """
        The cummulative probability density function of the Weibull distribution.
        """
        # only consider values > 0 and set rest to zero
        result = np.zeros_like(X)
        non_negative_indices = X > 0
        non_negatives = X[non_negative_indices]
        result[non_negative_indices] = 1 - np.exp(- (non_negatives / self.lambd) ** self.k)
        return result
    
    def n_raw_moment(self, n=1):
        # https://proofwiki.org/wiki/Raw_Moment_of_Weibull_Distribution
        return self.lambd ** n * scipy.special.gamma(1 + n / self.k)
        
    @functools.cached_property
    def mode(self):
        return 0 if self.k <= 1 else self.lambd * ((self.k - 1) / self.k) ** (1 / self.k)

    @functools.cached_property
    def median(self):
        return self.lambd * scipy.special.gamma(1 + 1 / self.k)
    
    def ml_lambda(X: np.ndarray, beta: float) -> float:
        """
        Compute the scale parameter lambda using the maximum likelihood method given a fixed beta.
        """
        assert(len(X[X < 0]) > 0, "invalid input")
        N = X.shape[0]
        return (1 / N * np.sum(X ** beta)) ** (1 / beta)

    def ml_beta(X: np.ndarray) -> float:
        """
        Compute the shape parameter beta using the maximum likelihood method.
        """
        assert(len(X[X < 0]) > 0, "invalid input")
        N = X.shape[0]
        l_fn = lambda beta: - 1 / N * np.sum(np.log(X)) - 1 / beta + np.sum(X ** beta * np.log(X)) / np.sum(X ** beta)
        return scipy.optimize.root(l_fn, 2.0)

    def estimate(X: np.ndarray):
        """
        Estimate the parameters of the Weibull distribution using the Maximum Likelihood Method.
        """
        # only consider positive values for the ML-estimation (log is only defined for positive numbers)
        X = X[X > 0]
        b = Weibull.ml_beta(X).x
        l = Weibull.ml_lambda(X, b)
        return Weibull(l, b)