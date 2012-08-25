#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <stack>
#include <vector>
#include <algorithm>
using namespace std;

typedef int Item;
typedef int Info;

class Node {
  int serialgen() {
    static int g_serial = 0;
    return g_serial++;
  }

 public:
  Node(Item k, Info i, Node *ll, Node *rr) {
    key = k; info = i;
    left = ll; right = rr;
    serial = serialgen();
    is_nil = false;
  }
  ~Node() {
    if (left && !left->is_nil) delete left;
    if (right && !right->is_nil) delete right;
  }

  static Node *nilNode() {
    Node *node = new Node(0, 0, NULL, NULL);
    node->left = node->right = node;
    node->is_nil = true;
    return node;
  }

  Item key; Info info;
  Node *left, *right;
  int serial;
  bool is_nil;
};

class Tree {
 public:
  Tree() {
    z = Node::nilNode();
    head = new Node(-1, 0, NULL, z);
  }
  ~Tree() {
    delete head;
    delete z;
  }

  void insert(Node *r, Node* n) {
    if (r->key >= n->key) {
      if (r->left && r->left != z)
        insert(r->left, n);
      else
        r->left = n;
    } else {
      if (r->right && r->right != z)
        insert(r->right, n);
      else
        r->right = n;
    }
  }

  Node *next(Node **n) {
    //printf("NEXT %p : %p %p ; %p\n", n, n->left, n->right, z);
    // left != z && right != z
    Node *it = *n;
    if (it->left == z) {
      Node *clone = new Node(it->key, it->info, z, z);
      *n = it->right;
      // delete it;
      return clone;
    } else { // n->left->left != z
      return next(&(it->left));
    }
  }

  void erase(Node *r, Item k) {
    if (r->key > k) {
      if (r->left && r->left != z) {
        if (r->left->key == k) {
          // [found]  r->left.
          Node *f = r->left;
          //     me
          //   (it)
          // left right
          if (f->left != z && f->right != z) {
            // f has 2
            //            Node *it = f->left;
            Node *c = next(&f->right);
            c->left = f->left;
            c->right = f->right;
            r->left = c;
          } else if (f->left == z) { // 右に子１人
            r->left = f->right;
          } else if (f->right == z) { // 左に子１人
            r->left = f->left;
          } else {
            r->left = z;
          }
          //delete f;
        } else {
          erase(r->left, k);
        }
      }
      // else ... not found.
    } else if (r->key < k) {
      if (r->right && r->right != z) {
        if (r->right->key == k) {
          // [found] r->right
          Node *f = r->right;
          //     me
          //      (it)
          //    left right
          if (f->left != z && f->right != z) {
            // f has 2
            //Node *it = f->left;
            Node *c = next(&f->right);
            c->left = f->left;
            c->right = f->right;
            r->right = c;
          } else if (f->left == z) { // 右に子１人
            r->right = f->right;
          } else if (f->right == z) { // 左に子１人
            r->right = f->left;
          } else {
            r->right = z;
          }
          //delete f;
        } else {
          erase(r->right, k);
        }
      }
      // else ... not found.
    }
  }

  void insert(Item k, Info i) {
    insert(head, new Node(k, i, z, z));
  }
  void erase(Item k) {
    erase(head, k);
  }

