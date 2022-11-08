
def partition(arr,low,high):
    # choose pivot
    pivot = arr[high]

    # pointer for greater element
    i = low - 1

    # looping through all element to find element can be swapped
    # beside the pivot, because we want to compare it to pivot
    for j in range(low,high):
        if(arr[j] <= pivot):
            # move i pointer to next element
            i = i + 1

            # swapping element i and j
            (arr[i], arr[j]) = (arr[j], arr[i])

    #swap pivot element with next of greatest pointer now
    (arr[i+1], arr[high]) = (arr[high], arr[i+1])

    #return the position where the partition done (where pivot placed now)
    return i+1

#perform quicksort
def doQuicksort(arr, low, high):
    if low<high:
        # find pivot
        piv = partition(arr, low, high)

        #recursive call on the left of pivot
        doQuicksort(arr, low, piv-1)
        
        #recursive call on the right of pivot
        doQuicksort(arr, piv+1, high)

def quickSort(arr):
    arr_copied = arr[:]
    doQuicksort(arr_copied, 0, len(arr_copied)-1)
    return arr_copied

data = [8,7,6,1,0,9,2]
print("Unsorted: ", data)
print("Sorted: ", quickSort(data))
print("Unsorted: ", data)


