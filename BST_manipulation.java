import java.util.LinkedList;

public class BST_manipulation {

    public static class Node {

        public int data;
        public Node left;
        public Node right;

        Node(int data){
            this.data = data;
            left = null;
            right = null;
        }

        Node(int data, Node left, Node right){
            this.data = data;
            this.left = left;
            this.right = right;
        }
    }

    public static Node listToBST(int nums[], int s, int e){
        // convert an arraylist into a BST
        if (e-s>1){
            int mid = (e+s)/2;
            if (e-s==2){
                Node l = new Node(nums[s]);
                return new Node(nums[e-1], l, null);
            } else {
                Node l = listToBST(nums, s, mid);
                Node r = listToBST(nums, mid+1, e);
                return new Node(nums[mid], l,r);
            }
        } else {
            return new Node(nums[s]);
        }
    }

    public static void solve1(Node root){
        // print out all nodes in order iteratively and without a stack
        if (root != null){

            Node cur = root;
            while (cur != null){
                if (cur.left == null){
                    System.out.println(cur.data);
                    cur = cur.right;
                }
                else {
                    Node t = cur.left;
                    cur.left = t.right;
                    t.right = cur;
                    cur = t;
                }
            }
        }
    }

    public static void solve2(Node root){
        // print out all nodes in order iteratively and with a stack
        LinkedList<Node> l = new LinkedList<Node>();
        Node cur = root;
        while(!l.isEmpty() || cur != null){
            while (cur != null){
                l.push(cur);
                cur = cur.left;
            }
            cur = l.pop();
            System.out.println(cur.data);
            cur = cur.right;
        }
    }

    public static void main(String[] args){
        int size = 25;
        int nums[] = new int [25];
        for (int i = 0; i < size; ++i) {
            nums[i] = i;
        }
        Node root = listToBST(nums, 0 , size);
        solve1(root);
        solve2(root);
    }
}


