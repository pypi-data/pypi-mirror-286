import math
from ddsketch import DDSketch

__version__ = "0.1.0"


class StreamingStats:
    GK_MAX_BAND = 999_999

    def __init__(self, epsilon=0.01):
        self.epsilon = epsilon
        self.one_over_2e = 1 / (2 * epsilon)
        self.n = 0
        self.mean = 0.0
        self.M2 = 0.0
        self.min = None
        self.max = None
        self.sum = 0.0
        self.sketch = DDSketch(epsilon)

    def update(self, value):
        self.n += 1
        self.sum += value
        self.delta = value - self.mean
        self.mean += self.delta / self.n
        self.M2 += self.delta * (value - self.mean)
        if self.min is None or self.max is None:
            self.min = value
            self.max = value
        else:
            self.min = min(self.min, value)
            self.max = max(self.max, value)
        self.sketch.add(value)

    def append(self, i):
        self.update(i)

    def __len__(self):
        return self.n

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    def mean(self):
        return self.mean

    def variance(self):
        if self.n <= 1:
            return 0.0
        return self.M2 / (self.n)

    def stddev(self):
        return math.sqrt(self.variance())

    def max(self):
        return self.max

    def min(self):
        return self.min

    def sum(self):
        return self.sum

    def percentile(self, phi):
        return self.sketch.get_quantile_value(phi)

    def quantile(self, phi):
        return self.percentile(phi)

    def dict(self):
        return {
            "n": self.n,
            "mean": self.mean,
            "variance": self.variance(),
            "stddev": self.stddev(),
            "min": self.min,
            "max": self.max,
            "sum": self.sum,
            "1st": self.percentile(0.01),
            "5th": self.percentile(0.05),
            "10th": self.percentile(0.1),
            "25th": self.percentile(0.25),
            "50th": self.percentile(0.5),
            "75th": self.percentile(0.75),
            "90th": self.percentile(0.9),
            "95th": self.percentile(0.95),
            "99th": self.percentile(0.99),
        }


def stats(iterable):
    accumulator = StreamingStats()
    accumulator.extend(iterable)
    return accumulator.dict()
