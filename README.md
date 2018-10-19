# 3162_SNA_G17


## QuickStart Guide 
##### Windows Users
GUI Option ->
Click on run_windows.bat
or use the command line to run the same file

##### Linux Users
Run the run_linx.sh script. 


This batch file will activate the Python 3.6 Virtual Environment and open the local web page using your default browser. It may take a few moments for the web server to initialize, if the page does not automatically initialize, reload the page after 10 seconds. 
If you wish to use a different browser, the main page is at http://127.0.0.1/vis/


## Running Tests

- Navigate to the root directory

- Activate the Linux Python Virtual Environment using 

        Linux: source .env/bin/activate

        Windows: .env_windows\Scripts\activate

- Use the following command to discover and run the unit tests

        python -m unittest discover



## Using the GUI
The navigation menu at the top has the following functionality.
From left to right
* Load Graph
   * This allows switching between graph datasets. 
   * Currently available are Enron, Reddit and Slashdot. 
* Reload Graph
    * This reloads the currently loaded graph
* Graph Algorithms
    * This allows use of the graph algorithms that are available. Some may take some time. 
* Graph Actions
    * This allows modification of the graph. *_To be Implemented_*

## Class Documentation

Class documentation built by Sphynx and hosted by Jekyll

https://sologuy3.github.io/3162_SNA_G17/genindex.html

## Project tree
The documentation sit under the /docs folder

The .env and .env_windows folders are Python Virtual Environments.

The /archive folder is for scrapped scripts and data

The /sna folder is the main project. Under this folder
- graph - contains the main graph, node and algorithms classes and the respective tests.
- migrations - not used
- static - contains static files used by the webserver, js and css.
- parsers - contains the one-time parsers used to interpret and clean the data.
- templates/graph_sna - contains the index.html file

Files:
- admin.py, apps.py, models.py, tests.py : are all django application files.
- urls.py defines how API/webserver endpoints are handled
- views.py contains functions that are called by url.py to handle web requests.

#### Folder structure breakdown below.


.
 * [docs](./docs)
   * [sphinx](./docs/sphinx)
     * [buildnmove.sh](./docs/sphinx/buildnmove.sh)
 * [open_site.bat](./open_site.bat)
 * [README.md](./README.md)
 * [requirements.txt](./requirements.txt)
 * [run_windows.bat](./run_windows.bat)
 * [sna](./sna)
   * [db_ops.py](./sna/db_ops.py)
   * [__init__.py](./sna/__init__.py)
   * [manage.py](./sna/manage.py)
   * [out.txt](./sna/out.txt)
   * [db.sqlite3](./sna/db.sqlite3)
   * [sna](./sna/sna)
     * [__init__.py](./sna/sna/__init__.py)
     * [settings.py](./sna/sna/settings.py)
     * [urls.py](./sna/sna/urls.py)
     * [wsgi.py](./sna/sna/wsgi.py)
   * [graph_sna](./sna/graph_sna)
   * [admin.py](./sna/graph_sna/admin.py)
   * [apps.py](./sna/graph_sna/apps.py)
   * [__init__.py](./sna/graph_sna/__init__.py)
   * [models.py](./sna/graph_sna/models.py)
   * [parsers](./sna/graph_sna/parsers)
     * [base_parser.py](./sna/graph_sna/parsers/base_parser.py)
     * [enron_parser.py](./sna/graph_sna/parsers/enron_parser.py)
     * [__init__.py](./sna/graph_sna/parsers/__init__.py)
     * [reddit_parser.py](./sna/graph_sna/parsers/reddit_parser.py)
     * [slashdot_parser.py](./sna/graph_sna/parsers/slashdot_parser.py)
   * [sna](./sna/graph_sna/sna)
     * [__init__.py](./sna/graph_sna/sna/__init__.py)
     * [settings.py](./sna/graph_sna/sna/settings.py)
     * [urls.py](./sna/graph_sna/sna/urls.py)
     * [wsgi.py](./sna/graph_sna/sna/wsgi.py)
   * [tests.py](./sna/graph_sna/tests.py)
   * [templates](./sna/graph_sna/templates)
     * [graph_sna](./sna/graph_sna/templates/graph_sna)
     * [index.html](./sna/graph_sna/templates/graph_sna/index.html)
   * [urls.py](./sna/graph_sna/urls.py)
   * [views.py](./sna/graph_sna/views.py)
   * [graph](./sna/graph_sna/graph)
     * [__init__.py](./sna/graph_sna/graph/__init__.py)
     * [node.py](./sna/graph_sna/graph/node.py)
     * [sample_graphs.py](./sna/graph_sna/graph/sample_graphs.py)
     * [testGraph.py](./sna/graph_sna/graph/testGraph.py)
     * [testNode.py](./sna/graph_sna/graph/testNode.py)
     * [testRegression.py](./sna/graph_sna/graph/testRegression.py)
     * [algorithms.py](./sna/graph_sna/graph/algorithms.py)
     * [graph.py](./sna/graph_sna/graph/graph.py)
     * [testAlgorithms.py](./sna/graph_sna/graph/testAlgorithms.py)
                 
   * [migrations](./sna/graph_sna/migrations)
     * [0001_initial.py](./sna/graph_sna/migrations/0001_initial.py)
     * [__init__.py](./sna/graph_sna/migrations/__init__.py)
                                                    .cpython-35.pyc
