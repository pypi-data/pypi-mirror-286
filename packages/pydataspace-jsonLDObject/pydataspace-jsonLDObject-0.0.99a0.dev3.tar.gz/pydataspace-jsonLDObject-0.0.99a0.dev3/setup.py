from setuptools import setup, find_packages

def print_found_packages():
    # Utilisez find_packages() pour obtenir la liste des packages trouvés
    packages = find_packages(include=['pydataspace','pydataspace.jsonLDObject', 'pydataspace.jsonLDObject.*'])
    print("Packages trouvés :")
    for package in packages:
        print(f"  {package}")

print_found_packages()


setup(
    name='pydataspace-jsonLDObject',
    version='0.0.99a0-dev003',
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



