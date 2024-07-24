#!/usr/bin/env python

import argparse
import os
import subprocess
from .runcommands import  *
from .dbm import *

def main():
    parser = argparse.ArgumentParser(description="Create & Manage Django projects.")
    
    parser.add_argument("-c", "--create", action="store_true", help="Create a new Django project")
    parser.add_argument("-p", "--path", type=str, help="Specify the path where to create the project")
    parser.add_argument("-n", "--name", type=str, default="myproject", help="Specify the name of the Django project")
    parser.add_argument("-a", "--apps", nargs='*', help="Create one or more Django apps by specifying their names")
    parser.add_argument("-s", "--setup-static-templates", action="store_true", help="Setup static and templates folders")
    parser.add_argument("-d", "--database", action="store_true", help="Change the database configuration")
    parser.add_argument("--dbtype", choices=['postgres', 'mysql', 'sqlite'], help="Type of database")
    parser.add_argument("--username", help="Database username")
    parser.add_argument("--password", help="Database password")
    parser.add_argument("--dbname", help="Database name")
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--port", help="Database port")


    args = parser.parse_args()
    
    if args.create:
        name = args.name
        path = args.path if args.path else os.getcwd()
        create_django_project(path, name)

    if args.apps:
        name = args.name
        path = args.path if args.path else find_manage_py_path(os.getcwd(), name)
        if not path:
            print("No Django project directory found. Please run this inside a Django project or specify a path.")
        else:
            if not args.apps:
                args.apps = ['app'] 
            create_django_apps(args.apps,name, path)

    if args.setup_static_templates:
        project_path = find_manage_py_path(os.getcwd())
        if project_path:
            create_static_and_templates_folders(project_path)
            update_settings_file(project_path)
            print("Static and templates folders setup complete.")
        else:
            print("No Django project directory found. Please run this inside a Django project.")

    if args.database:
        configure_database(args)


if __name__ == "__main__":
    main()
