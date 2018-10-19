.. CompSci17_SNA documentation master file, created by
   sphinx-quickstart on Fri Aug  3 04:41:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CompSci17_SNA's documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2


**Welcome to the Documentation**
To view the Graph Module documentation, please use the "Index" or "Module Index" links below.

**API**
The Django View API currently only supports three API calls.

The base URL for the API is http://localhost/vis/ or http://127.0.0.1/vis/

**GET** /reddit *or* /slashdot *or* /enron *or* /reload
This API call will load the given dataset into the view. This is done by
1. Loading the given dataset into the graph module on the server side
2. Reloading the web view

**GET** /load_graph.json
This API call will trigger a JSON response which will be interpreted by D3 to visualise the graph. The server will pick up the currently loaded graph, use the graph.dump_graph() method to generate a JSON file in a format that D3 can read, and pass this in its response to the GET request.

**GET** /algorithm
*Query Strings* **(Required)**
?type=
Valid values:
   'node_count'; Returns the Node Count of the Graph
   'edge_count'; Returns the Edge Count of the Graph
   'diameter';  Returns the Diameter of the Graph
   'minimum_average_path';  Returns the Minimum Average Path of the Graph
   'mode_path_length'; Returns the Mode Path Length of the Graph
   'average_edges_per_node'; Returns the Average Edges Per Node in the Graph
   'discover_components'; Runs DFS to discover nodes, and returns a nested list of components.
   'acc'; Returns the average clustering coefficient of the graph
   'scc'; Returns the strongly connected components of the graph (as a nested list)
   'holes';

This request will perform the algorithm given in the "type" query string, and return a formatted string response.


**POST** /algorithm





.. automodule:: graph_sna
   :members:

.. automodule:: graph_sna.graph
   :members:

.. automodule:: graph_sna.graph.graph
   :members:

.. autoclass:: algorithms.GraphAlgorithms
   :members:

.. autoclass:: graph_sna.graph.algorithms.GraphAlgorithms
   :members:

.. automodule:: node
   :members:

.. automodule:: graph_sna.graph.node
   :members:

.. automodule:: graph_sna.graph.node
   :members:


* :ref:`genindex`
* :ref:`modindex`

