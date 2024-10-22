# Clickhttp Library for Working with Clickhouse Database via HTTP Protocol

## Features

* Reading DataFrame based on SQL queries
* Executing multiple SQL queries with the return of the last result as a DataFrame
* Automatic creation of a temporary table with data on the MergeTree engine based on the query and returning its name
* Inserting into a table from a DataFrame
* Support for compressed mode (the server accepts and sends data packed in gzip)
* Support for working through a proxy server
* Ability to set a timeout for the session
* Support for DataFrame in formats: dask, numpy, pandas, polars, python, vaex
* Session initialization via Airflow connection ID or manual specification of the connector

## Composition of library

*clickhouse_multiquery*
 — Standalone function for executing multiquery to Clickhouse DBMS without returning data

*ClickHttpSession*
— Class for working with Clickhouse via HTTP protocol

*UserConn*
— NamedTuple object for creating a connection. Contains data for initialization:

* user      — Type: str, client login
* password  — Type: str, client password
* host      — Type: str, host address
* port      — Type: int, port for HTTP connection (typically 8123 with standard server settings)
* database  — Type: str, schema in the database (can be None)

*get_conn*
— Function for retrieving UserConn object based on Airflow Connection ID

*ClickHttpError*
— Base error class

*ClosedError*
— Error when attempting to perform an action after session has been closed

*FrameError*
— Error retrieving DataFrame

*FrameMultiQueryError*
— Error executing multiquery

*InsertError*
— Error executing insert into table

*FrameType*
— Enum that lists the supported DataFrame types.
  It is necessary for determining output data format for read operations when executing the methods read_frame and send_multiquery.
  To select required data type, you need to pass parameter at class: frame_type=FrameType.<your_required_data_type>.
  It is also important to understand that library does not install additional modules and uses those that user has installed independently.
  During library initialization, all uninstalled modules will be displayed in a warning message along with a command for installation.

* dask   — DataFrame as format dask.dataframe.DataFrame
* numpy  — DataFrame as format numpy.ndarray. Column names are absent
* pandas — DataFrame as format pandas.DataFrame
* polars — DataFrame as format polars.DataFrame
* python — Nested list of standard Python objects. Column names are absent
* vaex   — DataFrame as format vaex.dataframe.DataFrameLocal

*Frame*
— NamedTuple object returned when executing the methods read_frame and send_multiquery for ClickHttpSession class

* columns    — list of column names
* types      — list of original data types
* data       — DataFrame containing data
* time_read  — time taken to execute query by Clickhouse server in ms
* bytes_read — number of bytes sent by the server

## Class Methods

    close           — Close the session. Executed when using context manager with.
    execute         — Execute a query to the database without returning a result.
    insert_frame    — Write data from DataFrame to table.
    read_frame      — Return result of query as a DataFrame.
    reopen          — Open a new session. If a session is already open, it will close the current one and open a new one.
    send_multiquery — Execute multiquerн to database and return result of last query as DataFrame.
    set_proxy       — Specify a proxy server for connection. Running without parameters removes a proxy setting if it was previously specified.
    temp_query      — Create a temporary table with data based on sended query and return its name.

## Static Methods, Nested Objects, and Attributes

    change_mode     — Static method. Changes the query execution mode (compression/no compression).
    chunk_size      — Attribute. Size of the chunks of the sent frame in bytes, default is 50 MB. Can be specified during class initialization.
    database        — Attribute. Schema in the Clickhouse database. The value is taken from the UserConn object or Airflow connection_id. Set during class initialization.
    frame_type      — Enum object FrameType, default is FrameType.pandas. Set during class initialization.
    headers         — Headers of the transmitted requests. Formed during class initialization, contains personal data.
    is_closed       — Attribute. Boolean, True when the session is open.
    is_compressed   — Attribute. Boolean indicating whether packets are compressed for sending and receiving, default is True. Can be specified during class initialization.
    output_format   — Static method. Displays the selected method for obtaining the DataFrame from the server.
    proxy           — Attribute. String address of the proxy server, default is absent. Can be specified during class initialization.
    session_id      — Attribute. Unique ID of the current session as a string representation of UUIDv4. Created automatically.
    sess            — Instance of the requests.Session class.
    timeout         — Attribute. Time to wait for a response from the server in seconds, default is 10. Can be specified during class initialization.
    url             — Attribute. Address of the server, formed during class initialization.

## Declared magic methods of the class (without description)

    __enter__
    __exit__
    __repr__
    __str__

## Installation (Windows/Linux/MacOs)

### Install from directory

```shell
pip install .
```

### Install from git

```shell
pip install git+https://github.com/0xMihalich/clickhttp
```

