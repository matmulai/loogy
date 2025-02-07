Here is the complete content for a unit test suite for the given merge sort function, using Python's `unittest` framework:

```python
import unittest

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

class TestMergeSort(unittest.TestCase):

    def test_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_reverse_sorted_array(self):
        arr = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_unsorted_array(self):
        arr = [12, 11, 13, 5, 6, 7]
        expected = [5, 6, 7, 11, 12, 13]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_single_element_array(self):
        arr = [1]
        expected = [1]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_empty_array(self):
        arr = []
        expected = []
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_array_with_duplicates(self):
        arr = [3, 6, 2, 6, 1, 6, 3]
        expected = [1, 2, 3, 3, 6, 6, 6]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_large_numbers(self):
        arr = [1000000, 999999, 1000001]
        expected = [999999, 1000000, 1000001]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_mixed_numbers(self):
        arr = [0, -10, 5, -3, 2, 1, 0]
        expected = [-10, -3, 0, 0, 1, 2, 5]
        merge_sort(arr)
        self.assertEqual(arr, expected)

if __name__ == '__main__':
    unittest.main()
```

This test suite includes a variety of test cases that evaluate the `merge_sort` function for different scenarios:
- Sorting an already sorted array.
- Sorting a reverse sorted array.
- Sorting an arbitrary unsorted array.
- Sorting an array with a single element.
- Sorting an empty array.
- Sorting an array with duplicate elements.
- Sorting an array with large numbers.
- Sorting an array with mixed positive, zero, and negative numbers.

These test cases will help ensure that the `merge_sort` function operates correctly across a range of possible inputs.