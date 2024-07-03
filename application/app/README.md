# Simple Python Flask Program with MongoDB
## Python Flask Application

This repository contains a Python Flask application that connects to MongoDB, illustrating basic CRUD operations. This README outlines the setup, building, and running processes of the application within a Docker container.

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Python 
- pip (Python package installer)
- mongodb container 

## Application Structure

```
/application/
└── app             
   └── app.py           # Main Python application file with Flask routes.
├── Dockerfile          # Dockerfile for building the Docker image.
├── requirements.txt    # List of Python dependencies.
``` 

## Application Overview
The application features a simple web interface for managing TODO tasks, allowing users to add, update, mark as complete, delete, and search for tasks based on various criteria. Each task can contain details like name, description, due date, priority, and assignee.
- List Tasks (/list): Displays all tasks stored in the database.
- Uncompleted Tasks (/uncompleted): Shows tasks that have not been marked as uncompleted.
- Completed Tasks (/completed): Lists tasks that have been marked as completed.
- Toggle Task Completion (/done): Allows toggling the completion status of a task directly from the list by using an icon click. It updates the task's status in the database.
- Add a Task (/action with POST): Enables the addition of a new task through a form submission. Tasks are added with an initial status of "not done."
- Delete a Task (/remove): Facilitates the deletion of a task using its unique MongoDB _id.
- Update a Task (/update): Displays a form pre-filled with an existing task's details, allowing users to update them.
Confirm Task Update (/action3 with POST): Applies updates to an existing task in the database based on form submission.
- Search for Tasks (/search): Supports searching for tasks based on a specified field and keyword.
- List Collections (/collections): Lists all collections present in the mymongodb database, which can be useful for administrative purposes.

After understanding the appliction, Let's move on to the next step. 

## Building and runing the Docker Image
For the Docker build command to work correctly, your project folder should have a specific structure, ensuring that all necessary files are appropriately placed and accessible to Docker during the build process. Here’s the recommended directory structure and essential files for your Python Flask application:
```
/application/
└── app             
   └── app.py           # Main Python application file with Flask routes.
├── Dockerfile          # Dockerfile for building the Docker image.
├── requirements.txt    # List of Python dependencies.
``` 

Building the Docker Image: 

```
docker build -t python-flask-app .
```

Running the Application ()
```
docker run -p 5000:5000 python-flask-app
```
Here, -p 5000:5000 maps the host port to the container port as HOST_PORT:CONTAINER_PORT.

Accessing the Application:

Once the Docker container is running, you can access your Flask application by navigating to:
```
http://localhost:5000
```
