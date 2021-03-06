# Project Description
This web application executes the [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on a relational database. The application uses the [SQLite](https://sqlite.org/about.html) library to implement a transactional SQL database engine. SQLite is convenient because it doesn't require setting up a separate database server and it is built-in to [Python](https://www.python.org/).

The application's directory is called [crudy](crudy), and the project layout looks like this:

```
├── db.py
├── __init__.py
├── main.py
├── menu.py
├── orders.py
├── pool.py
├── schema.sql
├── static
│   └── style.css
└── templates
    ├── base.html
    ├── index.html
    ├── menu
    │   ├── create.html
    │   ├── update.html
    │   └── view.html
    ├── orders
    │   ├── create.html
    │   ├── update.html
    │   └── view.html
    └── pool
        ├── create.html
        └── view.html
```

### Connect to the Database
The connection to the SQLite database is established via [sqlite3.connect()](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect). 

- [db.py](crudy/db.py#L10-L13)

### Data Tables
The database schema is created before we store or retrieve any data.

- [schema.sql](crudy/schema.sql)

### CRUD Operations
The CRUD operations are implemented in several places of the application. Follow the links below for details.

- [menu.py](crudy/menu.py)
  - [create](https://github.com/jruizvar/project/blob/master/crudy/menu.py#L32)
  - [read](https://github.com/jruizvar/project/blob/master/crudy/menu.py#L21)
  - [update](https://github.com/jruizvar/project/blob/master/crudy/menu.py#L49)
  - [delete](https://github.com/jruizvar/project/blob/master/crudy/menu.py#L61)

# Instructions
The application was written in **Python 3.6** with the microframework [Flask](http://flask.pocoo.org). We recommend [Miniconda](https://conda.io/miniconda.html) package management system to create the development environment.

- Create Environment
```
conda create -n crudy python=3 mongodb
source activate crudy
```

- Install Dependencies

```
pip install flask flask-bootstrap flask-wtf pandas pymongo
``` 

- Download Project
```
git clone https://github.com/jruizvar/project.git
cd project
```

- Environment Setup
```
export FLASK_APP=crudy
export FLASK_ENV=development
```

- Initialize Databases
```
flask init-db
```
The directory `instance` containing the file `crudy.sqlite` is created.
Run the [MongoDB](http://api.mongodb.com/python/current/tutorial.html) service in another terminal.
```
mkdir instance/mongodata
mongod --dbpath instance/mongodata
```

- Execute Application
```
flask run
```

By default, the application starts running on http://localhost:5000/

![](doc/crudy.gif)
