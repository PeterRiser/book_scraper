# book_scraper

Welcome to my book scraper. This project is a small django applcation that fires up and display the attached sqlite file which contains data scraped from a test website

**NOTE**: there are no attached users to application

# What is in here?

I am glad you asked! In the book directory, you will find the main components of the application. The `models.py` contains a set of ORM classes that map out to the SQLite DB as well as helper aggregation functions. This is how I interact with the data once it is formatted correctly.

The `views.py` contains the logic for formatting the webpage and fetching the data that renders when you hit the url. 

The `tasks.py` contains the scraper logic that grabs the categories and the books and stores them in a DB. This is where the main logic takes place. Although it does not execute in the background as it is very computationally consuming. 

`serializers.py` contains a basic serializer that validates the books as they are input because the HTML can be difficult to parse. 

Some other important files are the `settings.py` file in book_scraper. This configures all the necessary packages. 

# How to run it?
I have included a requirements.txt file and a virtualenv directory. To run, first either install the requirements to your computer using ```pip install -r requirements.txt``` from the project directory.

Or, you can source the virtual environment if you are using a unix based system. To do so, simply run ```source env/bin/activate``` which will put you into a temporary environment with all of the correct python packages. 

Once your environment is configured, run ```python manage.py runserver``` to start a local server to view the data at the ip `127.0.0.1:8000`. On the website is two tables, a category table which shows the categories with associated stats per a category. The table below is a paginated set of all the books from the site. In addition, the average philosphy book is written at the top. 

# Why I chose Django
Django has a series of very adaptable plugins for webdevelopment and html parsing already as well as a variety of validation functions built into the package. This allows me to clearly take apart the webpage. In addition, it has a very robust Object Relational Mapping (ORM) which allows very easy insertion into a SQLite DB (which is also natively supported by Django, another plus).