### Install from pip

```shell
pip install clickhttp
```

## Examples

Examples of usage are described in examples.ipynb

[Download examples.ipynb file from link on Google Drive](https://drive.google.com/file/d/1NiZtHW8Nmj1IUBTwmLm8exbkttydhkG5/)

## FAQ

Q: What is this needed for?

A: In some ETL processes, there is a need to create multiple CTEs followed by data aggregation into a final selection.
Clickhouse does not create CTEs; instead, it executes the same query declared in the WITH section every time in all places of the main query,
wasting RAM resources and server computing power. An alternative to CTEs could be a temporary table with data, but Clickhouse does not
support executing multiple queries. This library serves as an alternative to clickhouse-client and clickhouse_driver.
It does not claim to be the best; however, some features of this solution may seem interesting.
The main goal of the library is to execute multiple queries within a single session, addressing the issue of creating
a Temporary Table with subsequent data retrieval.

Q: Why does clickhttp.ClickHttpSession not work in asynchronous mode if Clickhouse, as developers claim, is asynchronous?

A: Although the Clickhouse server operates in asynchronous mode, operations within a single session can only be synchronous,
and the delay between requests within a single session should not exceed 60 seconds.

Q: Why are only backports.zoneinfo and requests listed in the requirements.txt file? Where are numpy, pandas, polars, dask, vaex?

A: Starting from version 0.0.5, all imports not directly related to the operation of Session->Request | Session->Response have been excluded
from explicit imports and are now added only if they were previously installed by the user, as not all users utilize all declared DataFrame
formats in their work. Some may only need pandas, others numpy, while some use vaex. Now, importing the library will issue warning messages
about missing components but will continue to function. If a user does not even have numpy, all received and transmitted data will be obtained
in the format of nested Python lists; otherwise, there will be an option to choose the type of DataFrame received,
with the default class initialized as pandas.DataFrame.

Q: How can I check which DataFrame types are currently available to me?

A: You can use the built-in method get_names for clickhttp.FrameType. Executing this method will provide you with a list of available formats.

Q: I installed the missing library, but when executing clickhttp.FrameType.get_names(), it is not there. What should I do?

A:

1. Ensure that the library is installed in the correct version of Python or in the correct virtual environment.
2. Make sure that the interpreter has been restarted after installing the library.
3. After completing the first two steps, re-execute clickhttp.FrameType.get_names() and verify that the required format has appeared.

## Version History

### 0.1.2

* All docstrings have been translated into English
* Documentation and examples are now available in two languages
* Added MIT License
* Updated setup.py

### 0.1.1

* Added streaming for reading Big Data
* Refactored code to fix flake8 warnings
* Fixed warnings in README.md
* Resolved compatibility issues with earlier versions of Python
* Added Python versions 3.7 - 3.13 to workflow tests

### 0.1.0

* Added a function to check if the connection object belongs to NamedTuple
* Added a simple check for the ClickHttpSession class in workflow tests
* Changed the protocol to HTTPS for port 443
* The formatter function now removes extra spaces
* Added the project URL to setup.py

### 0.0.9

* Fixed the connection object check
* Added simple tests for workflows
* Corrected a typo in CHANGELOG.md

### 0.0.8

* Added SQL query formatting (with comment removal)
* Added a dependency for the third-party library sqlparse (SQL formatter) in requirements.txt
* Allowed the use of third-party NamedTuple objects for creating the connection object
* Increased default CHUNK_SIZE to 50 MB
* Project mirror moved to GitHub

### 0.0.7

* Fixed the missing requirements.txt file error

## 0.0.6

* Some code fixes
* Moved FAQ.txt and CHANGELOG.md to README.md
* Uploaded examples.ipynb to Google Drive
* First package publication on pip

## 0.0.5

* Added FAQ.txt
* Added CHANGELOG.md
* Updated README.md
* Updated examples.ipynb
* Added an optional use_columns attribute for the insert_table method
* Minor code fixes

## 0.0.4

* The version with pre-installed dask and vaex packages has been moved to a separate branch
* Only the requests module dependency remains in requirements.txt
* DTYPE and FrameType objects are created dynamically based on user-installed components
* Refactored some functions and methods
* Added an execute method for sending commands that do not require returning a frame

## 0.0.3

* Added support for dask.dataframe.DataFrame
* Added support for vaex.dataframe.DataFrameLocal
* The version supporting only pandas.DataFrame and polars.DataFrame has been moved to a separate branch

### 0.0.2

* Fixed logging output for some messages
* Replaced logging.warning with logging.info for message output during method execution

### 0.0.1

First version of the library
