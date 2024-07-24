#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: calculate_util.py
@DateTime: 2024/7/22 10:09
@SoftWare: PyCharm
"""

import math
import datetime
from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple, Any, Optional, Union, Set, Dict, Generator


class CalculateUtil(ABC):
    """
    Compute features based on a single or multi of data
    """

    @staticmethod
    def real_round(n):
        """
        Custom rounding function.

        Parameters:
        n (float): The number to round.

        Returns:
        int: The rounded result.
        """
        return math.floor(n + 0.5)

    @staticmethod
    def invert_round(n):
        """
        Custom rounding function where:
        - Values with decimal part less than 0.5 are rounded up.
        - Values with decimal part exactly 0.5 are rounded down.

        Parameters:
        n (float): The number to round.

        Returns:
        int: The rounded result.
        """
        if n % 1 >= 0.5:
            return math.floor(n)
        else:
            return math.ceil(n)

    @staticmethod
    def longest_increasing_subsequence(numeric_sequence: List[int]) -> List[int]:
        """
        Finds the longest increasing subsequence in a given numeric sequence.

        Args:
        numeric_sequence (List[int]): The input list of integers.

        Returns:
        List[int]: The longest increasing subsequence.
        """
        n = len(numeric_sequence)
        dp = [1] * n

        # Fill dp array with lengths of LIS ending at each index
        for i in range(1, n):
            for j in range(0, i):
                if numeric_sequence[i] > numeric_sequence[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        lis_length = max(dp)
        lis = []

        # Find the index of the maximum value in dp array
        max_index = dp.index(lis_length)
        lis.append(numeric_sequence[max_index])
        current_length = lis_length - 1

        # Trace back the sequence to find the LIS
        for i in range(max_index - 1, -1, -1):
            if dp[i] == current_length and numeric_sequence[i] < lis[-1]:
                lis.append(numeric_sequence[i])
                current_length -= 1

        return list(reversed(lis))

    @staticmethod
    def longest_decreasing_subsequence(numeric_sequence: List[int]) -> List[int]:
        """
        Finds the longest decreasing subsequence in a given numeric sequence.

        Args:
        numeric_sequence (List[int]): The input list of integers.

        Returns:
        List[int]: The longest decreasing subsequence.
        """
        n = len(numeric_sequence)
        dp = [1] * n

        # Fill dp array with lengths of LDS ending at each index
        for i in range(1, n):
            for j in range(0, i):
                if numeric_sequence[i] < numeric_sequence[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        lds_length = max(dp)
        lds = []

        # Find the index of the maximum value in dp array
        max_index = dp.index(lds_length)
        lds.append(numeric_sequence[max_index])
        current_length = lds_length - 1

        # Trace back the sequence to find the LDS
        for i in range(max_index - 1, -1, -1):
            if dp[i] == current_length and numeric_sequence[i] > lds[-1]:
                lds.append(numeric_sequence[i])
                current_length -= 1

        return list(reversed(lds))

    @staticmethod
    def generate_chunks_with_next(data: List[Any],
                                  chunk_size: int = 10) -> Generator[Tuple[List[Any], Optional[Any]], None, None]:
        """
        Yields consecutive chunks of size `chunk_size` from `data` after removing elements from the start of `data`
        based on the remainder of the length of `data` divided by `chunk_size`. Exits if the next element is None.

        :param data: The list of data from which to extract chunks.
        :param chunk_size: The size of each chunk. Default is 10.
        :yield: Tuples containing a chunk and the next element, if it exists.
        """
        # Calculate the number of elements to remove from the beginning of the list
        remainder = len(data) % chunk_size
        if remainder > 0:
            data = data[remainder:]

        # Generate the chunks and the next element
        for i in range(0, len(data)):
            chunk = data[i:i + chunk_size]
            next_element = data[i + chunk_size] if i + chunk_size < len(data) else None
            if next_element is None:
                break  # Break if we've reached or passed the end of the list
            yield chunk, next_element

    @staticmethod
    def generate_datasets_with_rolling_size(data: List[int],
                                            rolling_size: int = 5,
                                            adjust: bool = False) -> Tuple[List[List[int]], List[int]]:
        """
        Generates sequential test and validation datasets from a list of integers. It optionally adjusts
        test datasets by removing extreme values.

        The function iterates over the data to create overlapping test sets of a specified size. Each test set is
        followed by a validation set which is the next single element in the list. If the 'adjust' flag is True,
        the maximum and minimum values are removed from each test set.

        Args:
            data (List[int]): The input data list from which datasets are generated.
            rolling_size (int): The number of elements in each test set. Defaults to 5.
            adjust (bool): Whether to remove the maximum and minimum values from each test set. Defaults to False.

        Returns:
            Tuple[List[List[int]], List[int]]: A tuple containing two lists:
                - The first list contains the test sets, possibly adjusted.
                - The second list contains the single-element validation sets.
        """
        x_sets = []  # List to hold the test sets
        y_sets = []  # List to hold the validation sets

        # Iterate over the data to form test and validation sets
        for i in range(len(data) - rolling_size):
            test_set = data[i:i + rolling_size]  # Extract size elements for the test set
            validation_set = data[i + rolling_size]  # Take the next element as the validation set

            if len(test_set) > 2 and adjust:
                # Remove the maximum and minimum values if adjusting
                max_val = max(test_set)
                min_val = min(test_set)
                max_index = test_set.index(max_val)
                min_index = test_set.index(min_val)
                filtered_test_set = [x for idx, x in enumerate(test_set) if idx != max_index and idx != min_index]
                x_sets.append(filtered_test_set)
            else:
                x_sets.append(test_set)  # Append the test set as is if not adjusting

            y_sets.append(validation_set)  # Append the validation element

        return x_sets, y_sets

    @staticmethod
    def calculate_euclidean_distance(
            point1: Tuple[Any, ...],
            point2: Tuple[Any, ...]
    ) -> int:
        """
        Calculate the Euclidean distance between two points in n-dimensional space.

        The Euclidean distance is the straight-line distance between two points in Euclidean space.

        Args:
            point1 (Tuple[Any, ...]): The first point as an iterable of coordinates.
            point2 (Tuple[Any, ...]): The second point as an iterable of coordinates.

        Returns:
            int: The Euclidean distance between point1 and point2.

        Raises:
            ValueError: If point1 and point2 do not have the same dimensions.
        """
        if point1 is None or point2 is None:
            raise ValueError("Euclidean distance cannot be calculated for empty points.")

        if len(point1) != len(point2):
            raise ValueError("Both points must have the same number of dimensions.")

        p1 = [float(p) if p is not None else 0.0 for p in point1]
        p2 = [float(p) if p is not None else 0.0 for p in point2]

        euclidean_distance = math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(p1, p2)))
        return CalculateUtil.real_round(euclidean_distance)

    @staticmethod
    def calculate_same_number_index(target_data: List[int], input_data: List[int]) -> List[int]:
        """
        Finds the indices in 'target_data' where the numbers are present in 'input_data'.

        Args:
        target_data (List[int]): The list of target integers.
        input_data (List[int]): The list of input integers to be matched against.

        Returns:
        List[int]: A list of indices (1-based) in 'target_data' where numbers are found in 'input_data'.
        """
        same_number_index = []
        for ind, num in enumerate(target_data):
            if num in input_data:
                same_number_index.append(ind)
        return same_number_index

    @staticmethod
    def calculate_edge_number_index(target_data: List[int], input_data: List[int]) -> List[int]:
        """
        Finds the indices in 'target_data' where the numbers are adjacent to any number in 'input_data'.
        A number is considered adjacent if it's either one smaller or one larger.

        Args:
        target_data (List[int]): The list of target integers.
        input_data (List[int]): The list of input integers to check for adjacency.

        Returns:
        List[int]: A list of indices (1-based) in 'target_data' where numbers are adjacent to any in 'input_data'.
        """
        edge_info = []
        for ind, num in enumerate(target_data):
            edge_nums = set(num + i for i in [-1, 1])
            plead_edge = set(input_data).intersection(edge_nums)
            if len(plead_edge) > 0:
                edge_info.append(ind)
        return edge_info

    @classmethod
    def calculate_zone_ratio(
            cls,
            number_combination: Iterable[int],
            zone_ranges: List[Tuple[int, int]],
            **kwargs: Any
    ) -> Tuple[int, ...]:
        """
        Calculate the counts of numbers within predefined zones for a given sequence of numbers.
        This class method determines the distribution of the numbers in the input sequence across specified zones.
        Each zone is defined by a range, and this method counts how many numbers fall into each zone.

        :param number_combination: An iterable of numbers (like a list or tuple) from which the method will count how many
                                    numbers fall into each zone.
        :param zone_ranges: A list of tuples where each tuple contains two numbers representing the start and end of a
                            zone range, respectively. These ranges define the zones for categorizing the numbers.
        :param kwargs: Additional keyword arguments that may be used for future extensions of the method.
        :return: A tuple containing the count of numbers that fall within each specified zone.
        """

        # Check if zone ranges are defined, if not, raise an exception.
        if not zone_ranges:
            raise ValueError('Zone ranges must be provided.')

        # Initialize counters for each zone to zero.
        ratio = [0] * len(zone_ranges)

        # Iterate through each number and check which zone it falls into.
        for num in map(int, number_combination):  # Convert each number to an integer once before the loop.
            for i, (start, end) in enumerate(zone_ranges):
                if start <= num <= end:
                    ratio[i] += 1  # Increment the counter for the current zone.
                    break  # If the number is within the current zone, no need to check further zones.

        # Return the counts as a tuple, with each element representing the count for a respective zone.
        return tuple(ratio)

    @classmethod
    def calculate_big_small_ratio(
            cls,
            number_combinations: Iterable[int],
            big_small_ranges: List[Tuple[int, int]],
            **kwargs: Any
    ) -> Tuple[int, ...]:
        """
        Calculate the counts of numbers within predefined size ranges for a sequence of numbers.
        This class method assesses how many numbers from the input sequence fall within each of the specified size ranges.
        Each range represents a 'zone', which could correspond to a concept like 'big' or 'small' numbers.

        :param number_combinations: An iterable of numbers (like a list or tuple) from which the method will count how many
                                    numbers fall into each size range.
        :param big_small_ranges: A list of tuples where each tuple contains two numbers representing the start and end of a
                                 range, respectively. These ranges define the zones for categorizing the numbers.
        :param kwargs: Additional keyword arguments that may be used for future extensions of the method.
        :return: A tuple containing the count of numbers that fall within each specified range or 'zone'.
        """

        # Check if size ranges are defined, if not, raise an exception.
        if not big_small_ranges:
            raise ValueError('Size ranges for big and small numbers must be provided.')

        # Initialize counters for each range to zero.
        ratio = [0] * len(big_small_ranges)

        # Iterate through each number and check which range it falls into.
        for num in map(int, number_combinations):  # Convert each number to an integer once before the loop.
            for i, (start, end) in enumerate(big_small_ranges):
                if start <= num <= end:
                    ratio[i] += 1  # Increment the counter for the current range.
                    break  # If the number is within the current range, no need to check further ranges.

        # Return the counts as a tuple, with each element representing the count for a respective range or 'zone'.
        return tuple(ratio)

    @classmethod
    def calculate_road_012_ratio(
            cls,
            number_combination: Iterable[int],
            road_012_ranges: List[tuple[int, ...]],
            **kwargs: Any
    ) -> Tuple[int, ...]:
        """
        Calculate the count of numbers within predefined zones (referred to as 'roads') for a given sequence of numbers.
        This class method determines how many numbers from the input fall within each of the specified ranges. Each range
        represents a 'road', which is a segment of the overall data set.

        :param number_combination: A list, tuple, or other iterable of numbers. The method will iterate through this
                                   collection to count how many numbers fall into each 'road' as defined by the ranges.
        :param road_012_ranges: A list of range objects or sequences defining the 'roads'. Each element in this list
                                corresponds to a different 'road', and the numbers in 'number_combination' are checked
                                against these ranges to determine their counts.
        :param kwargs: Additional keyword arguments that are not used in this method but are included for potential
                       future extensibility of the method.
        :return: A tuple containing the count of numbers in each 'road'.
        """

        # Validate the presence of 'road_012_ranges'.
        if not road_012_ranges:
            raise ValueError('Road 012 ranges must be provided.')

        # Initialize counters for each 'road' to zero.
        ratio = [0] * len(road_012_ranges)

        # Count the numbers in each 'road' by iterating through the input numbers and the defined ranges.
        for num in map(int, number_combination):  # Convert each number to an integer once, before the loop.
            for i, vals in enumerate(road_012_ranges):
                if num in vals:
                    ratio[i] += 1
                    break  # Once the number is found in a 'road', stop checking the remaining 'roads'.

        # Return the counts as a tuple, with each element representing the count for a respective 'road'.
        return tuple(ratio)

    @classmethod
    def calculate_odd_even_ratio(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> Tuple[int, int]:
        """
        Calculate the ratio of odd to even numbers within a given sequence of numbers.
        This method is designed to be called on the class itself rather than on an instance of the class. It can be
        used to analyze a collection of numbers (number_combination) and determine the count of odd and even numbers.

        :param number_combination: A list, tuple, or other iterable of integers. The method will iterate through
                                   this collection to determine the count of odd and even numbers.
        :param kwargs: Additional keyword arguments that are not used in this method but are included for potential
                       future extensibility of the method.
        :return: A tuple containing two elements; the first is the count of odd numbers and the second is the
                 count of even numbers in the number_combination.
        """

        # Count the number of odd numbers in the number_combination
        # A number is considered odd if the remainder of the division by 2 is 1 (num % 2 evaluates to True)
        odd_count = sum(1 for num in number_combination if num % 2)

        # Count the number of even numbers in the number_combination
        # It's calculated by subtracting the odd count from the total length of the number_combination
        even_count = len(list(number_combination)) - odd_count

        # Return a tuple of odd and even counts
        return odd_count, even_count

    @classmethod
    def calculate_prime_composite_ratio(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> Tuple[int, int]:
        """
        Calculate the ratio of prime to composite numbers in a sequence of numbers provided in the number_combination.
        In this context, the number 1 is considered a prime number.

        :param number_combination: A list or tuple of numerical values. The method will determine which numbers are
                                   prime (including 1) and which are composite, and compute their counts.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: A tuple containing two elements; the first is the count of prime numbers (including 1) and the
                 second is the count of composite numbers in the number_combination.
        """

        def is_prime(num: int) -> bool:
            # Consider 1 as a prime number for the purpose of this calculation
            if num == 1:
                return True
            # Exclude numbers less than 1 and even numbers greater than 2 as they are not prime
            if num < 1 or (num % 2 == 0 and num > 2):
                return False
            # Check for factors from 3 to the square root of num
            for i in range(3, int(num ** 0.5) + 1, 2):
                if num % i == 0:
                    return False
            return True

        # Count prime numbers in the number_combination
        prime_count = sum(1 for num in number_combination if is_prime(num))
        # Count composite numbers as the remaining numbers in the number_combination
        composite_count = len(list(number_combination)) - prime_count

        # Return a tuple of prime and composite counts
        return prime_count, composite_count

    @classmethod
    def calculate_span(
            cls,
            number_combination:
            Iterable[int],
            **kwargs: Any
    ) -> int:
        """
        Calculate the span of a sequence of numbers provided in the number_combination. The span is defined as the
        difference between the maximum and minimum values in the set of numbers.

        :param number_combination: A list or tuple of numerical values. The method will find the maximum and minimum
                                   values in this collection and calculate the difference (span) between them.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: The span of the numbers in the number_combination as an integer. If the input contains floating
                 point numbers, the span is cast to an integer before being returned.
        """

        # Find the maximum and minimum values in the number combination
        max_value = max(number_combination)
        min_value = min(number_combination)

        # Calculate the span by subtracting the minimum value from the maximum value
        span = max_value - min_value

        # Cast the span to an integer and return it
        return int(span)

    @classmethod
    def calculate_sum_total(
            cls,
            number_combination: Iterable[Union[int, float]],
            **kwargs: Any
    ) -> Union[int, float]:
        """
        Calculate the total sum of a sequence of numbers provided in the number_combination. This method
        aggregates all the numerical values in the list or tuple passed as an argument and returns their sum.

        :param number_combination: A list or tuple of numerical values. The method will sum these values and return
                                   the result.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: The sum total of the numbers in the number_combination as an integer or float, depending on the
                 input values.
        """

        # Calculate the sum of the numbers in the combination using the built-in sum function
        total_sum = sum(number_combination)

        # Return the sum total
        return total_sum

    @classmethod
    def calculate_sum_tail(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> int:
        """
        Calculate the last digit (tail) of the sum of a given number combination. The tail is the unit's place
        of the sum, which can be useful for certain types of numerical analysis or pattern recognition.

        :param number_combination: A list or tuple of numerical values. The sum of these numbers will be calculated,
                                   and the tail of this sum (last digit) will be returned.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: The last digit of the sum of the number combination as an integer.
        """

        # Calculate the sum of the numbers in the combination
        total_sum = cls.calculate_sum_total(number_combination)

        # Return the last digit of this sum
        return total_sum % 10

    @classmethod
    def calculate_weekday(
            cls,
            date: str,
            date_format: str = '%Y-%m-%d',
            **kwargs: Any
    ) -> int:
        """
        Calculate the weekday number from a date string.

        :param date: Date string.
        :param date_format: default 'YYYY-MM-DD' format
        :return: Weekday number where 1 represents Monday and 7 represents Sunday.
        """
        date = datetime.datetime.strptime(date, date_format).date()
        return date.weekday() + 1

    @classmethod
    def calculate_ac(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> int:
        """
        Compute the complexity of a given number combination. Complexity is defined as the number of distinct
        absolute differences between each pair of numbers in the combination, excluding the number of elements minus one.

        :param number_combination: A list or tuple of numerical values for which the complexity will be calculated.
        :param kwargs: Additional keyword arguments, not used in this function but allows for extensibility.
        :return: An integer representing the complexity of the number combination.
        """

        # Initialize a set to store distinct absolute differences
        distinct_diffs = set()

        # Count the number of elements in the number combination
        number_combination_list = list(number_combination)
        num_count = len(number_combination_list)

        # Iterate over each unique pair of numbers to calculate absolute differences
        for i in range(num_count):
            for j in range(i + 1, num_count):
                # Calculate the absolute difference between the two numbers
                diff = abs(number_combination_list[j] - number_combination_list[i])
                # Add the absolute difference to the set of distinct differences
                distinct_diffs.add(diff)

        # Return the number of distinct differences minus the number of elements minus one
        return len(distinct_diffs) - (num_count - 1)

    @classmethod
    def calculate_avg(cls, number_combination: Iterable[int], **kwargs: Any) -> int:
        return math.floor(sum(number_combination) / len(list(number_combination)))

    @classmethod
    def calculate_consecutive_numbers(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> List[List[int]]:
        """
        Calculate the sequences of consecutive numbers in a given iterable of integers.

        :param number_combination: An iterable of integers to compute consecutive numbers from.
        :param kwargs: Additional keyword arguments.
        :return: A list of lists, each containing a sequence of consecutive numbers.
        """
        # Convert the input iterable to a list to support indexing
        number_combination_list = list(number_combination)
        sequences = []
        current_sequence = [number_combination_list[0]]  # Initialize with the first number

        for i in range(1, len(number_combination_list)):
            if number_combination_list[i] == current_sequence[-1] + 1:
                current_sequence.append(number_combination_list[i])
            else:
                if len(current_sequence) > 1:
                    sequences.append(current_sequence)
                current_sequence = [number_combination_list[i]]

        if len(current_sequence) > 1:
            sequences.append(current_sequence)

        return sequences

    @classmethod
    def calculate_repeated_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            window: int = 2,
            **kwargs: Any
    ) -> List[int]:
        """
        Calculate the numbers that appear in all given iterable of integers (intersection).

        :param number_combinations: An iterable of integers to find common numbers.
        :param window: The number of recent periods to process.
        :param kwargs: Additional keyword arguments.
        :return: A list containing the numbers that are common in all given iterables.
        """
        # Initialize the set with the first iterable to start the intersection process
        repeated_numbers: Set[int] = set(next(iter(number_combinations[-window:]), []))

        # Perform intersection with the subsequent iterables
        for number_combination in number_combinations:
            repeated_numbers.intersection_update(set(number_combination))

        # Return the result as a list
        return list(repeated_numbers)

    @classmethod
    def calculate_edge_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            window: int = 2,
            **kwargs: Any
    ) -> List[int]:
        """
        Calculate 'edge numbers' which are present in consecutive iterables where each number from the first iterable
        is either one less or one more than the numbers in the following iterable.

        :param number_combinations: An iterable of iterables of integers to find 'edge numbers'.
        :param window: The number of recent periods to process.
        :param kwargs: Additional keyword arguments.
        :return: A list containing the 'edge numbers'.
        """
        # Convert the input to a list for indexed access
        number_combinations_list = list(number_combinations[-window:])

        # Initialize an empty set for the edge numbers
        edge_numbers: Set[int] = set()

        # Iterate over each number combination, starting from the second one
        for index in range(1, len(number_combinations_list)):
            # Create a set of potential edge numbers from the previous combination
            last_number_set = set(num + i for i in [-1, 0, 1]
                                  for num in number_combinations_list[index - 1]
                                  if (num + i) > 0)
            # Create a set from the current combination
            current_number_set = set(number_combinations_list[index])
            # Find the intersection of the two sets
            intersection = current_number_set.intersection(last_number_set)
            # Update the edge numbers set with the intersection
            edge_numbers.update(intersection)

        # Return the result as a sorted list to maintain a consistent order
        return sorted(edge_numbers)

    @classmethod
    def calculate_cold_hot_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            all_numbers: Iterable[int],
            window: int = 5,
            **kwargs: Any
    ) -> Tuple[List[int], List[int]]:
        """
        Calculate and return 'cold numbers' and 'hot numbers' from a series of number combinations.
        'Cold numbers' are those that did not appear in the last 5 iterations,
        and 'hot numbers' are those that appeared at least once in the last 5 iterations.

        :param number_combinations: An iterable of iterables of integers to analyze numbers.
        :param all_numbers: An iterable of all possible numbers that could appear.
        :param window: default 5
        :param kwargs: Additional keyword arguments.
        :return: A tuple containing two lists - the first with 'cold numbers' and the second with 'hot numbers'.
        """
        # Convert the input to a list for indexed access
        number_combinations_list = list(number_combinations[-window:])

        # Determine the range for the last 5 periods
        last_five_periods = number_combinations_list if len(
            number_combinations_list) >= window else number_combinations_list

        # Flatten the list of last five periods and convert to a set to remove duplicates
        numbers_in_last_five_periods: Set[int] = set(num for period in last_five_periods for num in period)

        # Convert all_numbers to a set for efficient lookup
        all_numbers_set: Set[int] = set(all_numbers)

        # 'Cold numbers' are those that are not in the last five periods
        cold_numbers: List[int] = sorted(list(all_numbers_set - numbers_in_last_five_periods))

        # 'Hot numbers' are those that are in the last five periods
        hot_numbers: List[int] = sorted(list(numbers_in_last_five_periods))

        # Return the cold numbers and hot numbers
        return cold_numbers, hot_numbers

    @classmethod
    def calculate_omitted_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            all_numbers: Iterable[int],
            window: int = 10,
            **kwargs: Any
    ) -> Dict[int, int]:
        """
        Update and return the omission values for each number in all_numbers.

        :param number_combinations: A list of lists of integers representing past number draws.
        :param all_numbers: A list of all possible numbers that could appear.
        :param window: default 10
        :return: A dictionary with numbers as keys and their omission values as values.
        """
        # Initialize the omission values for each number to 0
        omission_values: Dict[int, int] = {number: -1 for number in all_numbers}

        # Convert the input to a list for indexed access
        number_combinations_list = list(number_combinations[-window:])

        # Determine the range for the last 5 periods
        last_ten_periods = number_combinations_list if len(
            number_combinations_list) >= window else number_combinations_list

        # The number of draws since the last appearance
        draws_since_last_appearance = 0

        # Iterate over the past draws in reverse order (most recent first)
        for draw in reversed(last_ten_periods):
            # Check each number in all_numbers
            for number in all_numbers:
                # If the number is in the current draw and its omission value is -1 (hasn't appeared yet)
                if number in draw and omission_values[number] == -1:
                    # Set the omission value to the number of draws since it last appeared
                    omission_values[number] = draws_since_last_appearance
            # Increment the count of draws since the last appearance
            draws_since_last_appearance += 1

        # For any number that hasn't appeared yet, set its omission value to the total number of draws
        for number in all_numbers:
            if omission_values[number] == -1:
                omission_values[number] = draws_since_last_appearance

        return omission_values

    @staticmethod
    def calculate_standard_deviation_welford(numeric_sequence: List[Union[int, float]],
                                             decay_factor: Union[int, float] = 0.95) -> Union[int, float]:
        """
        Calculates the standard deviation of a numeric sequence using Welford's method.

        This method is an online algorithm designed to compute the standard deviation of a sequence of numbers
        iteratively, which can be useful for large datasets where all data cannot be loaded into memory at once.

        Args:
            numeric_sequence (List[Union[int, float]]): The sequence of numbers (integers or floats) for which the standard deviation is to be calculated.
            decay_factor (Union[int, float]): The decay factor for weighting recent values more heavily. Defaults to 0.95.

        Returns:
            float: The standard deviation of the sequence. Returns 0 if the sequence contains fewer than two elements.

        Notes:
            This function uses an exponential decay to weight recent observations more heavily in the calculation
            of the mean and variance, which makes it sensitive to recent changes in the sequence.
        """

        if len(numeric_sequence) == 0:
            raise ValueError("The numeric sequence cannot be empty.")
        n = 0
        mean = 0.0
        M2 = 0.0
        weighted_n = 0.0  # Weighted sample count

        for x in numeric_sequence:
            n += 1
            weight = decay_factor ** (len(numeric_sequence) - n)  # Compute weight, newer data has higher weight
            delta = x - mean
            weighted_n += weight
            mean += (delta * weight) / weighted_n
            delta2 = x - mean
            M2 += delta * delta2 * weight

        if weighted_n < 2:
            return 0.0  # Not enough samples to compute standard deviation
        variance = M2 / weighted_n  # Compute variance using weighted sample count
        return math.sqrt(variance)

    @staticmethod
    def calculate_standard_deviation(numeric_sequence: List[Union[int, float]]) -> Union[int, float]:
        """
        Calculates the standard deviation of a numeric sequence.

        This method computes the standard deviation by first calculating the mean of the numbers,
        then the variance as the average of the squared differences from the mean, and finally
        taking the square root of the variance.

        Args:
            numeric_sequence (List[Union[int, float]]): The sequence of numbers (integers or floats) for which the standard deviation is to be calculated.

        Returns:
            float: The standard deviation of the sequence.

        Raises:
            ValueError: If the numeric_sequence is empty, as standard deviation cannot be calculated.
        Notes:
            This function uses an exponential decay to weight recent observations more heavily in the calculation
            of the mean and variance, which makes it sensitive to recent changes in the sequence.
        """
        if len(numeric_sequence) == 0:
            raise ValueError("The numeric sequence cannot be empty.")

        # Calculate the mean of the sequence
        mean = sum(numeric_sequence) / len(numeric_sequence)

        # Calculate the squared differences from the mean
        squared_diffs = [(x - mean) ** 2 for x in numeric_sequence]

        # Calculate the variance
        variance = sum(squared_diffs) / len(numeric_sequence)

        # Calculate and return the standard deviation
        standard_deviation = math.sqrt(variance)
        return standard_deviation

    @abstractmethod
    def calculate_winning_amount(
            self,
            winning_number_combination: List[int],
            purchase_number_combinations: List[List[int]],
            **kwargs: Any
    ) -> Tuple[float, int]:
        """
        Calculate the winning amount based on matching combinations.

        :param winning_number_combination: Winning number combination.
        :param purchase_number_combinations: Purchase number combinations.
        :param kwargs: Additional keyword arguments.
        :return: The total winning amount and the count of winning combinations
        """
        pass
