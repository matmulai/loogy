Below is a set of unit tests written in Python using the `unittest` framework to test the merge sort implementation provided:

```python
import unittest

class TestMergeSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element_list(self):
        self.assertEqual(merge_sort([1]), [1])

    def test_already_sorted_list(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_list(self):
        self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_list(self):
        self.assertEqual(merge_sort([38, 27, 43, 3, 9, 82, 10]), [3, 9, 10, 27, 38, 43, 82])

    def test_list_with_duplicates(self):
        self.assertEqual(merge_sort([4, 5, 4, 3, 3, 2, 1]), [1, 2, 3, 3, 4, 4, 5])

    def test_float_numbers(self):
        self.assertEqual(merge_sort([3.1, 2.2, 5.5, 1.0, 8.8]), [1.0, 2.2, 3.1, 5.5, 8.8])

    def test_list_with_negative_numbers(self):
        self.assertEqual(merge_sort([-3, -1, -7, 0, 5, 2]), [-7, -3, -1, 0, 2, 5])

    def test_alternating_large_small_numbers(self):
        self.assertEqual(merge_sort([1000, -1000, 500, -500, 0]), [-1000, -500, 0, 500, 1000])

    def test_merge_function(self):
        self.assertEqual(merge([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])

if __name__ == '__main__':
    unittest.main()
```

### Explanation
- `test_empty_list`: Tests the sorting of an empty list.
- `test_single_element_list`: Tests the sorting of a list with one element.
- `test_already_sorted_list`: Tests sorting of an already sorted list.
- `test_reverse_sorted_list`: Tests sorting of a list sorted in descending order.
- `test_unsorted_list`: Tests sorting of a completely unsorted list.
- `test_list_with_duplicates`: Tests sorting of a list with duplicate elements.
- `test_float_numbers`: Tests sorting of a list with floating-point numbers.
- `test_list_with_negative_numbers`: Tests sorting of a list containing negative numbers.
- `test_alternating_large_small_numbers`: Tests sorting of a list with large and small numbers alternated.
- `test_merge_function`: Directly tests the `merge` function with two pre-sorted sublists.

These comprehensive tests cover various edge cases and typical use cases to ensure the correctness and robustness of the merge sort implementation.