from scipy.stats import norm


def sumNormalDistributions(*distributions):
    """
    This function give the distribution of random variables which the sum of a set of random variables coming from normal distributions
    INPUT:
        - *distribution: normal distributions to be summed up(scipy.stats.norm)
    OUTPUT:
        - Normal distribution of summed values
    """
    for dist in distributions:
        if not isinstance(dist, type(norm())):
            raise TypeError

    return norm(sum([dist.mean() for dist in distributions]), sum([dist.var() for dist in distributions]) ** (1/2))


def subtractNormalDistributions(dist1, dist2):
    """
    This function give the distribution of random variables which the subtract of a two of random variables coming from normal distributions
    The second distribution is subtracted from the first one.
    INPUT:
        - dist1: the diminishing normal distribution (scipy.stats.norm)
        - dist2: the subtracted normal distribution (scipy.stats.norm)
    OUTPUT:
        - Normal distribution of extracted values
    """
    for dist in [dist1, dist2]:
        if not isinstance(dist, type(norm())):
            raise TypeError

    return norm(dist1.mean()-dist2.mean(), sum(dist1.var()+dist2.var()) ** (1/2))

