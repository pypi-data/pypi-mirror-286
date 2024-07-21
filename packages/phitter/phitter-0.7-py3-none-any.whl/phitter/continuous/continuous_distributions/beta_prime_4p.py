import warnings

import numpy
import scipy.optimize
import scipy.special
import scipy.stats

warnings.filterwarnings("ignore")


class BETA_PRIME_4P:
    """
    Beta Prime 4P Distribution
    Parameters BETA_PRIME_4P distribution: {"alpha": *, "beta": *, "loc": *, "scale": *}
    https://phitter.io/distributions/continuous/beta_prime_4p
    """

    def __init__(
        self,
        parameters: dict[str, int | float] = None,
        continuous_measures=None,
        init_parameters_examples=False,
    ):
        """
        Initializes the BETA_PRIME_4P distribution by either providing a Continuous Measures instance [CONTINUOUS_MEASURES] or a dictionary with the distribution's parameters.
        Parameters BETA_PRIME_4P distribution: {"alpha": *, "beta": *, "loc": *, "scale": *}
        https://phitter.io/distributions/continuous/beta_prime_4p
        """
        if continuous_measures is None and parameters is None and init_parameters_examples == False:
            raise ValueError(
                "You must initialize the distribution by providing one of the following: distribution parameters, a Continuous Measures [CONTINUOUS_MEASURES] instance, or by setting init_parameters_examples to True."
            )
        if continuous_measures != None:
            self.parameters = self.get_parameters(continuous_measures=continuous_measures)
        if parameters != None:
            self.parameters = parameters
        if init_parameters_examples:
            self.parameters = self.parameters_example

        self.alpha = self.parameters["alpha"]
        self.beta = self.parameters["beta"]
        self.loc = self.parameters["loc"]
        self.scale = self.parameters["scale"]

    @property
    def name(self):
        return "beta_prime_4p"

    @property
    def parameters_example(self) -> dict[str, int | float]:
        return {"alpha": 911, "beta": 937, "loc": -7, "scale": 125}

    def cdf(self, x: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Cumulative distribution function
        """
        result = scipy.stats.betaprime.cdf(x, self.alpha, self.beta, loc=self.loc, scale=self.scale)
        # z = lambda t: (t - self.loc) / self.scale
        # result = scipy.special.betainc(self.alpha, self.beta, z(x) / (1 + z(x)))
        return result

    def pdf(self, x: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Probability density function
        """
        result = scipy.stats.betaprime.pdf(x, self.alpha, self.beta, loc=self.loc, scale=self.scale)
        # z = lambda t: (t - self.loc) / self.scale
        # result = (1 / self.scale) * (z(x) ** (self.alpha - 1) * (1 + z(x)) ** (-self.alpha - self.beta)) / (scipy.special.beta(self.alpha,self.beta))
        return result

    def ppf(self, u: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Percent point function. Inverse of Cumulative distribution function. If CDF[x] = u => PPF[u] = x
        """
        result = scipy.stats.betaprime.ppf(u, self.alpha, self.beta, loc=self.loc, scale=self.scale)
        # result = self.loc + (self.scale * scipy.special.betaincinv(self.alpha, self.beta, u)) / (1 - scipy.special.betaincinv(self.alpha, self.beta, u))
        return result

    def sample(self, n: int, seed: int | None = None) -> numpy.ndarray:
        """
        Sample of n elements of ditribution
        """
        if seed:
            numpy.random.seed(seed)
        return self.ppf(numpy.random.rand(n))

    def non_central_moments(self, k: int) -> float | None:
        """
        Parametric no central moments. µ[k] = E[Xᵏ] = ∫xᵏ∙f(x) dx
        """
        return (scipy.special.gamma(k + self.alpha) * scipy.special.gamma(self.beta - k)) / (scipy.special.gamma(self.alpha) * scipy.special.gamma(self.beta))

    def central_moments(self, k: int) -> float | None:
        """
        Parametric central moments. µ'[k] = E[(X - E[X])ᵏ] = ∫(x-µ[k])ᵏ∙f(x) dx
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        µ3 = self.non_central_moments(3)
        µ4 = self.non_central_moments(4)

        if k == 1:
            return 0
        if k == 2:
            return µ2 - µ1**2
        if k == 3:
            return µ3 - 3 * µ1 * µ2 + 2 * µ1**3
        if k == 4:
            return µ4 - 4 * µ1 * µ3 + 6 * µ1**2 * µ2 - 3 * µ1**4

        return None

    @property
    def mean(self) -> float:
        """
        Parametric mean
        """
        µ1 = self.non_central_moments(1)
        return self.loc + self.scale * µ1

    @property
    def variance(self) -> float:
        """
        Parametric variance
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        return self.scale**2 * (µ2 - µ1**2)

    @property
    def standard_deviation(self) -> float:
        """
        Parametric standard deviation
        """
        return numpy.sqrt(self.variance)

    @property
    def skewness(self) -> float:
        """
        Parametric skewness
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        std = numpy.sqrt(µ2 - µ1**2)
        central_µ3 = self.central_moments(3)
        return central_µ3 / std**3

    @property
    def kurtosis(self) -> float:
        """
        Parametric kurtosis
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        std = numpy.sqrt(µ2 - µ1**2)
        central_µ4 = self.central_moments(4)
        return central_µ4 / std**4

    @property
    def median(self) -> float:
        """
        Parametric median
        """
        return self.ppf(0.5)

    @property
    def mode(self) -> float:
        """
        Parametric mode
        """
        return self.loc + (self.scale * (self.alpha - 1)) / (self.beta + 1)

    @property
    def num_parameters(self) -> int:
        """
        Number of parameters of the distribution
        """
        return len(self.parameters)

    def parameter_restrictions(self) -> bool:
        """
        Check parameters restrictions
        """
        v1 = self.alpha > 0
        v2 = self.beta > 0
        v3 = self.scale > 0
        return v1 and v2 and v3

    def get_parameters(self, continuous_measures) -> dict[str, float | int]:
        """
        Calculate proper parameters of the distribution from sample continuous_measures.
        The parameters are calculated by solving the equations of the measures expected
        for this distribution.The number of equations to consider is equal to the number
        of parameters.

        Parameters
        ==========
        continuous_measures: MEASUREMESTS
            attributes: mean, std, variance, skewness, kurtosis, median, mode, min, max, size, num_bins, data

        Returns
        =======
        parameters: {"alpha": *, "beta": *, "loc": *, "scale": *}
        """

        ## In this distribution solve the system is best than scipy estimation.
        def equations(initial_solution: tuple[float], continuous_measures) -> tuple[float]:
            alpha, beta, loc, scale = initial_solution

            parametric_mean = scale * alpha / (beta - 1) + loc
            parametric_variance = (scale**2) * alpha * (alpha + beta - 1) / ((beta - 1) ** 2 * (beta - 2))
            # parametric_skewness = 2 * numpy.sqrt(((beta - 2)) / (alpha * (alpha + beta - 1))) * (((2 * alpha + beta - 1)) / (beta - 3))
            parametric_median = loc + scale * scipy.stats.beta.ppf(0.5, alpha, beta) / (1 - scipy.stats.beta.ppf(0.5, alpha, beta))
            parametric_mode = scale * (alpha - 1) / (beta + 1) + loc

            eq1 = parametric_mean - continuous_measures.mean
            eq2 = parametric_variance - continuous_measures.variance
            # eq3 = parametric_skewness - continuous_measures.skewness
            eq3 = parametric_median - continuous_measures.median
            eq4 = parametric_mode - continuous_measures.mode

            return (eq1, eq2, eq3, eq4)

        scipy_parameters = scipy.stats.betaprime.fit(continuous_measures.data_to_fit)
        try:
            x0 = (continuous_measures.mean, continuous_measures.mean, continuous_measures.min, scipy_parameters[3])
            bounds = ((0, 0, -numpy.inf, 0), (numpy.inf, numpy.inf, numpy.inf, numpy.inf))
            args = [continuous_measures]
            solution = scipy.optimize.least_squares(equations, x0=x0, bounds=bounds, args=args)
            parameters = {"alpha": solution.x[0], "beta": solution.x[1], "loc": solution.x[2], "scale": solution.x[3]}
        except:
            parameters = {"alpha": scipy_parameters[0], "beta": scipy_parameters[1], "loc": scipy_parameters[2], "scale": scipy_parameters[3]}

        return parameters


if __name__ == "__main__":
    import sys

    sys.path.append("../")
    from continuous_measures import CONTINUOUS_MEASURES

    ## Import function to get continuous_measures
    def get_data(path: str) -> list[float]:
        sample_distribution_file = open(path, "r")
        data = [float(x.replace(",", ".")) for x in sample_distribution_file.read().splitlines()]
        sample_distribution_file.close()
        return data

    ## Distribution class
    path = "../continuous_distributions_sample/sample_beta_prime_4p.txt"
    data = get_data(path)
    continuous_measures = CONTINUOUS_MEASURES(data)
    distribution = BETA_PRIME_4P(continuous_measures=continuous_measures)

    print(f"{distribution.name} distribution")
    print(f"Parameters: {distribution.parameters}")
    print(f"CDF: {distribution.cdf(continuous_measures.mean)} {distribution.cdf(numpy.array([continuous_measures.mean, continuous_measures.mean]))}")
    print(f"PDF: {distribution.pdf(continuous_measures.mean)} {distribution.pdf(numpy.array([continuous_measures.mean, continuous_measures.mean]))}")
    print(f"PPF: {distribution.ppf(0.5)} {distribution.ppf(numpy.array([0.5, 0.5]))} - V: {distribution.cdf(distribution.ppf(0.5))}")
    print(f"SAMPLE: {distribution.sample(5)}")
    print(f"\nSTATS")
    print(f"mean: {distribution.mean} - {continuous_measures.mean}")
    print(f"variance: {distribution.variance} - {continuous_measures.variance}")
    print(f"skewness: {distribution.skewness} - {continuous_measures.skewness}")
    print(f"kurtosis: {distribution.kurtosis} - {continuous_measures.kurtosis}")
    print(f"median: {distribution.median} - {continuous_measures.median}")
    print(f"mode: {distribution.mode} - {continuous_measures.mode}")
