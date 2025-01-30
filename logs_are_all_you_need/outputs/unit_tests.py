Here is a list of unit tests for the merge sort implementation in Python:

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
    
    def test_empty_array(self):
        arr = []
        merge_sort(arr)
        self.assertEqual(arr, [])

    def test_single_element_array(self):
        arr = [1]
        merge_sort(arr)
        self.assertEqual(arr, [1])
        
    def test_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        merge_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
        
    def test_reverse_sorted_array(self):
        arr = [5, 4, 3, 2, 1]
        merge_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
        
    def test_random_array(self):
        arr = [3, 2, 5, 4, 1]
        merge_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
        
    def test_duplicate_elements(self):
        arr = [1, 3, 2, 3, 3]
        merge_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 3, 3])
        
    def test_negative_numbers(self):
        arr = [-1, -3, -2, -4, -5]
        merge_sort(arr)
        self.assertEqual(arr, [-5, -4, -3, -2, -1])
        
    def test_mixed_numbers(self):
        arr = [3, -1, 2, -5, 4]
        merge_sort(arr)
        self.assertEqual(arr, [-5, -1, 2, 3, 4])

# Run the tests
if __name__ == '__main__':
    unittest.main()
```

Each test case handles various scenarios, including empty arrays, single-element arrays, presorted arrays, reverse sorted arrays, random arrays, arrays with duplicate elements, and arrays with negative numbers. These tests help ensure the functionality and robustness of the merge sort implementation.