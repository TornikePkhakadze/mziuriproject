from django.test import TestCase
# from django.core.cache import cache
# import random
# import time

# def expencive_calculations():
#     numbers = [i for i in range(10_000_000)]
#     random.shuffle(numbers)
#     numbers.sort()
#     return numbers

# def get_list():
#     start = time.time()
#     sorted_list = cache.get('numbers')
#     if not sorted_list:
#         sorted_list = expencive_calculations()
#         cache.set('numbers', sorted, 60 * 5)
#     end = time.time()
#     print(end-start)
#     return sorted_list

# get_list()
# get_list()

