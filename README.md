Proyecto Colibrí
===========

[![Build Status](https://travis-ci.org/openkratio/proyecto-colibri.png)](https://travis-ci.org/openkratio/proyecto-colibri)

Installing requirements
-----------------------

These instructions have been tested with Ubuntu 12.04.

Install required packages, including pip for managing dependencies:

$> apt-get install python-dev python-setuptools python-pip

$> apt-get install libgraphviz-dev

Install the listed requirements with:

$> pip install -r requirements.txt

If you don't plan to use posgresql, feel free to edit requirements.txt and delete the line:
- psycopg2==2.5

TODO: Create a requirements-dev.txt that allows to use sqlite without any edits.


Run the project locally
-----------------------
Create the db:

$> python manage.py syncdb

Run the migration scripts:

$> python manage.py migrate

Get the data:

$> scrapy crawl members

$> scrapy crawl votes

$> scrapy crawl initiatives

Run the server:

$> python manage.py runserver 8080

Now browse http://localhost:8080 and you should find the colibri homepage :-)


Contribute
----------
Feel free to contribute with the project.
