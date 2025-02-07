```python
def merge_sort(arr):
    """
    This function sorts an array using the merge sort algorithm.
    """
    if len(arr) > 1:
        # Find the middle of the array
        mid = len(arr) // 2
        
        # Dividing the array elements into 2 halves
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Sorting the first half
        merge_sort(left_half)

        # Sorting the second half
        merge_sort(right_half)

        i = j = k = 0

        # Copy data to temporary arrays L[] and R[]
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Test the merge_sort function
arr = [12, 11, 13, 5, 6, 7]
print("Given array is", arr)

merge_sort(arr)
print("Sorted array is", arr)
```

Known Issues:

1. **Space Complexity:** Merge sort requires additional space proportional to the size of the input array due to the temporary arrays used for merging.
2. **Stable Sort:** The algorithm is stable as it does not change the relative order of elements with equal keys.
3. **Recursive Stack:** This implementation uses a recursive approach which might lead to a stack overflow when sorting very large arrays due to excessive recursion depth in Python. Using an iterative approach or controlling the maximum recursion depth can alleviate this.

This code defines a merge sort algorithm that can sort an array of integers. The test case demonstrates the sorting process. The mentioned known issues should be considered for conscious use in environments with limited resources or specific constraints.