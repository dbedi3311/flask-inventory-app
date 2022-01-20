# Flask-Based Inventory Tracking Application

This is an inventory application built with Flask, SQLite, and Semantic UI to help track hypothetical inventory for a company. Submission for the Shopify Backend Developer Challenge 2022


## Deployed
I've hosted the inventory application on Heroku at the following link: [https://flask-inventory-app.herokuapp.com/](https://flask-inventory-app.herokuapp.com/) 

CRUD functionality (Creating new inventory, Reading inventory items in list format, Updating inventory, and Deleting inventory) has been implemented. An additional feature is the ability to export the stored inventory into a .csv file (which can be done by clicking the download button).


## Running on Local Machine
Verify that you have Python 3 installed on your local machine. You can download it at: [https://www.python.org/](https://www.python.org/)

First clone the repository to a working directory using git. After the project is cloned, navigate to the directory which includes the requirements.txt file.

Proceeding this, open a terminal/command prompt and run the following command:

```
 pip install -r requirements.txt 
```

After this is complete, run:

```
python3 app.py
```
This should bring up the application

![image](https://user-images.githubusercontent.com/29437601/150395316-aafd7b3b-8128-42c8-805a-5233158faad4.png)

## Backend Specifications
SQLite database with SQLAlchemy for Object-relational mapping (ORM).
