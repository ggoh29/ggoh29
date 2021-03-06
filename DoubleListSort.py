# Sort a list of indexes pointing to a list of values
# Done by quicksort, mergesort and heapsort
# Takes two list, one list of index and one list of values
# Only sorts the list of indexes
# Ideally, both list should be the same size
# In reality, as long as min(index) > -1 and max(index) < len(values) it should be fine
import math

# Quicksort


def twoListQuickSort(index, values, start, end):
        if end - start > 1:
            pivot = values[index[start]]
            counter = start
            for i in range(start+1, end):
                if values[index[i]] < pivot:
                    temp = index[counter]
                    index[counter] = index[i]
                    index[i] = temp
                    counter += 1
            if counter == start:
                twoListQuickSort(index, values, start + 1, end)
            elif counter == end-1:
                twoListQuickSort(index, values, start, end-1)
            else:
                twoListQuickSort(index, values, counter, end)
                twoListQuickSort(index, values, start, counter)


def twoListQuick(index, values):
    length = len(index)
    if length != len(values):
        raise Exception('length mismatch')
    twoListQuickSort(index, values, 0, length)


# Heapsort

def singleListPopMax(index, counter):
    temp = index[0]
    index[0] = index[counter]
    index[counter] = temp
    singleListHeapify(index, 1, counter)


def singleListHeapify(index, i, mx):
    if i * 2 + 1 <= mx:
        l = i * 2 - 1 
        r = l + 1
        if index[l] > index[r]:
            pointer = l
        else:
            pointer = r
        i -= 1
        if index[pointer] > index[i]:
            temp = index[pointer]
            index[pointer] = index[i]
            index[i] = temp
            singleListHeapify(index, pointer+1, mx)
    elif i * 2 == mx:
        i -= 1
        mx -= 1
        if index[i] < index[mx]:
            temp = index[mx]
            index[mx] = index[i]
            index[i] = temp

        
def singleListHeap(index):
    length = len(index)
    start = math.floor(length/2)+1
    for i in range(start, 0, -1):
        singleListHeapify(index, i, length)
    for j in range(length-1, -1, -1):
        singleListPopMax(index,  j)
        
# double list
        
        
def twoListHeap(index):
    length = len(index)
    start = math.floor(length/2)+1
    for i in range(start, 0, -1):
        twoListHeapify(index, i, length)
    for j in range(length-1, -1, -1):
        twoListPopMax(index,  j)


def twoListPopMax(index, values, counter):
    temp = index[0]
    index[0] = index[counter]
    index[counter] = temp
    twoListHeapify(index, values, 1, counter)


def twoListHeapify(index, values, i, mx):
    if i * 2 + 1 < mx:
        l = i * 2 - 1
        r = i * 2
        if values[index[l]] > values[index[r]]:
            pointer = l
        else:
            pointer = r
        i -= 1
        if values[index[pointer]] > values[index[i]]:
            temp = index[pointer]
            index[pointer] = index[i]
            index[i] = temp
            twoListHeapify(index, values, pointer + 1, mx)
    elif i * 2 == mx:
        i -= 1
        mx -= 1
        if values[index[i]] > values[index[mx]]:
            temp = index[mx]
            index[mx] = index[i]
            index[i] = temp


def twoListHeap(index, values):
    length = len(index)
    if length != len(values):
        raise Exception('length mismatch')
    start = math.floor(length/2)
    for i in range(start, 0, -1):
        twoListHeapify(index, values, i, length)
    for j in range(length-1, -1, -1):
        twoListPopMax(index, values, j)

# Mergesort
# Just trying a unorthodox method of mergesort
# It works but the complexity seems wrong so will need to fix it some day

def twoListMergeSort(index,values):
    length = len(index)
    if length != len(values):
        raise Exception('length mismatch')
    temp = index.copy()
    counter = 1
    while True:
        for i in range(0, int(length/2 * counter)):
            l,r = 0,0
            left = (2 * i) * counter
            right = (2 * i + 1) * counter
            if right > length:
                continue
            while l < counter and r < counter and right + r < length:
                if values[temp[left + l]] < values[temp[right + r]]:
                    index[left + l + r] = temp[left + l]
                    l += 1
                else:
                    index[left + l + r] = temp[right + r]
                    r += 1
            while l < counter:
                index[left + l + r] = temp[left + l]
                l += 1
            while r < counter and right + r < length:
                index[left + l + r] = temp[right + r]
                r += 1
        counter *= 2
        if counter < length:
            temp, index = index, temp
        else:
            break

