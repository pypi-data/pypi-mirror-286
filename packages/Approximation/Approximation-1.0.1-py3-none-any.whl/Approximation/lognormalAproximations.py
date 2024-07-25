from scipy.stats import lognorm, norm
import math

def _get_mu(dist):
        if len(dist.args) >= 3:
            return math.log(dist.args[2])
        else:
            return math.log(dist.kwds.get('scale',1))
        
def _get_loc(dist):
    if len(dist.args) >= 2:
        return dist.args[1]
    else:
        return dist.kwds.get('loc',0)
    
def _get_sigma(dist):
    if len(dist.args) >= 1:
        return dist.args[0]
    else:
        return dist.kwds['s']


def FentonWilkinson(*distributions):
    """
    Famous Fenton-Wilkinson approximation
    It assumes first and second moments of the concenated distribution equals to 
    sum of moments of child distribution.
    This function allows lognorm distributions from scipy.stats package
    It returns scipy.stats.lognorm object which is Fenton-Wilkinson approximated 
    distribution for summation of given distributions.
    INPUT:
        - *distribution: lognormal distributions to be summed up(scipy.stats.lognorm)
    OUTPUT:
        - approximated_distribution
    """
    for dist in distributions:
        if not isinstance(dist, type(lognorm(1,1))):
            raise TypeError
            
    if len(distributions) == 1:
        return distributions[0]
    expected_mean = sum([s.mean() for s in distributions])
    expected_var = sum([s.var() for s in distributions])
    th = sum([s.support()[0] for s in distributions])   
    sigma = math.sqrt(math.log((expected_var/(expected_mean-th)**2)+1))
    mu = math.log(expected_mean-th) - sigma*sigma/2
    return lognorm(s=sigma,loc=th,scale=math.exp(mu))


def SchwartzYeh_tabular(*distributions):
    """
    Famous Schwatrz-Yeh approximation
    It assumes first and second moments of the concenated distribution equals to 
    sum of moments of child distribution.
    This function allows lognorm distributions from scipy.stats package
    It returns scipy.stats.lognorm object which is Fenton-Wilkinson approximated 
    distribution for summation of given distributions.
    INPUT:
        - *distribution: lognormal distributions to be summed up(scipy.stats.lognorm)
    OUTPUT:
        - approximated_distribution
    """
    def _SchwartzYeh_table():
        global region1, region2

        region1 = dict()
        region1[1] = [-0.1153239, -5.667912, 11.51279, -7.162489, 1.312986],\
                        [-0.1611385, 20.84215, -44.99768, 27.5621, -5.109783],\
                        [0.1345124, -26.70183, 59.19191, -36.95334, 6.912766],\
                        [0.08057054, 14.29709, -32.25969, 20.55628, -3.888684],\
                        [-0.03145306, -2.730047, 6.244253, -4.048245, 0.7746786]
        
        region1[2] = [0.04012876, -4.483259, 7.39176, -3.77219, 0.5262268],\
                        [-1.579114, 16.37249, -29.94901, 13.37812, -1.747459],\
                        [2.174588, -21.14152, 39.76749, -17.7689, 2.195322],\
                        [-0.7525302, 11.47157, -21.89501, 10.06767, -1.224983],\
                        [0.08447987, -2.222839, 4.289557, -2.035757, 0.2499568]
        
        region1[3] = [-3.958699, -5.454983, 11.3928, -7.116366, 1.315218],\
                        [6.839918, 19.62529, -43.14091, 26.47795, -4.940592],\
                        [-4.717296, -24.86802, 56.18572, -35.01815, 6.560938],\
                        [1.81936, 13.23538, -30.50022, 19.37757, -3.658379],\
                        [-0.2817493, -2.518272, 5.893337, -3.809492, 0.7260144]

        region2 = dict()
        region2[1] = [-335.4792, 528.123, -308.5414, 78.95054, -7.518427], \
                        [1354.559, -2133.838, 1245.491, -319.1052, 30.36738],\
                        [-1865.732, 2941.369, -1718.295, 440.3198, -41.88256],\
                        [1059.09, -1671.264, 977.6851, -250.7169, 23.84698],\
                        [-212.1206, 335.0888, -196.3238, 50.40234, -4.79598]
        
        region2[2] = [89.42737, -152.1976, 97.34654, -27.44724, 2.756644],\
                        [-368.8427, 628.7175, -407.7784, 114.8104, -11.61187],\
                        [496.6108, -851.4775, 557.4036, -158.8548, 16.24075],\
                        [-268.4747, 463.8312, -306.1915, 88.42364, -9.152624],\
                        [50.77676, -88.3302, 58.76009, -17.17538, 1.799387]
        
        region2[3] = [-359.6955, 557.6596, -324.2909, 82.71772, -7.863267],\
                        [1443.269, -2250.748, 1307.118, -333.6339, 31.67827],\
                        [-1986.007, 3106.047, -1804.377, 460.3419, -43.66067],\
                        [1128.759, -1768.423, 1028.409, -262.4284, 24.8749],\
                        [-226.4791, 355.3536, -206.9294, 52.84466, -5.008795]
    
    _SchwartzYeh_table()
    mu_tmp = _get_mu(distributions[0])
    sigma_tmp = _get_sigma(distributions[0])
    th_tmp = _get_loc(distributions[0])

    for dist in distributions[1:]:
        th_tmp += _get_loc(dist)

        if mu_tmp > _get_mu(dist):
            w_m = _get_mu(dist) - mu_tmp #44
            sigma1 = sigma_tmp
            sigma2 = _get_sigma(dist)
        else:
            w_m = mu_tmp - _get_mu(dist) #44
            mu_tmp = _get_mu(dist)
            sigma2 = sigma_tmp
            sigma1 = _get_sigma(dist)
        w_s = math.sqrt(sigma1 ** 2 + sigma2 ** 2) 

        
        if w_s > 15:
            raise "Sigma value of Gaussian random variable is out of range: {w_s}. The Schwartz tables are only valid for sigma values less than 15"
        if w_m < -40:
            raise "Expected value of Gaussian random variable is out of range: {w_m}. The Schwartz tables are only valid for mü values whose absolute value is less than 40"

        if w_m > -20:
            A = region1
        else:
            A = region2
        
        G1_value = 0
        G2_value = 0
        G3_value = 0
        
        for j in range(5):
            for k  in range(5):
                G1_value += A[1][j][k] * w_s ** (j/2) * abs(w_m) ** (k/2) #32
                G2_value += A[2][j][k] * w_s ** (j/2) * abs(w_m) ** (k/2) #32
                G3_value += A[3][j][k] * w_s ** (j/2) * abs(w_m) ** (k/2) #32
        
        G1_value = G1_value ** 10
        G2_value = G2_value ** 10
        G3_value = G3_value ** 10

        mu_tmp += G1_value #49
        sigma_tmp = math.sqrt(abs(sigma1**2 - G1_value ** 2 - 2 * (-sigma1/w_s)**2 * G3_value + G2_value))

    return lognorm(s=sigma_tmp,loc=th_tmp,scale=math.exp(mu_tmp))