# Morpheus API

Morpheus's REST API.

## How to run 

### Prerequisites

 To run this in your local environment you must install the following dependencies first:

 - Python 3.7+
 - PostgreSQL 10+
 
### Installation

 Once you've installed all the dependencies follow this steps:

 1) Edit your configuration file and fill in all the reelevant options.
 
 2) Run the application configuration:
   
  ```
  python3 setup.py 
  ```

 This will create your database, run the migrations and download all necesary python packages. 
  
 3) Run the application 

 ```
 python3 main.py
 ```
 
 ### Adding users
 
 Use moderator control panel (modcp) to add users. 
 
```
python3 modcp.py
```

Pick a username, name, valid email and password.
 
 ## Testing
 
 This application uses pyunit as its test suite.
 To run the tests from the command line use:
 
 ```python
 python -m unittest
 ```