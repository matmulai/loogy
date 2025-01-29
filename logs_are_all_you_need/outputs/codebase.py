```python
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

# Example of usage
if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6, 7]
    print("Given array is", arr)
    merge_sort(arr)
    print("Sorted array is", arr)
```

This code implements the merge sort algorithm in Python. It uses recursion to split the given array into halves and continues to divide until the base case of a single element list is reached. Then, it merges back the elements in a sorted manner. This code should sort the list as expected. Ensure that you call this function in a script or a main function block to test for its proper execution.