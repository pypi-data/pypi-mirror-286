# Approximation Package
## Project Motivation
Summing two random variables and fitting them into a suitable distribution is often a challenging task. One well-known distribution that is difficult to sum exactly is the lognormal distribution. Many mathematicians have addressed this problem and developed approximation methods, even though an exact distribution may not be possible.

The creation of this package is inspired by the idea of encapsulating these approximation methods in a Python package while maintaining the user-friendly nature of the Python language. I started with two well-known approximation methods: Fenton-Wilkinson (1) and Schwartz-Yeh (2).

Additionally, I have included two simple functions: one for summing normal distributions and another for obtaining the distribution of the difference between two normal distributions. Another function is available to create a random sample using the Monte Carlo method for summed distributions.

The aim is to extend the package with methods from the literature that approximate combined distributions. This will allow users to easily apply these approximation methods without needing a complete understanding of the underlying techniques or the necessity of hard-coding.
## Install
### Dependencies
1. __*scipy*__ package is utilized to define the distributions.
1. __*math*__ package is required for the calculations.
1. __*random*__ package is used to generate random samples.
### User installation
* pip install Approximation
## File Descriptions
* **setup.py**
* **test.py**
* **lognormalApproximations.py** : Appromation methods for the summation of two random variables coming from lognormal distributions.
* **normalSummation.py** : Function that contains operations among random variables coming from normal distributions
* **validation.py** : Functions regarding to validate approximation methods
## Available Functions
### Fenton-Wilkinson Approximation
(1) Fenton, L. (1960). The sum of log-normal probability distributions in scatter transmission systems. *IRE Transactions on communications systems, 8(1)*, 57-67.

The famous Fenton-Wilkinson approximation assumes that the first and second moments of the concatenated distribution are equal to the sum of the moments of the individual distributions. This function allows lognormal distributions from the **scipy.stats** package. It returns a **scipy.stats.lognorm** object, which represents the Fenton-Wilkinson approximated distribution for the summation of the given distributions.

**INPUT**
* distributions (scipy.stats.lognorm)
**OUTPUT**
* approximated lognormal distribution (scipy.stats.lognorm)
**USAGE**
* from Approximation import FentonWilkinson
* distribution1 = lognormal(1,2)
* distribution2 = lognorm(s=0.4,loc=0,scale=math.exp(1.2))
* ...
* approximated_distribution = FentonWilkinson(distribution1, distribution2, ...)
### Schwartz-Yeh Approximation (with table)
(2) Schwartz, S. C., & Yeh, Y. S. (1982). On the distribution function and moments of power sums with log‐normal components. *Bell System Technical Journal, 61(7)*, 1441-1462.
Famous Schwartz-Yeh approximation focuses on exact expressions for the moments with two components. An iterative approach is used when there are more than two components. While calculating the moments of the log of summed random variables, the expressions become two-parameter functions. Therefore, Schwartz and Yeh also provided two tables for a certain range of Gaussian random variable values to facilitate the calculation of the output of related functions without complex limit and convergence analysis. This function allows lognormal distributions from the **scipy.stats** package. It returns a **scipy.stats.lognorm** object, which represents the Schwartz-Yeh approximated distribution for the summation of the given distributions.
**INPUT**
* distributions (scipy.stats.lognorm)
**OUTPUT**
* approximated lognormal distribution (scipy.stats.lognorm)
**USAGE**
* from Approximation import SchwartzYeh_tabular
* distribution1 = lognormal(1,2)
* distribution2 = lognorm(s=0.4,loc=0,scale=math.exp(1.2))
* ...
* approximated_distribution = SchwartzYeh_tabular(distribution1, distribution2, ...)
### Sum of Normal Distributions
Even though, the sum of normal distributions is an easy task, we provided this function to ensure the completeness of the package. 
**INPUT**
* distributions (scipy.stats.norm)
**OUTPUT**
* approximated lognormal distribution (scipy.stats.norm)
**USAGE**
* from Approximation import sumNormalDistributions
* distribution1 = normal(1,2)
* distribution2 = norm(loc=0,1.2)
* ...
* summed_distribution = sumNormalDistributions(distribution1, distribution2, ...)
### Subtraction of Two Normal Distributions
The same summation approach is used when targeting the subtraction of two normally distributed random variables, with the simple assumption of multiplying the subtracted distribution by -1.
**INPUT**
* distributions (scipy.stats.norm)
**OUTPUT**
* approximated lognormal distribution (scipy.stats.norm)
**USAGE**
* from Approximation import subtractNormalDistributions
* diminishing_distribution = normal(1,2)
* subtracted_distribution = norm(loc=0,1.2)
* ...
* subtracted_distribution = subtractNormalDistributions(diminishing_distribution, subtracted_distribution)
### CreateRandomSumDistributions
This function provides a sample for the summation of random variables originating from the given distributions.
**INPUT**
* distributions (scipy.stats._distn_infrastructure.rv_continuous_frozen)
* size: number of points to be created
**OUTPUT**
* a python list that contains sample for the summation of input distributions
**USAGE**
* from Approximation import CreateRandomSumDistributions
* dist1 = norm(1,2)
* dist2 = lognorm(loc=0,1.2)
* ...
* sample = sumNormalDistributions(dist1, dist2, ..., size=1000)
# Licenses and Acknowledgements
This project provides ready-to-go approximation methods for users. The approximation methods themselves were not developed by the creators of this package. Instead, the implementation of these methods has been done by the project owner. All references for the methods are provided within this README file. Only the implementation of these methods is licensed by the project owner, as specified in the license file.

I am profoundly grateful to all the scientists whose groundbreaking contributions in this field have inspired me to develop this package. Their work has been invaluable in my research projects and has made it possible to bring these advanced approximation methods to a wider audience.


