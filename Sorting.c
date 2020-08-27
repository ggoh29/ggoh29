#include<stdio.h>
#include<stdlib.h>
// need to know the length of the array the first time the function is called

// mergesort

void mergesort(int arr[], int s, int e){
    if (e-s > 1){
        int split = (e-s)/2;

        int left[split]; 
        int right[e - s - split];

        for (int i = s; i < s+split; ++i){
            left[i-s] = arr[i];            
        } 
        for (int j = split+s; j < e; ++j){
            right[j-split-s] = arr[j];
        }
        mergesort(left, 0, split);
        mergesort(right, 0, e-s-split);

        int i = 0;
        int j = 0;
        while (i < split && j < e - s - split){
            if (left[i] <= right[j]){
                arr[j+i] = left[i];
                i++;
            } else{
                arr[j+i] = right[j];
                j++;
            }
        }
        if(i == split){
            for (int n = j; n < e-s-split; ++n){
                arr[i+n] = right[n];
            }
        } else {
            for (int n = i; n < split; ++n){
                arr[j+n] = left[i];
            }
        }
    }
}

// heapsort


void heapify(int arr[], int i, int max){
    int pointer;
    if (i * 2 + 1 < max){
        int l = 2 * i;
        int r = 2 * i + 1;
        if (arr[l] > arr[r]){
            pointer = l;
        } else {
        pointer = r;
        }
        if (arr[pointer] > arr[i]){
            int tmp = arr[pointer];
            arr[pointer] = arr[i];
            arr[i] = tmp;
            heapify(arr,pointer,max);
        }
    } 
    else if (i * 2 == max) {
        if (arr[i * 2] > arr[i]){
            int tmp = arr[i * 2];
            arr[i * 2] = arr[i];
            arr[i] = tmp;
        } 
    }
}

void popmax(int arr[], int i){
    int tmp = arr[0];
    arr[0] = arr[i];
    arr[i] = tmp;
    heapify(arr, 0, i-1);
}

void heapsort(int arr[], int max){
    for (int j = max/2; j > -1; --j){
        heapify(arr,j,max);
    }
    print(arr,max);
    for (int k = max-1; k > 0; --k){
        popmax(arr, k);
    }
}

// quicksort

void quicksort(int arr[], int s, int e){
    if (e-s > 1){
        int partition = arr[s];
        int counter = 0;
        for (int i = s+1; i < e; ++i){
            if (arr[i] < partition){
                int t = arr[s+counter];
                arr[s + counter] = arr[i];
                arr[i] = t;
                ++counter; 
            }
        }
        if (counter == 0){
            quicksort(arr, s+1,e);
        }
        else if (counter == e - s -1){
            quicksort(arr, s, e-1);
        } 
        else 
        {
            quicksort(arr,s,s+counter+1);
            quicksort(arr,s+counter,e);
        }
    } 
}