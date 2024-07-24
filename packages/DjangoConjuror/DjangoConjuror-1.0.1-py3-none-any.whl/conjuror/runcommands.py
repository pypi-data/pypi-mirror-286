import subprocess
import shutil
import sys
import os

def create_django_project(path, project_name):
    try:
        os.chdir(path)
        subprocess.run(["python", "-m", "django", "startproject", project_name], check=True)
        create_constants(path, project_name)
        print(f"Django project '{project_name}' created successfully in {path}")
    except subprocess.CalledProcessError:
        print(f"Failed to create Django project. Make sure Django is installed and the path is correct.")
    except Exception as e:
        print(f"Error creating Django project: {e}")

def create_constants(path,project_name):
    constants_filename = os.path.join(path,project_name)
    constants_filename = os.path.join(constants_filename,"constants.py")
    constant_name = "SERVER_IP"
    constant_value = "127.0.0.1"
    constants = [
        ("SERVER_IP", "127.0.0.1"),
        ("SITE_URL", "127.0.0.1"),
        ("SITE_MARKETING_URL", "http://127.0.0.1:8000"),
        ("EMAIL_HOST", ""),
        ("EMAIL_USE_TLS", ""),
        ("EMAIL_PORT", ""),
        ("EMAIL_HOST_USER", ""),
        ("EMAIL_HOST_PASSWORD", ""),
    ]
    with open(constants_filename, 'w') as file:
        for constant_name, constant_value in constants:
            file.write(f"{constant_name} = '{constant_value}'\n")
    if path is None:
        path = find_manage_py_path(os.getcwd(),project_name)
        if path is None:
            print("No Django project found. Please specify a project path or run this command inside a Django project directory.")
            return
    directory_name = os.path.basename(path)
    settings_file_path = os.path.join(path, project_name ,project_name, 'settings.py')
    if not os.path.exists(settings_file_path):
        print("Settings file not found. Please make sure it exists in the main app directory.")
        sys.exit(1)


    with open(settings_file_path, 'r') as f:
        lines = f.readlines()

    import_os_line_index = None
    for i, line in enumerate(lines):
        if 'from pathlib import Path' in line:
            import_os_line_index = i

    if import_os_line_index is not None and 'import constants' not in lines:
        lines.insert(import_os_line_index + 1, "import constants\n")

    lines.append("\n")
    lines.append("AUTH_USER_MODEL = 'djangoauth.User'\n")
    lines.append("EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'\n")
    lines.append("SITE_URL = constants.SITE_URL\n")
    lines.append(f"EMAIL_HOST = constants.EMAIL_HOST\n")
    lines.append(f"EMAIL_USE_TLS = constants.EMAIL_USE_TLS\n")
    lines.append(f"EMAIL_PORT = constants.EMAIL_PORT\n")
    lines.append(f"EMAIL_HOST_USER = constants.EMAIL_HOST_USER\n")
    lines.append(f"EMAIL_HOST_PASSWORD = constants.EMAIL_HOST_PASSWORD\n")

    for i, line in enumerate(lines):
        if 'INSTALLED_APPS = ' in line.strip():
            import_os_line_index = i + 1 
        
    if import_os_line_index is not None:
        if import_os_line_index is not None:
            lines.insert(import_os_line_index, f"'djangoauth',\n")

    with open(settings_file_path, 'w') as f:
        f.write("".join(lines))

    setup_dir = os.path.abspath(os.path.dirname(__file__))
    copy_folders(os.path.join(setup_dir,'Auth'),os.path.join(path,project_name))
    add_url(os.path.join(path,project_name,project_name,'urls.py'))

    
def add_url(file_path,app_names=None):
    new_import_line = "from django.urls import path, include\n"
    new_url_pattern = "    path('auth/', include('djangoauth.urls')),"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    import_line_found = False
    for index, line in enumerate(lines):
        if line.startswith("from django.urls import path"):
            lines[index] = new_import_line
            import_line_found = True
            break

    for line in lines:
        if line == new_import_line:
            break
        elif not import_line_found:
            lines.insert(0, new_import_line)
        

        
    insert_index = None
    for index, line in enumerate(lines):
        if line.strip().startswith("path('admin/'"):
            insert_index = index + 1
            break

    if not app_names:
        if insert_index is not None:
            lines.insert(insert_index, new_url_pattern)
    else:
        for app_name in app_names:
            apps = app_name.split(',')
            for app in apps:
                lines.insert(insert_index, f"    path('{app}/', include('{app}.urls')),\n")


    with open(file_path, 'w') as file:
        file.writelines(lines)

