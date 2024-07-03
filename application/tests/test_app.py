import pytest
from flask import url_for
from app import app as flask_app
from pymongo import MongoClient, errors
import os
import time

@pytest.fixture
def app():
    flask_app.config['MONGO_URI'] = os.getenv('MONGO_URL', 'mongodb://root:mongoDB@mongodb:27017/mymongodb?authSource=admin')
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    mongo_uri = app.config['MONGO_URI']
    print("Attempting to connect with URI:", mongo_uri)  # Log the URI being used to connect
    for _ in range(5):  # Try 5 times to connect with a delay
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            client.server_info()  # Force connection
            db = client.get_database()  # Automatically get the database from the URI
            print("Databases before test:", client.list_database_names())  # Debug information
            yield db
            client.drop_database(db.name)
            print("Databases after test:", client.list_database_names())  # Debug information
            return
        except errors.ServerSelectionTimeoutError as err:
            print(f"Connection failed, retrying... ({err})")
            time.sleep(2)
    raise Exception("Failed to connect to MongoDB")

def test_uncompleted_tasks(client, init_db):
    response = client.get(url_for('tasks'))
    assert response.status_code == 200
    assert "TODO Reminder with Flask and MongoDB" in response.data.decode()

def test_add_task(client, init_db):
    task_data = {
        "name": "Test Task",
        "desc": "Test Description",
        "date": "2024-06-30",
        "pr": "High",
        "assignee": "Tester"
    }
    response = client.post(url_for('action'), data=task_data)
    assert response.status_code == 302

    # Verify task was added to the database
    db = init_db
    print("Using database:", db.name)  # Debug information
    print("Collections in testdb before insertion:", db.list_collection_names())  # Debug information
    task = db.todo.find_one({"name": "Test Task"})
    print("Task found in database:", task)  # Debug information
    assert task is not None

    # Debugging information about the databases
    print("Databases after test:", db.client.list_database_names())

def test_delete_task(client, init_db):
    # Add a task to the database
    task_data = {
        "name": "Task to Delete",
        "desc": "Description to Delete",
        "date": "2024-07-02",
        "pr": "Low",
        "assignee": "Tester"
    }
    client.post(url_for('action'), data=task_data)

    # Fetch the task to get its ID
    db = init_db
    task = db.todo.find_one({"name": "Task to Delete"})
    assert task is not None
    task_id = str(task["_id"])

    # Delete the task
    response = client.get(url_for('remove', _id=task_id))
    assert response.status_code == 302

    # Verify task is deleted
    deleted_task = db.todo.find_one({"_id": task["_id"]})
    print("Deleted task:", deleted_task)  # Debug information
    assert deleted_task is None

    # Debugging information about the databases
    print("Databases after test:", db.client.list_database_names())

def test_update_task(client, init_db):
    # Add a task to the database
    task_data = {
        "name": "Task to Update",
        "desc": "Description to Update",
        "date": "2024-07-03",
        "pr": "Medium",
        "assignee": "Tester"
    }
    client.post(url_for('action'), data=task_data)

    # Fetch the task to get its ID
    db = init_db
    task = db.todo.find_one({"name": "Task to Update"})
    assert task is not None
    task_id = str(task["_id"])

    # Update the task
    updated_task_data = {
        "name": "Updated Task",
        "desc": "Updated Description",
        "date": "2024-07-04",
        "pr": "High",
        "assignee": "Updated Tester",
        "_id": task_id
    }
    response = client.post(url_for('action3'), data=updated_task_data)
    assert response.status_code == 302

    # Verify task is updated
    updated_task = db.todo.find_one({"_id": task["_id"]})
    print("Updated task:", updated_task)  # Debug information
    assert updated_task is not None
    assert updated_task["name"] == "Updated Task"
    assert updated_task["desc"] == "Updated Description"
    assert updated_task["date"] == "2024-07-04"
    assert updated_task["pr"] == "High"
    assert updated_task["assignee"] == "Updated Tester"

    # Debugging information about the databases
    print("Databases after test:", db.client.list_database_names())

def test_list_tasks(client, init_db):
    # Add a couple of tasks to the database
    tasks_data = [
        {
            "name": "Task 1",
            "desc": "Description 1",
            "date": "2024-07-02",
            "pr": "Low",
            "assignee": "Tester 1"
        },
        {
            "name": "Task 2",
            "desc": "Description 2",
            "date": "2024-07-03",
            "pr": "High",
            "assignee": "Tester 2"
        }
    ]
    for task_data in tasks_data:
        client.post(url_for('action'), data=task_data)

    # Fetch all tasks
    response = client.get(url_for('lists'))
    assert response.status_code == 200
    response_data = response.data.decode()
    print("List tasks response data:", response_data)  # Debug information
    for task_data in tasks_data:
        assert task_data["name"] in response_data
        assert task_data["desc"] in response_data
        assert task_data["date"] in response_data
        assert task_data["pr"] in response_data
        assert task_data["assignee"] in response_data

        