# Version History

## 0.1.2

* All docstrings have been translated into English
* Documentation and examples are now available in two languages
* Added MIT License
* Updated setup.py

## 0.1.1

* Added streaming for reading Big Data
* Refactored code to fix flake8 warnings
* Fixed warnings in README.md
* Resolved compatibility issues with earlier versions of Python
* Added Python versions 3.7 - 3.13 to workflow tests

## 0.1.0

* Added a function to check if the connection object belongs to NamedTuple
* Added a simple check for the ClickHttpSession class in workflow tests
* Changed the protocol to HTTPS for port 443
* The formatter function now removes extra spaces
* Added the project URL to setup.py

## 0.0.9

* Fixed the connection object check
* Added simple tests for workflows
* Corrected a typo in CHANGELOG.md

## 0.0.8

* Added SQL query formatting (with comment removal)
* Added a dependency for the third-party library sqlparse (SQL formatter) in requirements.txt
* Allowed the use of third-party NamedTuple objects for creating the connection object
* Increased default CHUNK_SIZE to 50 MB
* Project mirror moved to GitHub

## 0.0.7

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

## 0.0.2

* Fixed logging output for some messages
* Replaced logging.warning with logging.info for message output during method execution

## 0.0.1

First version of the library
