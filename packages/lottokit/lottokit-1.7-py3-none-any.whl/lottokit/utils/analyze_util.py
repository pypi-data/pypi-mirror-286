#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: analyze_util.py
@DateTime: 2024/7/22 10:11
@SoftWare: PyCharm
"""

from abc import ABC, abstractmethod
from typing import Any


class AnalyzeUtil(ABC):
    """
    Analyze based on multiple data
    """

    @abstractmethod
    def analyze_same_period_numbers(self, **kwargs: Any) -> None:
        """
        Analyze same period number in the last period.
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_same_weekday_numbers(self, **kwargs: Any) -> None:
        """
        Analyze same weekday number in the last period.
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_repeated_numbers(self, **kwargs: Any) -> None:
        """
        Analyze the number that appeared twice in the last two period.
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_edge_numbers(self, **kwargs: Any) -> None:
        """
        Analyze Also called adjacent number, plus or minus 1 with the winning number issued in the previous period
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_cold_hot_numbers(self, **kwargs: Any) -> None:
        """
        Analyze Numbers that have appeared in the last period
        Analyze Numbers that have not appeared in the last period
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_omitted_numbers(self, **kwargs: Any) -> None:
        """
        Analyze.
        Omission: The number of periods since the previous opening to the current period.
        Average omission: The average number of omissions in the statistical period
                          (calculation formula: Average omission =
                          total number of omissions in the statistical period / (number of occurrences +1))
        Maximum missed value: Indicates the maximum value of all missed values in the statistical period.
        Current omission: The number of periods between the last occurrence and the present, if the missing object
                          appeared in the current period, the current omission value is 0
        Previous period omission: The interval between the last two periods (excluding the current period)
        Theoretical number: The theoretical number refers to the number of times the missing object should
                            theoretically appear, = the total number of t times * theoretical probability
        Desired probability: Desired probability reflects the ideal occurrence probability of the missing object.
                             The formula is (current omission/average omission * theoretical probability)
        """
        raise NotImplementedError
