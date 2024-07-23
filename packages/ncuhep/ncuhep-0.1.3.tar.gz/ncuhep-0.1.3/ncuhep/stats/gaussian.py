import numpy as np
import matplotlib.pyplot as plt 
from .histogram import Histogram
from iminuit import Minuit
from iminuit.cost import LeastSquares


def model(x, mu, sigma):
    return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

class Gaussian(Histogram):
    def __init__(self, sample, bin_size, confidence_level=0.95):
        super().__init__(sample, bin_size, confidence_level)
        self.sample_size = len(self.sample)
        
    def fit(self):
        min_fval = None
        m_min = None
        for _ in range(1000):
            lsq = LeastSquares(self.x, self.y, self.e, model)
            m = Minuit(lsq, mu=np.random.normal(1, 0.1) * np.mean(self.sample), sigma=np.random.normal(1, 0.1) * np.std(self.sample))
            
            m.migrad()
            m.hesse()

            if min_fval is None or m.fval < min_fval:
                min_fval = m.fval
                m_min = m
        m = m_min
        
        self.mu = m.values['mu']
        self.sigma = m.values['sigma']
        self.mu_error = m.errors['mu']
        self.sigma_error = m.errors['sigma']
        self.chi2 = m.fval / (len(self.x) - len(m.values))
        self.ndof = len(self.x) - len(m.values)
        
        
    def plot(self):
        plt.rcParams["font.family"] = "monospace"
        fit_info = [
            f'$\chi^2$\t      ${self.chi2:.3f}$',
            f'Mean \t\t${self.mu:.3E} \pm {self.mu_error:.2E}$',
            f'Std. Dev. \t${self.sigma:.3E} \pm {self.sigma_error:.2E}$'
        ]
        
        plt.errorbar(self.x, self.y, yerr=self.e, fmt='o', label='Data', zorder=1, color='black')
        plt.plot(self.x, model(self.x, self.mu, self.sigma), label='Fit', zorder=2, color='black', linestyle='--', linewidth=2)
        
        plt.legend(title='\n'.join(fit_info))
        plt.show()
        
   
sample = np.random.normal(0, 12, 10000)
g = Gaussian(sample, 1, 0.95)
g.fit()
g.plot()


