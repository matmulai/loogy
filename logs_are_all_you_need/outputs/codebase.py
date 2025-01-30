Here's a complete implementation of the merge sort algorithm in Python, taking into account the reported issue where the list wasn't being sorted correctly:

```python
def merge_sort(arr):
    if len(arr) > 1:
        # Finding the middle of the array
        mid = len(arr) // 2
        
        # Dividing the array elements into 2 halves
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sorting both halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Merging the sorted halves
        i = j = k = 0
        
        # Copy data to temp arrays left_half and right_half
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

# Example usage:
if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6, 7]
    print("Given array is", arr)
    merge_sort(arr)
    print("Sorted array is", arr)
```

This implementation divides the array into two halves, recursively sorts each half, and then merges the sorted halves together. Care has been taken to handle all edge cases in the merging step, ensuring that the algorithm sorts correctly. 

Make sure to test this corrected implementation with various input scenarios to verify its correctness. If any issues arise, they should be related to specific edge cases or input types rather than the core logic of the merge sort itself.