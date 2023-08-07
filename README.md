# Django-Bug-Tracking
A basic project for managing bugs in a typical project and application.

## Screenshots

###### Homepage
![Image of Homepage](https://github.com/TuanLe53/Django-Bug-Tracker-Project/blob/main/screenshots/Screenshot%20(59).png)

## Tech/Framework Used

**Built With**

- [Django](https://www.djangoproject.com/)
- Html
- CSS
- Javascript
- D3.js

## Features
- Allows the user to add projects 
- Allows users to add and manage bugs in their project
- Allows users to add and manage their team members
- Bug has priority (low, medium, high) and state(resolved, unresolved)

## Installation

- Clone the github repository:

```
git clone https://github.com/TuanLe53/Django-Bug-Tracker-Project.git
```

- cd into the Django bug tracker project and migrate database

```
python manage.py makemigrations
python manage.py migrate
```

- set your database in the settings.py file

- Run server

```
python manage.py runserver
```
