#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: denoiser_util.py
@DateTime: 2024/7/22 10:25
@SoftWare: PyCharm
"""

import pywt
import numpy as np
from typing import List, Union


class DenoiserUtil:
    @staticmethod
    def moving_average(sequence: List[Union[int, float]], window_size: int = 3) -> np.ndarray:
        """
        Calculate the moving average of a sequence using a sliding window.

        :param sequence: The input sequence, as a list.
        :param window_size: The size of the sliding window, default is 3.
        :return: The sequence processed with moving average, as a numpy array.
        """
        return np.convolve(sequence, np.ones(window_size) / window_size, mode='valid')

    @staticmethod
    def median_filter(sequence: List[Union[int, float]], kernel_size: int = 3) -> List[float]:
        """
        Apply a median filter to the sequence to reduce noise.

        :param sequence: The input sequence, as a list.
        :param kernel_size: The size of the kernel, default is 3.
        :return: The sequence processed with a median filter, as a list.
        """
        filtered_sequence = []
        for i in range(len(sequence)):
            start = max(0, i - kernel_size // 2)
            end = min(len(sequence), i + kernel_size // 2 + 1)
            median_val = np.median(sequence[start:end])
            filtered_sequence.append(median_val)
        return filtered_sequence

    @staticmethod
    def remove_outliers(sequence: List[Union[int, float]], threshold: float = 2.0) -> List[Union[int, float]]:
        """
        Remove outliers from the sequence.

        :param sequence: The input sequence, as a list.
        :param threshold: The threshold value for detecting outliers, default is 2.0.
        :return: The sequence with outliers removed, as a list.
        """
        mean = np.mean(sequence)
        std_dev = np.std(sequence)
        filtered_sequence = [x for x in sequence if np.abs(x - mean) <= threshold * std_dev]
        return filtered_sequence

    @staticmethod
    def denoise_wavelet(sequence: List[Union[int, float]], wavelet: str = 'db1', level: int = 1) -> np.ndarray:
        """
        Denoise the sequence using wavelet transformation.

        :param sequence: The input sequence, as a list.
        :param wavelet: The name of the wavelet to use, default is 'db1'.
        :param level: The level of decomposition, default is 1.
        :return: The wavelet-denoised sequence, as a numpy array.
        """
        coeffs = pywt.wavedec(sequence, wavelet, level=level)
        sigma = np.median(np.abs(coeffs[-level])) / 0.6745
        uthresh = sigma * np.sqrt(2 * np.log(len(sequence)))
        coeffs[1:] = [pywt.threshold(i, value=uthresh, mode='soft') for i in coeffs[1:]]
        return pywt.waverec(coeffs, wavelet)
