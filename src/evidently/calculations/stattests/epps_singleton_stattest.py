from typing import Tuple

import numpy as np
import pandas as pd
from scipy.stats import epps_singleton_2samp
from scipy.stats import iqr

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _epps_singleton(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Run the Epps-Singleton (ES) test of two samples.
    Args:
        reference_data: reference data
        current_data: current data
        threshold: level of significance (default will be 0.05)
    Returns:
        p_value: p-value based on the asymptotic chi2-distribution.
        test_result: whether the drift is detected
    """
    # raised error if iqr is zero
    iqr_value = iqr(np.hstack((reference_data, current_data)))
    if iqr_value == 0:
        raise ValueError(
            f'{"Epps-Singleton testsinterquartile range (IQR) is zero. IQR of 0 means there is no variability in the middle 50% of your data, but the center of the distribution can be anywhere. Expected: your data sould have higher variability/variance."}'
        )
    p_value = epps_singleton_2samp(reference_data, current_data)[1]
    return p_value, p_value < threshold


epps_singleton_test = StatTest(
    name="es",
    display_name="Epps-Singleton",
    func=_epps_singleton,
    allowed_feature_types=["num"],
    default_threshold=0.05,
)

register_stattest(epps_singleton_test)