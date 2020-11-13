# App server that has a RESTful interface to provide CRUD ops for one DB table
# I am going to pick something at random like a book
# CHoose own etnity

# Book will have
## id (int, auto inc), key i.e. this will be the unique identifier
# title
# authoir
# price (integ, price in cent)
# There are other attributes it could have ISBN (this could have been 
# the unique identifier)

# Design the API
# CRUD interface
# it will need to allow us
## get all books
# get a book by id
# create a book
# update a book
# delete a book

# other apps may require other functionality in the interface
# And we can always add functionality later
# Note no code yet

# Proposed interface

# Action |Method |URL |Simple params
# Get all|Get | books | none
# Find bvy id |Get|/books/id|none
# Create| POST | /books | {title, author, price}
# Update | PUT |/books/id | {price:3000}
# delete | DELETE | /books/id | none

# Step 2 : Make app-server with skeleton functions
# OK now we start to code
# Make a very basic appserver, test it.
# Add a funciton and URL map for each of the functions 
# we require in our interface.
# Each function should just return text saying what the are. 
# Test them using CURL


# STEP 3
# Functions
# For this stage we will not link to a DB, we will just store the books
# in a list like we did in week 05

# Do the get all first that should be the easiest, TEST if with CURL
# Do find by id, TEST IT
# Do create, TEST IT
# Do update, TEST IT
# Do delete, TEST IT

