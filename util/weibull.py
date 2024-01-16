import numpy as np
import scipy
import scipy.optimize
import scipy.special
import functools
import math

class Weibull:
    # https://en.wikipedia.org/wiki/Weibull_distribution
    
    def __init__(self, lambd: float, beta: float): # both parameters should be >0
        """
        lambd: scale parameter in (0, infinity)
        k: shape parameter in (0, infinity)
        """
        self.lambd = lambd
        self.beta = beta 

    
    def __repr__(self):  
        return " Weibull distr for lambda=% s, beta=% s \n " % (self.lambd, self.beta)
    

    def pdf(self, X: np.ndarray) -> np.ndarray:
        """
        The probability density function of the Weibull distribution.
        """
        # only consider values > 0 and set rest to zero
        result = np.zeros_like(X)
        non_negative_indices = X > 0
        non_negatives = X[non_negative_indices]
        result[non_negative_indices] = self.beta / self.lambd * (non_negatives / self.lambd) ** (self.beta - 1) * np.exp(- (non_negatives / self.lambd) ** self.beta)
        return result

    def cdf(self, X: np.ndarray) -> np.ndarray:
        """
        The cummulative probability density function of the Weibull distribution.
        """
        # only consider values > 0 and set rest to zero
        result = np.zeros_like(X)
        non_negative_indices = X > 0
        non_negatives = X[non_negative_indices]
        result[non_negative_indices] = 1 - np.exp(- (non_negatives / self.lambd) ** self.beta)
        return result
    
    def n_raw_moment(self, n=1):
        # https://proofwiki.org/wiki/Raw_Moment_of_Weibull_Distribution
        return self.lambd ** n * scipy.special.gamma(1 + n / self.beta)
        
    @functools.cached_property
    def mode(self):
        return 0 if self.k <= 1 else self.lambd * ((self.k - 1) / self.beta) ** (1 / self.beta)

    @functools.cached_property
    def median(self):
        return self.lambd * scipy.special.gamma(1 + 1 / self.k)
    
    def ml_lambda(X: np.ndarray, beta: float) -> float:
        """
        Compute the scale parameter lambda using the maximum likelihood method given a fixed beta.
        """
        assert len(X[X > 0]) > 0, "invalid input"
        N = X.shape[0]
        return (1 / N * np.sum(X ** beta)) ** (1 / beta)

    def ml_beta(X: np.ndarray) -> float:
        """
        Compute the shape parameter beta using the maximum likelihood method.
        """
        assert len(X[X > 0]) > 0, "invalid input"
        N = X.shape[0]
        l_fn = lambda beta: - 1 / N * np.sum(np.log(X)) - 1 / beta + np.sum(X ** beta * np.log(X)) / np.sum(X ** beta)
        return scipy.optimize.root(l_fn, 2.0)

    def estimate(X: np.ndarray):
        """
        Estimate the parameters of the Weibull distribution using the Maximum Likelihood Method.
        """
        # only consider positive values for the ML-estimation (log is only defined for positive numbers)
        X = X[X > 0]
        X= X[~np.isnan(X)]

        #assert len(X) > 0, "invalid input"
        # exception if no data is available for computation
        
        try:
            b = Weibull.ml_beta(X).x.item()
            l = Weibull.ml_lambda(X, b).item()
        except Exception:
            b=-999
            l=-999
        finally:
        
            return Weibull(l, b)
       
    
    
    def graphical_parameters(X: np.ndarray): 
        '''
        Compute the parameters of the weibull distribution with the graphical method 
        '''
        max_included_windspeed=int(np.nanmax(X)+1)
        number_of_bins=1000
        edges=np.linspace(0,max_included_windspeed, number_of_bins)
        #Start by computing the empirical CDF:
        empiric_pdf= np.histogram(X, bins=edges)[0]
        CDF=np.array([empiric_pdf[0]])
        for i in range(1, len(empiric_pdf)):
            CDF=np.append(CDF, CDF[i-1]+empiric_pdf[i] )
        
        # disregard the first d  bins? -> This makes sure we have no near-constant part in the beginning
        d=0
        for i in range(0, len(CDF)):
            d=i
            if CDF[i] >0.1:
                break

        edges=edges[d:]
        empiric_pdf=empiric_pdf[d:]
        CDF=CDF[d:]

        #normalize the CDF and the PDF
        empiric_pdf=(empiric_pdf/CDF[len(CDF)-1])
        CDF=CDF/CDF[len(CDF)-1]

        # transform the axes of the CDF in order to find the Weibull parameters
        mod_CDF= np.log(-np.log(1-CDF[1:] +0.000001) +0.000001) # HOW TO RESOLVE THIS PROPERLY?
        log_edges=np.log(edges[2:])

         # now do linear regression
        linpol=np.polyfit(log_edges, mod_CDF, 1)
        mod_CDF_model = np.poly1d(linpol)
        b=linpol[0]
        l=np.exp( - linpol[1]/linpol[0])
        return [l,b]
    
    

    def graphical_estimate(X: np.ndarray):
        """
        Estimate the parameters of the Weibull distribution using the Graphical Method.
        """
        # only consider positive values for the ML-estimation (log is only defined for positive numbers)
        X= X[X > 0]
        X= X[~np.isnan(X)]

        #assert len(X) > 0, "invalid input"
        # exception if no data is available for computation
        try:
            params=Weibull.graphical_parameters(X)
        except Exception: 
            params=[-999, -999]
        finally:
            l=params[0]
            b=params[1]
            return Weibull(l,b)
    
arr=np.array([2,2,3])

print(Weibull.graphical_estimate(arr))