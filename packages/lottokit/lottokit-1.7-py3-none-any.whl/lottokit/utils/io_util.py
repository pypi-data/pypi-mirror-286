#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: io_util.py
@DateTime: 2024/7/22 10:08
@SoftWare: PyCharm
"""

import sys
import csv
import json
import logging
import logging.handlers
from typing import List, Any, Optional


class IOUtil:
    @classmethod
    def get_logger(cls, log_file: str = None) -> logging.Logger:
        # Choose a unique logger name based on the log_file argument
        logger_name = log_file if log_file is not None else 'default_logger'
        # Get the logger instance by name
        logger = logging.getLogger(logger_name)

        # Check if the logger already has handlers to prevent adding them again
        if not logger.handlers:
            if log_file is None:
                # Configuration for logging to the terminal
                # log_format = '%(asctime)s [%(levelname)s] <%(lineno)d> %(funcName)s: %(message)s'
                log_format = '%(message)s'
                handler = logging.StreamHandler(sys.stdout)
            else:
                # Configuration for logging to a file with rotation at midnight
                log_format = ('%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                              '%(filename)s <%(lineno)d> %(funcName)s: %(message)s')
                handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=7)

            # Set the formatter for the handler
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)

            # Optionally set a different log level for the handler
            handler.setLevel(logging.INFO)

            # Add the handler to the logger
            logger.addHandler(handler)
            # Set the log level for the logger
            logger.setLevel(logging.INFO)

        # Return the configured logger
        return logger

    @classmethod
    def detail_log(cls: Any, app_log: Any, show_details: Optional[str] = None, **kwargs: Any) -> None:
        if show_details is not None:
            detail_message = kwargs.get(show_details, '')
            app_log.info(detail_message)

    @classmethod
    def print_matrix(cls: Any, appeared_sequences: List[List[int]], matrix_size: int) -> None:
        for sequence in appeared_sequences:
            for i in range(1, matrix_size + 1):
                if i in sequence:
                    print(f"{i:>4}", end=" ")
                else:
                    print(f"{'-':>4}", end=" ")
            print()

    @classmethod
    def list_to_int(cls, numbers: List[int], zero_replacement: str = '', **kwargs: Any) -> int:
        """
        Convert a list of integers to a single integer, with an optional replacement for zeros.

        :param numbers: list of integers
        :param zero_replacement: string to replace zeros with, defaults to an empty string
        :return: single integer formed by concatenating the list elements
        """
        # Validate input data is a list
        if not isinstance(numbers, List):
            raise ValueError("Input 'numbers' must be a list.")

        # Validate all elements in the list are integers
        if not all(isinstance(x, int) for x in numbers):
            raise ValueError("All elements in the 'numbers' list must be integers.")

        # Convert list elements to strings, replacing zeros with zero_replacement
        parts = [zero_replacement if x == 0 else str(x) for x in numbers]

        # Join the parts and convert to an integer
        return int(''.join(parts))

    @classmethod
    def int_to_list(cls, number: int, modulus: int = 10, **kwargs: Any) -> List[int]:
        """
        Convert an integer to a list of digits, each digit is the remainder of division by a modulus.

        :param number: The integer to be converted into a list of digits.
        :param modulus: The divisor used for the modulo operation on each digit, defaults to 10.
        :return: A list of integers, where each integer is a digit of the original number after the modulo operation.
        """
        # Validate input data is an integer
        if not isinstance(number, int):
            raise ValueError("Input 'number' must be an integer.")

        # Validate modulus is a positive integer
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError("Input 'modulus' must be a positive integer.")

        # Convert the integer to a list of digits using the modulus
        digit_list = [int(d) % modulus for d in str(abs(number))]

        # Return the list of digits
        return digit_list

    @classmethod
    def write_data_to_file(
            cls,
            file_path: str,
            data: List[str],
            app_log: Optional[logging.Logger] = None,
            mode: str = 'a+',
            **kwargs: Any
    ) -> bool:
        """
        Write data to a file.

        :param file_path: Path to the file where data will be written.
        :param data: List of data to write to the file.
        :param app_log: Optional logger for logging information, defaults to None.
        :param mode: Mode in which the file should be opened, defaults to 'a+' for append.
        :return: bool weather success or failed
        """
        if app_log is None:
            app_log = cls.get_logger()

        if not data:
            app_log.warning("No data provided to write to the file.")
            return False

        try:
            with open(file_path, mode) as fp:
                app_log.debug(f'Writing to file: {fp.name}')
                for line in data:
                    if line is not None:
                        fp.write(f'{line}\n')
        except Exception as ex:
            app_log.exception(f"An error occurred while writing to the file: {ex}")
            return False

        return True

    @classmethod
    def read_data_from_file(
            cls,
            file_path: str,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'r'
    ) -> Optional[List[str]]:
        """
        Read data from a file and return a list of non-empty lines.

        :param file_path: Path to the file to be read.
        :param app_log: Optional logger for logging information, defaults to None.
        :param mode: Mode in which the file should be opened, defaults to 'r' for read only.
        :return: List of non-empty lines from the file or None if an exception occurs.
        """
        if app_log is None:
            app_log = cls.get_logger()

        data = []
        try:
            with open(file_path, mode) as fp:
                app_log.debug(f'Opening file: {fp.name}')
                data = [line.strip() for line in fp if line.strip()]
        except Exception as ex:
            app_log.exception(f"An error occurred while reading the file: {ex}")
            return None

        app_log.info(f'Number of non-empty lines read: {len(data)}')
        return data

    @classmethod
    def write_csv_data_to_file(
            cls,
            file_path: str,
            data: List[List[Any]],
            app_log: Optional[logging.Logger] = None,
            mode: str = 'a+',
            newline: str = '',
            **kwargs: Any
    ) -> bool:
        """
        Write data to a CSV file.

        :param file_path: Path to the file where CSV data will be written.
        :param data: List of rows (where each row is a list) to write to the CSV file.
        :param app_log: Optional logger for logging information, defaults to None which will create a new logger.
        :param mode: Mode in which the file should be opened, defaults to 'a+' for append.
        :param newline: Controls how universal newlines works (it only applies to text mode). It defaults to ''.
        :return: bool weather success or failed
        """
        if app_log is None:
            app_log = cls.get_logger()

        if not data:
            app_log.warning("No data provided to write to the file.")
            return False

        try:
            with open(file_path, mode=mode, newline=newline) as fp:
                app_log.debug(f'Writing to CSV file: {fp.name}')
                writer = csv.writer(fp, **kwargs)
                writer.writerows(data)
        except Exception as ex:
            app_log.exception(f"An error occurred while writing to the CSV file: {ex}")
            return False

        return True

    @classmethod
    def read_csv_data_from_file(
            cls,
            file_path: str,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'r',
            **kwargs: Any
    ) -> Optional[List[List[str]]]:
        """
        Read CSV data from a file and return a list of rows.

        :param file_path: Path to the CSV file to be read.
        :param app_log: Optional logger for logging information, defaults to a new logger if None.
        :param mode: Mode in which the file should be opened, defaults to 'r' for read only.
        :return: List of rows from the CSV file or None if an exception occurs.
        """
        if app_log is None:
            app_log = cls.get_logger()

        try:
            with open(file_path, mode=mode, **kwargs) as fp:
                app_log.debug(f'Reading CSV file: {fp.name}')
                reader = csv.reader(fp, **kwargs)
                data = [row for row in reader]
        except Exception as ex:
            app_log.exception(f"An error occurred while reading the CSV file: {ex}")
            return None

        return data

    @classmethod
    def write_json_data_to_file(
            cls,
            file_path: str,
            data: Any,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'w',
            **kwargs: Any
    ) -> bool:
        """
        Write data to a JSON file.

        :param file_path: Name of the JSON file.
        :param data: Data to write (usually a dict or a list).
        :param app_log: Optional logger for logging information, defaults to a new logger if None.
        :param mode: Mode in which the file should be opened, defaults to 'w' for write (overwriting).
        :return: bool weather success or failed
        """
        if app_log is None:
            app_log = cls.get_logger()

        app_log.debug(f'Writing to JSON file: {file_path}')
        try:
            with open(file_path, mode, encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False, indent=4, **kwargs)
        except Exception as ex:
            app_log.exception(f"An error occurred while writing to the JSON file: {ex}")
            return False

        return True

    @classmethod
    def read_json_data_from_file(
            cls,
            file_path: str,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'r',
            **kwargs: Any
    ) -> Optional[Any]:
        """
        Read data from a JSON file.

        :param file_path: Name of the JSON file.
        :param app_log: Optional logger for logging information, defaults to a new logger if None.
        :param mode: Mode in which the file should be opened, defaults to 'r' for read.
        :return: Data read from the JSON file or None if an exception occurs.
        """
        if app_log is None:
            app_log = cls.get_logger()

        try:
            with open(file_path, mode, encoding='utf-8', **kwargs) as fp:
                app_log.debug(f'Reading from JSON file: {file_path}')
                return json.load(fp)
        except Exception as ex:
            app_log.exception(f"An error occurred while reading the JSON file: {ex}")
            return None
