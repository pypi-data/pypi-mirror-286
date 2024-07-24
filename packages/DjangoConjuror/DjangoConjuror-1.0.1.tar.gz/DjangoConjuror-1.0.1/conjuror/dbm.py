from .runcommands import *

def configure_database(args):
    project_path = find_manage_py_path(os.getcwd(), args.name)
    if project_path:
        update_database_settings(project_path, args)
        print("Database configuration updated.")
    else:
        print("No Django project directory found. Please run this inside a Django project or specify a path.")

def update_database_settings(project_path, args):
    directory_name = os.path.basename(project_path)
    settings_path = os.path.join(project_path, directory_name, 'settings.py')
    if not os.path.exists(settings_path):
        print("Settings file not found. Please make sure it exists in the main app directory.")
        sys.exit(1)

    with open(settings_path, 'r') as f:
        settings = f.readlines()

    
    new_db_config = generate_db_config(args)
    
    start_index = next((i for i, line in enumerate(settings) if 'DATABASES =' in line), None)
    if start_index is not None:
        end_index = start_index
        brace_count = 0
        for i, line in enumerate(settings[start_index:], start_index):
            if '{' in line:
                brace_count += line.count('{')
            if '}' in line:
                brace_count -= line.count('}')
            if brace_count == 0 and i > start_index:
                end_index = i + 1
                break

        settings[start_index:end_index] = new_db_config
    
    with open(settings_path, 'w') as file:
        file.writelines(settings)

def generate_db_config(args):
    db_config = {
        'postgres': f"""DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': '{args.dbname}',
                'USER': '{args.username}',
                'PASSWORD': '{args.password}',
                'HOST': '{args.host}',
                'PORT': '{args.port if args.port else "5432"}',
            }}
        }}\n""",
        'mysql': f"""DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '{args.dbname}',
                'USER': '{args.username}',
                'PASSWORD': '{args.password}',
                'HOST': '{args.host}',
                'PORT': '{args.port if args.port else "3306"}',
            }}
        }}\n""",
        'sqlite': f"""DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, '{args.dbname}.sqlite3'),
            }}
        }}\n"""
    }
    return db_config[args.dbtype].split('\n')
