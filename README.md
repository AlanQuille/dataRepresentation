# Data Representation Project 2020
## Option A
This repository contains all the files necessary for a Flask server which performs SQL operations on two tables, student and lecturer.

### How to run

To run the server, navigate into the Server folder and type:

**python restserver.py**

And press Enter.

### Username and password

If you're navigating the web server via a browser, to login use the following credentials:

*Username*: **root**

*Password*: **Pericles1.**


And press Enter (to clarify, the password is a blank string).

### Default value of table ###
The server allows one to change the current table being operated on from student to lecturer or vice versa. The default value is determined by the default_value.txt file in the Server folder. The current default value is 1 for lecturer but one can change it to 0 for the student table if required.

### Github link ###
This repository is available online <a href="https://github.com/AlanQuille/dataRepresentation">here</a>

### Pythonanywhere hosting link ###
The app is hosted online [http://mamq.pythonanywhere.com](http://mamq.pythonanywhere.com "here")

### load.sql ###
Optionally, you can create the database "datarepresentation" and the student and lecturer tables automatically by running load.sql in this directory. Some sample data is also input into the table. Run in a database called datarepresentation with the following command:

mysql -h localhost -u root datarepresentation < /path/to/load.sql



