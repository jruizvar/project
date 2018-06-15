# Project Description
This web application executes the [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) operations on a relational database. The application uses the [SQLite](https://sqlite.org/about.html) library to implement a transactional SQL database engine. SQLite is convenient because it doesn't require setting up a separate database server and it is built-in to **Python**.

### Connect to the Database
The connection to the SQLite database is established via [sqlite3.connect()](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect). 

- [db.py](myapp/db.py#L10-L13)

### Data Tables
The database schema is created before we store or retrieve any data.

- [schema.sql](myapp/schema.sql)

### CRUD Operations
The CRUD operations are implemented in several places of the application. Follow the links below for details.

- [Create](https://github.com/jruizvar/project/blob/master/myapp/menu.py#L32)
- [Read](https://github.com/jruizvar/project/blob/master/myapp/menu.py#L21)
- [Update](https://github.com/jruizvar/project/blob/master/myapp/menu.py#L49)
- [Delete](https://github.com/jruizvar/project/blob/master/myapp/menu.py#L61)

# Instructions
The application was written in **Python 3.6** with the microframework [Flask](http://flask.pocoo.org). We recommend [Miniconda](https://conda.io/miniconda.html) package management system to create the development environment.

- Create Environment
```
conda create -n flask python=3
source activate flask
```

- Install Dependencies

```
pip install flask flask-bootstrap flask-wtf
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

- Initialize Database
```
flask init-db
```

- Execute Application
```
flask run
```

By default, the application starts running on http://localhost:5000/
