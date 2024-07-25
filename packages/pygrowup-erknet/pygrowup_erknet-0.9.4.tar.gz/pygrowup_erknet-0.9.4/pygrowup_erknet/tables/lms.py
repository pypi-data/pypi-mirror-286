from typing import Union

class LMS(object):
    l : float
    m : float
    s : float
    sigma : Union[float, None]

    def __init__(self, l: float, m: float, s: float, sigma : Union[float, None]) -> None:
        self.l = l
        self.m = m
        self. s = s
        self.sigma = sigma