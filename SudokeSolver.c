#include<stdio.h>
#include<stdlib.h>

void print(int arr[][9]){
    for (int i = 0; i < 9; ++i){
        for (int j = 0; j < 9; ++j){
            printf("%d,", arr[i][j]);
        }
        printf("\n");
    }
}


void solveVert(int arr[][9], int pos[],int x, int y){
    for (int i = 0; i < 9; ++i){
        int k = arr[i][x];
        if (k){
            pos[k-1] = 0;
        }
    }
}

void solveHori(int arr[][9], int pos[],int x, int y){
    for (int i = 0; i < 9; ++i){
        int k = arr[y][i];
            if(k){
                pos[k-1] = 0;
            }    
        }
    }

void solveNear(int arr[][9], int pos[],int x, int y){
    int x1 = x/3;
    int y1 = y/3;
    for (int i = 0; i < 3; ++i){
        for (int j = 0; j <3 ; ++j){
            int k = arr[y1*3+i][x1*3+j];
            if (k){
                pos[k-1] = 0;
            }
        }
    }
}

int solve(int arr[][9], int *i){
    if (*i != 81){
        int x = *i%9;
        int y = *i/9;
        *i = *i + 1;
        if (arr[y][x]){
            if (solve(arr, i)){
                return 1;
            } else{
                *i = *i - 1;
                return 0;
            }
        }
        else{
            int pos[9] = {1,1,1,1,1,1,1,1,1};
            solveHori(arr,pos,x,y);
            solveVert(arr,pos,x,y);
            solveNear(arr,pos,x,y);
            int j = 0;
            while(j<9){
                if (pos[j]){
                    arr[y][x] = j+1;
                    if (solve (arr, i)){
                        return 1;
                    }
                    else{
                        *i = *i - 1;
                        arr[y][x] = 0;
                    }
                }
                ++j;
            }
        }   
        return 0;
    }
    return 1; 
}


int main(){
    int puzzle[9][9] = {{6,0,0,4,1,0,3,0,8},
                        {8,0,5,0,6,3,4,0,0},
                        {7,3,0,0,2,0,0,0,1},
                        {0,0,6,1,5,7,0,0,2},
                        {5,7,0,0,0,4,1,0,6},
                        {1,2,0,0,9,6,0,4,0},
                        {3,0,0,0,0,0,0,8,0},
                        {0,6,9,0,3,0,0,5,0},
                        {0,0,7,0,4,0,0,1,0}};
    int i = 0;
    solve(puzzle, &i);
    print(puzzle);
    return 0;
}