from setuptools import setup, find_packages

setup(
    name='DjangoConjuror',
    version='1.0.1',
    packages=find_packages(include=['conjuror', 'conjuror.*']),
    install_requires=[
        'django',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'conjuror = conjuror.cli:main',
        ],
    },
    package_data={
        'conjuror.Auth': [
            'djangoauth/email_templates/*',
            'static/assets/css/*',
            'static/assets/js/*',
            'static/assets/images/*',
            'static/assets/fonts/*',
            'templates/auth/*',
        ],
    },
    include_package_data=True,
    author='Hassan Farooq',
    author_email='hassanfarooq0122@gmail.com',
    description='This tool is created to ease the Django Development. Developers can use this to create and manage their Django Projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # if your README is Markdown
    url='https://www.linkedin.com/in/hassan-farooq-65ba88280',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
