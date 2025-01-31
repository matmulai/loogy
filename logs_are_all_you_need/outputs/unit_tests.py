To write unit tests for the `merge_sort` function, we'll use Python's `unittest` framework. We'll test the function with various test cases to ensure it handles different scenarios such as sorting an already sorted list, sorting a list with duplicate elements, and handling an empty list. Here is a list of unit tests for the `merge_sort` function in Python:

```python
import unittest

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

class TestMergeSort(unittest.TestCase):
    def test_sorted_list(self):
        arr = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(merge_sort(arr), expected)

    def test_reverse_list(self):
        arr = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(merge_sort(arr), expected)

    def test_unsorted_list(self):
        arr = [12, 11, 13, 5, 6, 7]
        expected = [5, 6, 7, 11, 12, 13]
        self.assertEqual(merge_sort(arr), expected)

    def test_empty_list(self):
        arr = []
        expected = []
        self.assertEqual(merge_sort(arr), expected)

    def test_single_element_list(self):
        arr = [1]
        expected = [1]
        self.assertEqual(merge_sort(arr), expected)

    def test_duplicate_elements_list(self):
        arr = [3, 1, 2, 1, 3]
        expected = [1, 1, 2, 3, 3]
        self.assertEqual(merge_sort(arr), expected)

    def test_large_numbers_list(self):
        arr = [100000, 99999, 1000, 999]
        expected = [999, 1000, 99999, 100000]
        self.assertEqual(merge_sort(arr), expected)

    def test_negative_numbers_list(self):
        arr = [-1, -3, -2, 0]
        expected = [-3, -2, -1, 0]
        self.assertEqual(merge_sort(arr), expected)

if __name__ == '__main__':
    unittest.main()
```

These tests cover a variety of scenarios, including sorted and unsorted lists, lists with duplicates, empty lists, lists with a single element, and lists containing negative and large numbers. By running these tests, we can validate the correctness of the `merge_sort` function.