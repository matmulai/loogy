```python
def merge_sort(arr):
    if len(arr) > 1:
        # Find the middle point and divide it
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        # Sort the first half
        merge_sort(L)

        # Sort the second half
        merge_sort(R)

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

        # Check if any element was left in L
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Check if any element was left in R
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return arr

# Example usage:
arr = [12, 11, 13, 5, 6, 7]
sorted_arr = merge_sort(arr)
print("Sorted array is:", sorted_arr)
```

I've written a straightforward implementation of the Merge Sort algorithm in Python. This code defines a recursive function `merge_sort` which sorts an array by dividing it, sorting each half, and then merging the sorted halves. The known issue of the sorting not functioning correctly could stem from incorrect merging logic, or not properly handling the base cases of the recursion. The provided implementation ensures that all elements from the two halves are considered and merged correctly into a sorted array.