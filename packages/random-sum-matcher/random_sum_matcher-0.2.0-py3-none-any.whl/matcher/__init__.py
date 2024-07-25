# simple_adder/__init__.py
# random_sum_matcher/__init__.py

from .main import random_sum_matcher

matching_sums = random_sum_matcher(count=100, range_start=1, range_end=100)
for sum_value, count in matching_sums.items():
    print(f"Sum: {sum_value}, Combinations: {count}")