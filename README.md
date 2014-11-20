###NMSAPP Django app###

* nmsapp is a django app that works with the nmsweb django project.
* Build the package and pip install the package to use it.
* This will build the package with pyc files excluding py files. So make sure
  to compileall before generating the package.

###Building Packag###
* Generate latest pyc files.

    python generate_pyc.py

* Update the version in setup.py file.
* Build the package using following command.
    
    python setup.py sdist

* New package will be generated in the build/ directory.
* Install the package using the following command.

    pip install build/nmsapp-<version>.tar.gz
