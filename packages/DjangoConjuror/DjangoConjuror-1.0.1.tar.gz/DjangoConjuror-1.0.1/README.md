# DjangoConjuror

DjangoConjuror is a command-line tool designed to simplify the setup and management of Django projects. It provides straightforward commands to create new projects, add applications, configure databases, and much more.

## Features

- **Create Django Projects:** Initialize new projects with a custom name at a specified location.
- **Add Django Apps:** Add one or more applications to your Django project with ease.
- **Database Configuration:** Customize database settings with options for PostgreSQL, MySQL, or SQLite.
- **Setup Static and Templates:** Set up directories for static files and templates automatically.
- **CRUD Operations:** Incorporate CRUD functionalities for create, read, update, and delete operations.
- **Authentication and Account Management:** Includes full authentication workflows like login, signup, and logout, along with account recovery.
- **Email Functionality:** Set up SMTP for email operations related to account management such as password reset.
- **Custom User Models and Templates:** Use custom user models and templates for streamlined account management.

## Installation

Install DjangoConjuror via pip:

```bash
pip install DjangoConjuror
```

## Usage

### Create a New Project

```bash
conjuror --create --path /path/to/project --name myproject
```

- `--create` or `-c`: Start the creation of a new Django project.
- `--path` or `-p`: Specify the project's directory.
- `--name` or `-n`: Name the new project (defaults to "myproject" if not specified).

### Add Applications

```bash
conjuror --apps app1 app2 app3
```
OR

```bash
conjuror -a app1 app2 app3
```

This command adds the specified apps to your Django project.

### Setup Authentication , Account Management, Static and Template Directories

```bash
conjuror --setup-static-templates
```
OR

```bash
conjuror -s
```
This command is same as setup  initializes login, signup, logout, and password recovery functionalities using Custom templates and models.

### Configure Database

```bash
conjuror --database --dbtype postgres --username user --password pass --dbname dbname --host localhost --port 5432
```
OR

```bash
conjuror -d --dbtype postgres --username user --password pass --dbname dbname --host localhost --port 5432
```

At Default sqlite will be integrated As the db.

### CRUD Operations

```python
from conjuror.Crud import crud

# Example usage
crud.StoreData(model, dict)
crud.FetchData(model, dict)
crud.UpdateData(model, filters, dict)
crud.DeleteData(model, dict)
crud.GetData(model, dict)
```

Model is your django model on which you want to perform crud operations , and dict is a dictionary containg keys as your models fields and value as the data . 

```python
from models import student
from conjuror.Crud import crud
# Example 
crud.StoreData(student, {"name":"student","rollno":1})
```

### Use As a Single Click Project Setup

```bash

# If you want to create a django project in the current Directory

conjuror -c -n myproject -a app1,app2 -s -d --dbtype postgres --username user --password pass --dbname dbname --host localhost --port 5432

# if you want to create a django project in a specific directory 

conjuror -c -n myproject -a app1,app2 -s -p /path/to/my/directory -d --dbtype postgres --username user --password pass --dbname dbname --host localhost --port 5432

```