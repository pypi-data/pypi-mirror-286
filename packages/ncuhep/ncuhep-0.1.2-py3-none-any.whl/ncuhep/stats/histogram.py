import numpy as np
import scipy.stats as stats


class Histogram:
    def __init__(self, sample, bin_size, confidence_level=0.95):
        self.sample = sample
        self.bin_size = bin_size
        self.confidence_level = confidence_level
        self.bins = int((np.amax(sample) - np.amin(sample)) // bin_size + 1)
        self.__min = np.amin(sample) // bin_size - 1
        self.__shift = self.__min * bin_size + bin_size / 2
        self.__shifted_sample = sample - self.__shift
        self._x, self._y = self.__bin(self.__shifted_sample, bin_size, self.bins)

    def __bin(self, sample, bin_size, bins):
        assert bin_size > 0
        assert bins > 0
        assert type(bins) == int
        assert type(bin_size) in [int, float]

        x = np.linspace(0, bins * bin_size, bins + 1, endpoint=True)
        y = np.zeros(bins + 1)

        for s in sample:
            index = int((s // bin_size))
            if index >= bins:  # Ensure index is within bounds
                index = bins - 1
            y[index] += 1

        return x, y


    @property
    def x(self):
        return self._x + self.__shift + self.bin_size / 2

    @property
    def y(self):
        return self._y / (np.sum(self._y) * self.bin_size)
    
    @property
    def e(self):
        return self.error_estimate(self._y) / (np.sum(self._y) * self.bin_size)
                                       
    @property
    def counts(self):
        return self._y

    @property
    def counts_error(self):
        return self.error_estimate(self._y)
    
    def poisson_confidence_interval(self, k):
        alpha = 1 - self.confidence_level
        lower_bound = 0.5 * stats.chi2.ppf(alpha / 2, 2 * k)
        upper_bound = 0.5 * stats.chi2.ppf(1 - alpha / 2, 2 * (k + 1))
        
        if type(k) == np.ndarray:
            lower_bound[k == 0] = 0
        return lower_bound, upper_bound
    
    def error_estimate(self, k):
        lower_bound, upper_bound = self.poisson_confidence_interval(k)
        return (upper_bound - lower_bound) / 2
    
