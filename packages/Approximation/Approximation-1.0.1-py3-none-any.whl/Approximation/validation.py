import random

def CreateRandomSumDistributions(*distributions, size=1000):
    """
    This function creates random values that comes from the sum of provided distributions
    INPUT
        - *distributions: distribution to sum up (scipy.stats._distn_infrastructure.rv_continuous_frozen)
        - size: number of points
    OUTPUT
        - list of random variables
    """
    sum_values = list()
    for i in range(size):
        tmp_total = 0
        for dist in distributions:
            tmp_total += dist.ppf(random.random())
        sum_values.append(tmp_total)
    return sum_values