def create_urls_file(file_path,app_name):
    content = f"""\
from django.urls import path
from {app_name} import views

app_name = '{app_name}'

urlpatterns = [
    # Add your URL patterns here
]
"""

    with open(file_path, 'w') as file:
        file.write(content)
    
def create_django_apps(app_names,project_name=None, path=None):
    if path is None:
        path = find_manage_py_path(os.getcwd(),project_name)
        if path is None:
            print("No Django project found. Please specify a project path or run this command inside a Django project directory.")
            return

    try:
        project_path = os.path.join(path)
        add_url(os.path.join(path,project_name,'urls.py'),app_names)
        os.chdir(project_path)
        for app_name in app_names:
            apps = app_name.split(',')
            for app in apps:
                subprocess.run(["python", "manage.py", "startapp", app], check=True)
                update_settings_file_apps(project_path,app)
                create_urls_file(os.path.join(path,app,'urls.py'),app)
                print(f"Django app '{app}' created successfully in {project_path}")
    except subprocess.CalledProcessError:
        print("Failed to create Django app. Make sure you are inside a Django project directory and Django is installed.")
    except Exception as e:
        print(f"Error creating Django app: {e}")

def update_settings_file_apps(project_path,app):
    directory_name = os.path.basename(project_path)
    settings_file_path = os.path.join(project_path, directory_name, 'settings.py')
    if not os.path.exists(settings_file_path):
        print("Settings file not found. Please make sure it exists in the main app directory.")
        sys.exit(1)

    with open(settings_file_path, 'r') as f:
        lines = f.readlines()
    apps_line_index = None
    for i, line in enumerate(lines):
        if 'INSTALLED_APPS = ' in line.strip():
            apps_line_index = i + 1 
        
    if apps_line_index is not None:
        if apps_line_index is not None:
            lines.insert(apps_line_index, f"'{app}',\n")

    with open(settings_file_path, 'w') as f:
        f.write("".join(lines))

def create_static_and_templates_folders(project_path):
    static_path = os.path.join(project_path, 'static')
    templates_path = os.path.join(project_path, 'templates')

    os.makedirs(static_path, exist_ok=True)
    os.makedirs(templates_path, exist_ok=True)

def update_settings_file(project_path):
    directory_name = os.path.basename(project_path)
    settings_file_path = os.path.join(project_path, directory_name, 'settings.py')
    if not os.path.exists(settings_file_path):
        print("Settings file not found. Please make sure it exists in the main app directory.")
        sys.exit(1)

    with open(settings_file_path, 'r') as f:
        lines = f.readlines()

    static_line_index = None
    templates_line_index = None
    import_os_line_index = None
    for i, line in enumerate(lines):
        if 'from pathlib import Path' in line:
            import_os_line_index = i
        if 'STATIC_URL' in line:
            static_line_index = i
        if 'TEMPLATES = ' in line.strip():
            templates_line_index = i + 1 

    if import_os_line_index is not None and 'import os' not in lines:
        lines.insert(import_os_line_index + 1, "import os\n")

    if static_line_index is not None:
        lines.insert(static_line_index + 2, 'STATICFILES_DIRS = [BASE_DIR, "static"]\n')

    if templates_line_index is not None:
        while 'DIRS' not in lines[templates_line_index]:
            templates_line_index += 1 
        lines[templates_line_index] = lines[templates_line_index].replace(
            "'DIRS': []",
            "'DIRS': [BASE_DIR, 'templates']",
        )
    

    with open(settings_file_path, 'w') as f:
        f.write("".join(lines))

def copy_folders(source_dir, destination_dir):
    try:
        for item in os.listdir(source_dir):
            item_path = os.path.join(source_dir, item)
            destination_path = os.path.join(destination_dir, item)
            
            if os.path.isdir(item_path):
                shutil.copytree(item_path, destination_path)
            else:
                shutil.copy2(item_path, destination_path)    

        print("DjangoAuth Created successfully!")        
    except FileNotFoundError:
        print(f"Source directory '{destination_dir}' not found.")
    except FileExistsError:
        print(f"Destination directory '{destination_dir}' already exists.")

def find_manage_py_path(start_path, project_name=None):
    for root, dirs, files in os.walk(start_path):
        if 'manage.py' in files:
            if project_name:
                folder_name = os.path.basename(root)
                if folder_name == project_name:
                    return root
            else:
                return root
    return None
