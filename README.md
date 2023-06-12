# Shortest-path Planning for Guadalajara's MiBici Public Bike System

This repository uses station locations in Guadalajara's public bike system (MiBici) to build a weighted undirected graph and perform shortest-path planning between two arbitrary locations. Data was obtained from https://www.mibici.net/es/datos-abiertos/ and it is stored within `data` folder in `nomenclatura_2023_05.csv` file.

## Displaying stations
The only information being used is the latitude and longitude for each station in the `.csv` file. For each station, latitude and longitude coordinates are mapped into $(x,y)$ coordinates, in kilometers, centered at the middle point of all the stations. This is done via function `to_global` within `utils.py` module. Here's the plot for the resulting resulting spatial distribution of the stations:

![locations](https://github.com/a-lemus96/mibici-gdl/assets/95151624/fc85087c-632b-426a-b3c1-c55c107d6364)

## Building a 2D-tree for efficient spatial search queries
Using the spatial information computed from the previous section, a variance-based 2D-tree is built to perform efficient search queries. The splitting direction along the building procedure is determined by the highest among the variances along $x$ and $y$ coordinates. Tree class definition and its corresponding methods are defined within `tree.py` module. Here's the plot for the resulting 2D-tree defined by the station locations:

![2d-tree](https://github.com/a-lemus96/mibici-gdl/assets/95151624/75664194-bb78-4d04-97de-dbf7d824503d)

In the previous plot, 4 random nodes are colored arbitrarily along with the bounding rectangular region they define.

## Building a graph using $K$-nearest neighbors
`Tree` class definition within `tree.py` module contains a method called `nearest_neighbors` that allows one to compute efficiently the $K$-nearest neighbors to a query point. This method is used to build a weighted undirected graph with all the stations serving as nodes, with the edges given by the closest $K$ nodes to each node, and with the weights given by the Euclidean distances between them. Graph utilities are defined in `graph.py` module. The resulting graph, for $K = 3$ looks like this:

![graph](https://github.com/a-lemus96/mibici-gdl/assets/95151624/e408cf52-40e6-4b1a-ab13-cbe02cf5cf1e)

## Shortest-path planning between two arbitrary points
This graph representation allows one to perform queries of the form: "What is the shortest path between two arbitrary positions $p$ and $q$?". To compute a solution to these queries, both $p$ and $q$ nodes are connected to the graph by computing the $K$ closest nodes and running either Dijkstra's or Bellman-Ford algorithm.  Both implementations are defined in `graph.py` module. Here's  the output for two random endpoints:

![path](https://github.com/a-lemus96/mibici-gdl/assets/95151624/e8c67072-e6fa-4861-b393-715a1dd1478f)

## Running the tests
Simply run `python main.py -file FILE -method METHOD` where `-file` is the filename that must be contained inside `data` folder and `-method` can take as values either `dijkstra` or `belman-ford` as argument values. All the output graphs are stored within `out` folder.