  void dot(const char *prefix, int file_id) {
    // "PREFIX_%03d.dot"
    int name_size = strlen(prefix) + 4 + 1;
    char name[name_size], name_dot[name_size + 4], name_gif[name_size + 4];
    snprintf(name, name_size, "%s_%03d", prefix, file_id);
    snprintf(name_dot, name_size + 4, "%s.dot", name);
    snprintf(name_gif, name_size + 4, "%s.gif", name);

    FILE *fp = fopen(name_dot, "w");
    if (!fp) return;

    fputs("graph sample {\n", fp);
    fputs("  graph [ center = \"false\", ordering = out, ranksep = 0.2, nodesep = 0.5 ];\n", fp);
    fputs("  node [ fontname = \"Courier\", fontsize = 14, shape = circle, width = 0.2, height = 0.2, margin = 0.01 ];\n", fp);
    fputs("  edge [ color = black, weight = 1 ];\n", fp);

    stack<Node*> st;
    // printf("HEAD %p : %p %p ; %p\n", head, head->left, head->right, z);
    Node *n = head->right;  // ignore the head (-1)
    while ((n && n != z) || !st.empty()) {
      // printf("WI %d\n", n->key);
      if (n && n != z) {
        // if (n->key >= 0) {
        if (n->key == coloring) 
          fprintf(fp, "  N%d [ label = \"%d\", style = \"filled\", fillcolor = \"%s\" ]\n", n->serial, n->key, color);
        else
          fprintf(fp, "  N%d [ label = \"%d\" ]\n", n->serial, n->key);

        if (n->left && n->left != z) {
          fprintf(fp, "  N%d -- N%d;\n", n->serial, n->left->serial);
        } else {
          fprintf(fp, "  L%d [ shape = box, width = 0.1, height = 0.1, label = \"\" ];\n", n->serial);
          fprintf(fp, "  N%d -- L%d;\n", n->serial, n->serial);
        }
        st.push(n);
        n = n->left;  // if (n == z) n = NULL;
      } else {
        n = st.top(); st.pop();
        if (n->right && n->right != z) {
          fprintf(fp, "  N%d -- N%d;\n", n->serial, n->right->serial);
        } else {
          fprintf(fp, "  R%d [ shape = box, width = 0.1, height = 0.1, label = \"\" ];\n", n->serial);
          fprintf(fp, "  N%d -- R%d;\n", n->serial, n->serial);
        }
        n = n->right;
      }
    }
    fputs("}\n", fp);

    fclose(fp);
    /*
    char cmd[100];
    snprintf(cmd, 100, "dot -Tgif %s -o %s", name_dot, name_gif);
    system(cmd);
    */
  }

  Node *head, *z;
  int key;
  int coloring;
  const char *color;
};

void shuffle(vector<int>& ar) {
  int N = ar.size();
  for (int i=0; i<N; ++i) {
    int j = rand() % N;
    int k = rand() % N;
    if (j != k) swap(ar[j], ar[k]);
  }
}

int main(int argc, char **argv) {
  Tree tree;

  int file_id = 0;

  srand(clock());

  enum { ASC, DESC, RAND };
  int mode = RAND;
  if (argc >= 2) {
    if (strcmp(argv[1], "asc") == 0) mode = ASC;
    else if (strcmp(argv[1], "desc") == 0) mode = DESC;
    else if (strcmp(argv[1], "rand") == 0) mode = RAND;
  }

  int maxnum = atoi(argv[2]);
  if (maxnum <= 0) maxnum = 30;

  // tree.dot("t", file_id++);

  vector<int> st(maxnum); for (int i=0; i<maxnum; i++) st[i] = i;

  switch (mode) {
    case RAND:
      shuffle(st);
      break;
    case DESC:
      reverse(st.begin(), st.end());
      break;
    case ASC: default:
      break;
  }

  tree.color = "#9999ff";
  tree.coloring = -1;
  tree.dot("t", file_id++);

  for (int i=0; i<maxnum; i++) {
    int val = st[i];

    //tree.coloring = -1;
    //tree.dot("t", file_id++);

    tree.insert(val, val);

    tree.coloring = val;
    tree.dot("t", file_id++);
  }

  tree.coloring = -1;
  tree.dot("t", file_id++);

  shuffle(st);
  //sort(st.begin(), st.end());

  tree.color = "#ff9999";

  for (int i=0; i<maxnum; i++) {
    int val = st[i];

    tree.coloring = val;
    tree.dot("t", file_id++);

    tree.erase(val);

    // tree.coloring = -1;
    // tree.dot("t", file_id++);
  }

  tree.coloring = -1;
  tree.dot("t", file_id++);

  return 0;
}
