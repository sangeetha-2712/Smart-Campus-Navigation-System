SMART CAMPUS NAVIGATION SYSTEM

DSA concepts:
- Weighted, undirected graph
- Adjacency-list representation
- Dijkstra's shortest path algorithm
- Min-heap priority queue using Python heapq

Requirements:
- Python 3
- Tkinter (normally included with Python)
- No third-party packages

Run:
    python smart_campus_navigation.py

How to use:
1. Select a starting location and destination.
2. Click Find Shortest Path.
3. The shortest route is highlighted in red and its distance is shown.
4. Use Add New Location to add a vertex.
5. Use Add Road / Distance to add a two-way weighted edge.

Sample locations:
Main Gate, Department Block, Canteen, Library, Hostel.
The sample distances are illustrative. Replace them with actual campus distances.

Graph storage:
graph[location][neighbour] = distance
Each road is stored in both directions because the sample campus roads are two-way.

Complexity (adjacency list + binary min-heap):
Time: O((V + E) log V)
Space: O(V + E)
V = number of locations; E = number of roads.

Dijkstra's algorithm requires non-negative edge weights.
