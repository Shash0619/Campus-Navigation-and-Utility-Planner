class Building:
    def __init__(self, bid, name, location):
        self.id = bid
        self.name = name
        self.location = location

# ---------------- BST IMPLEMENTATION ----------------

class BSTNode:
    def __init__(self, building):
        self.data = building
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, building):
        self.root = self._insert(self.root, building)

    def _insert(self, root, building):
        if root is None:
            return BSTNode(building)
        if building.id < root.data.id:
            root.left = self._insert(root.left, building)
        else:
            root.right = self._insert(root.right, building)
        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.data.id, root.data.name)
            self.inorder(root.right)

    def preorder(self, root):
        if root:
            print(root.data.id, root.data.name)
            self.preorder(root.left)
            self.preorder(root.right)

    def postorder(self, root):
        if root:
            self.postorder(root.left)
            self.postorder(root.right)
            print(root.data.id, root.data.name)

# ---------------- AVL TREE ----------------

class AVLNode:
    def __init__(self, building):
        self.data = building
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def get_height(self, root):
        return root.height if root else 0

    def get_balance(self, root):
        return self.get_height(root.left) - self.get_height(root.right)

    def rotate_left(self, z):
        y = z.right
        T = y.left
        y.left = z
        z.right = T
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T = y.right
        y.right = z
        z.left = T
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, building):
        if not root:
            return AVLNode(building)

        if building.id < root.data.id:
            root.left = self.insert(root.left, building)
        else:
            root.right = self.insert(root.right, building)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and building.id < root.left.data.id:
            return self.rotate_right(root)

        if balance < -1 and building.id > root.right.data.id:
            return self.rotate_left(root)

        if balance > 1 and building.id > root.left.data.id:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        if balance < -1 and building.id < root.right.data.id:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

# ---------------- GRAPH (Adjacency List + Matrix) ----------------

class Graph:
    def __init__(self, n):
        self.n = n
        self.matrix = [[0]*n for _ in range(n)]
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v, w):
        self.matrix[u][v] = w
        self.matrix[v][u] = w
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def bfs(self, start):
        visited = [False]*self.n
        q = [start]
        visited[start] = True
        while q:
            u = q.pop(0)
            print(u, end=" ")
            for v, _ in self.adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        print()

    def dfs(self, start):
        visited = [False]*self.n
        self._dfs(start, visited)
        print()

    def _dfs(self, u, visited):
        visited[u] = True
        print(u, end=" ")
        for v, _ in self.adj[u]:
            if not visited[v]:
                self._dfs(v, visited)

# ---------------- DIJKSTRA SHORTEST PATH ----------------

import heapq

def dijkstra(graph, start):
    dist = [float('inf')] * graph.n
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        for v, w in graph.adj[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist

# ---------------- KRUSKAL MST ----------------

def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

def union(parent, rank, x, y):
    xr = find(parent, x)
    yr = find(parent, y)
    if rank[xr] < rank[yr]:
        parent[xr] = yr
    elif rank[xr] > rank[yr]:
        parent[yr] = xr
    else:
        parent[yr] = xr
        rank[xr] += 1

def kruskal(edges, n):
    edges.sort(key=lambda x: x[2])
    parent = [i for i in range(n)]
    rank = [0]*n
    mst = []

    for u, v, w in edges:
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            mst.append((u, v, w))
            union(parent, rank, x, y)
    return mst

# ---------------- EXPRESSION TREE ----------------

class ExpNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def eval_tree(root):
    if root.left is None and root.right is None:
        return int(root.val)
    a = eval_tree(root.left)
    b = eval_tree(root.right)
    if root.val == '+': return a + b
    if root.val == '-': return a - b
    if root.val == '*': return a * b
    if root.val == '/': return a // b

# ---------------- SAMPLE DEMO ----------------

if __name__ == "__main__":
    b1 = Building(10, "Library", "Block A")
    b2 = Building(5, "Admin", "Block B")
    b3 = Building(20, "CSE Dept", "Block C")

    bst = BST()
    bst.insert(b1)
    bst.insert(b2)
    bst.insert(b3)
    print("BST Inorder:")
    bst.inorder(bst.root)

    avl = AVL()
    root = None
    root = avl.insert(root, b1)
    root = avl.insert(root, b2)
    root = avl.insert(root, b3)

    g = Graph(4)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, 4)
    g.add_edge(2, 3, 6)

    print("BFS:")
    g.bfs(0)
    print("DFS:")
    g.dfs(0)

    print("Dijkstra from node 0:", dijkstra(g, 0))

    edges = [(0, 1, 2), (1, 2, 4), (2, 3, 6)]
    print("MST:", kruskal(edges, 4))

    root = ExpNode('*')
    root.left = ExpNode('5')
    root.right = ExpNode('+')
    root.right.left = ExpNode('2')
    root.right.right = ExpNode('3')
    print("Expression Tree Eval:", eval_tree(root))
