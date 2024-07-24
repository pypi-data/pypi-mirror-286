from statistics import NormalDist
from typing import Union
from .lms import LMS

normal_dist = NormalDist()

def z_to_percentile(z: Union[float, int]) -> float:
    return normal_dist.cdf(float(z)) * 2.0 - 1.0

def percentile_to_z(percentile: float) -> float:
    return normal_dist.inv_cdf((1.0 + percentile) / 2.0)

def calculate_value_by_percentile(percentile: float, lms: LMS) -> float:
    z = percentile_to_z(percentile)
    return lms.m * (1 + lms.l * lms.s * z) ** (1 / lms.l)
