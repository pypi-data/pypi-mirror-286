from scipy.stats import ttest_1samp


class OneSampleHypothesisTesting:
    def __init__(self, data: list, population_mean: float, alternative: str = "two-sided", alpha: float = 0.05):

        if len(data) < 2:
            raise Exception("Input data must have at least two data points")

        elif len(set(data)) == 1:
            raise Exception("Input data must not have identical elements")

        else:
            self.data = data

        self.population_mean = population_mean

        self.t_test_results = ttest_1samp(a=self.data, popmean=population_mean, alternative=alternative)

    def calculate_t_statistic(self) -> float:

        t_statistic = self.t_test_results.statistic

        return t_statistic

    def calculate_pvalue(self) -> float:

        p_value = self.t_test_results.pvalue

        return p_value