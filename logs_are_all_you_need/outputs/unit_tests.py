Here is a list of unit tests for the `merge_sort` function in Python, implemented using the unittest framework:

```python
import unittest

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]        # Dividing the elements into 2 halves
        R = arr[mid:]

        merge_sort(L)        # Sorting the first half
        merge_sort(R)        # Sorting the second half

        i = j = k = 0
        
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left in L
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Checking if any element was left in R
        while j < len(R):
            arr[k] = R[j]
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

    def test_array_with_duplicates(self):
        arr = [4, 5, 1, 2, 2, 3]
        expected = [1, 2, 2, 3, 4, 5]
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

    def test_large_numbers(self):
        arr = [1000000, 500000, 10000, 5000, 1000]
        expected = [1000, 5000, 10000, 500000, 1000000]
        merge_sort(arr)
        self.assertEqual(arr, expected)

    def test_identical_elements(self):
        arr = [2, 2, 2, 2, 2]
        expected = [2, 2, 2, 2, 2]
        merge_sort(arr)
        self.assertEqual(arr, expected)

if __name__ == "__main__":
    unittest.main()
```

This unit test code covers various scenarios, including:

1. Already sorted array.
2. Reverse sorted array.
3. Unsorted array.
4. Array with duplicate values.
5. Single element array.
6. Empty array.
7. Array with large numbers.
8. Array with identical elements.

Each test case checks whether the `merge_sort` function correctly sorts the array, asserting the expected output with the actual result. Run this script as a standalone program to execute these tests.