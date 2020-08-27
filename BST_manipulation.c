#include <stdio.h>
#include<stdlib.h>

typedef struct Node{
    int val;
    struct Node *left;
    struct Node *right;
}Node;

Node *toBTree(int arr[], int s, int e){
    // making a balanced binary search tree given a sorted list
    Node *nd = malloc(sizeof(Node));
    if (e - s > 1){
        int split = (e+s)/2;
        nd -> val = arr[split];
        nd -> left = toBTree(arr, s, split);
        nd -> right = toBTree(arr, split+1, e);
        return nd;
    }
    else if (e - s == 1){
        nd -> val = arr[s];
        nd -> left = NULL;
        nd -> right = NULL;
        return nd;
    }
}   

void recursivePrint(Node *n){
    // recursive print of a binary tree
    if (n == NULL){
        return;
    } else{
        recursivePrint(n->left);
        printf("%d " , n->val);
        recursivePrint(n->right);
    }
}

void stackPrint(Node *n, int size){
    // in order print of a binary tree using a pseudo-stack
    Node *q[size];
    q[0] = n;
    n = n -> left;
    int p = 1;
    while (p > 0 || n != NULL){
        if (n == NULL){
            Node *new = q[p-1];
            printf("%d ", new->val);
            n = new->right;
            --p;
        }
        else {
            q[p] = n;
            n = n->left;
            ++p;
        }
    }
}

void rotatePrint(Node *n){
    // in order print of a binary tree using iteration and without a stack
    while (n != NULL){
        while (n -> left != NULL){
        Node *l = n -> left;
        n -> left = l -> right;
        l -> right = n;
        n = l;
        }
        printf("%d ", n-> val);
        n = n -> right;
    }
}

Node *recursiveInvert(Node *n){
    // invert a binary tree recursively
    if (n != NULL){
        Node *t = n -> left;
        n -> left = recursiveInvert(n->right);
        n -> right = recursiveInvert(t);
    }
    return n;
}

void *queueInvert(Node *n, int size){
    // invert a binary tree with a queue
    if (n!= NULL){
        Node *p[size];
        int start = 0;
        int end = 1;
        p[0] = n;
        while(end - start != 0){
            n = p[start];
            ++start;
            Node *t = n -> left;
            n -> left = n->right;
            n -> right = t;
            if (n->right != NULL){
                p[end] = n->right;
                ++end; 
            }
            if (n->left != NULL){
                p[end] = n -> left;
                ++end;
            }
        }
    }
    
}




int main(){
    int size = 33;
    int lst[size];
    for(int i = 0; i < size; ++i){
        lst[i] = i;
    }
    Node *n = toBTree(lst,0,size);
    recursivePrint(n);
    printf("\n");
    stackPrint(n, size);
    printf("\n");
    rotatePrint(n);
    recursiveInvert(n);
    queueInvert(n, size);
    rotatePrint(n);
    return 0;
}