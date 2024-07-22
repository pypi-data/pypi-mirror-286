import os
import subprocess
from setuptools import setup, find_packages

version_file_path = ""

def list_directory_contents(directory):
    try:
        # Liste tous les fichiers et dossiers dans le répertoire spécifié
        contents = os.listdir(directory)
        print(f"Contents of '{directory}':")
        for item in contents:
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                print(f"File: {item}")
                if item ==  "VERSION":
                    version_file_path = item_path
                    print(version_file_path)
            elif os.path.isdir(item_path):
                print(f"Directory: {item}")
            else:
                print(f"Other: {item}")
    except FileNotFoundError:
        print(f"The directory '{directory}' does not exist.")
    except PermissionError:
        print(f"Permission denied to access '{directory}'.")



def read_version():
    repo_path = os.getenv('CI_PROJECT_DIR', os.path.abspath(os.path.dirname(__file__)))
    list_directory_contents(repo_path)
    print(version_file_path)
    
    if not os.path.isfile(version_file_path):
        print("Le fichier version n'existe pas")
        return '0.0.0.0'
    with open(version_file_path, 'r') as version_file:
        version = version_file.read().strip()
        print(f"La version dans le fichier VERSION est {version}")
    return version


def get_version():
    repo_path = os.getenv('CI_PROJECT_DIR', os.path.abspath(os.path.dirname(__file__)))
    version_file_path = os.path.join(repo_path, 'VERSION')
    print(version_file_path)
    if not os.path.exists(version_file_path):
        raise FileNotFoundError(f"The version file does not exist: {version_file_path}")
    with open(version_file_path, 'r') as version_file:
        version = version_file.read().strip()
    return version

def increment_version(version):
    major, minor, patch, build = map(str, version.split('.'))
    val = int(build) + 1
    res = str(val)  # Increment the patch version
    return f"{major}.{minor}.{patch}.{res}"

def write_version(version):
    version_file_path = './VERSION'
    with open(version_file_path, 'w') as version_file:
        version_file.write(version)

if os.getenv('CI'):
    # Only increment the version in CI environment
    if os.getenv('CI_COMMIT_REF_NAME') == 'main':
        current_version = read_version()
        new_version = increment_version(current_version)
        print(new_version)
        write_version(new_version)
    else:
        new_version = read_version()
else:
    new_version = read_version()





def print_found_packages():
    # Utilisez find_packages() pour obtenir la liste des packages trouvés
    packages = find_packages(include=['pydataspace','pydataspace.jsonLDObject', 'pydataspace.jsonLDObject.*'])
    print("Packages trouvés :")
    for package in packages:
        print(f"  {package}")

print_found_packages()


setup(
    name='pydataspace-jsonLDObject',
    version=read_version(),
    packages=find_packages(include=['pydataspace', 'pydataspace.jsonLDObject', 'pydataspace.jsonLDObject.*']),
    package_data={
        'mypackage': ['pydataspace/data/*.yaml'],  # Inclut tous les fichiers .json et .txt dans le répertoire data/
    },
    include_package_data=True,
    install_requires=[
        # Liste des dépendances
    ],
    author='Olivier Tirat',
    author_email='olivier.tirat@free.fr',
    description='Objet JsonLD de base pour pydataspace',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/dataspace2/ontologies/jsonldobject',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)



