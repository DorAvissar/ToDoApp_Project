# Test Overview

The test  is designed to ensure that the Flask application's task management functionalities, including creating, retrieving, updating, and deleting tasks, are functioning correctly. The tests interact with MongoDB, verifying both the application's response and the database's state to ensure consistency and correctness.

- Fixtures
app: This fixture configures the Flask application for testing, setting up a testing environment with a MongoDB URI and enabling the TESTING flag to isolate test effects from production.

- client: Provides a test client for the application configured by the app fixture, allowing you to simulate requests to the application.

- init_db: Attempts to establish a connection with MongoDB, retrying up to five times with delays. It yields the database object for direct manipulation during tests and ensures clean-up by dropping the test database after each test, providing a fresh state.

## Individual Tests: 

- test_uncompleted_tasks:

    Purpose: Verifies that the endpoint for retrieving tasks is functioning as expected.
    Process: Makes a GET request to the 'tasks' endpoint and checks that the response status is 200 (OK) and that the response data contains a specific string, indicating that tasks are being retrieved correctly.

- test_add_task:

    Purpose: Ensures that tasks can be added through the application.
    Process: Submits a POST request with task details to the 'action' endpoint and checks that the response redirects correctly (status 302). It then verifies that the new task is present in the MongoDB database, confirming the operation's success.

- test_delete_task:

    Purpose: Tests the deletion functionality of a task.
    Process: First, a task is added to the database, then a DELETE request is simulated by sending a GET request to the 'remove' endpoint with the task's ID. The test checks for a successful redirect and verifies that the task is no longer present in the database.

- test_update_task:

    Purpose: Checks the task update functionality.
    Process: Adds a task and then sends a POST request with updated task details to the 'action3' endpoint. The response is checked for a redirect, and the task in the database is verified to ensure it reflects the updated details.

- test_list_tasks:

    Purpose: Confirms that all tasks can be listed correctly.
    Process: Adds multiple tasks to the database and makes a GET request to the 'lists' endpoint. It verifies that the response is correct and that it contains the details of all added tasks, confirming the listing functionality.

## Debugging Information
Each test includes debug prints that show the state of the database before and after tests, which can be very helpful during development and debugging phases to understand the internal state and identify issues.

# Docker Compose
After running the test locally , 
Docker Compose File Overview:

Services:
The services section defines two separate services that Docker Compose will manage:

- mongodb:

    Image: This service uses the official MongoDB image from Docker Hub tagged as latest. This will ensure that the latest version of MongoDB is used.

    Environment: Sets environment variables to configure the MongoDB container. It specifies default username (root) and password (mongoDB) for MongoDB initialization.

    Ports: Maps port 27017 of the container to port 27017 on the host, allowing the MongoDB server to be accessible from the host machine.

    Networks: Attaches the MongoDB service to a custom network called app-network. This enables network isolation and facilitates communication between your application and MongoDB within this network.

- test-app:

    Build:
    
    Context: Specifies the directory (current directory in this case, denoted by .) where the Dockerfile is located. This directory should contain all files necessary for building the application image.

    Dockerfile: Points to a specific Dockerfile (Dockerfile.test), which is tailored for running tests. This file would typically set up the application environment, install dependencies, and prepare the application for testing.

    Environment: Defines an environment variable MONGO_URL that provides the connection string for MongoDB, formatted to use the credentials and network settings defined in the MongoDB service.

    Depends on: Specifies that test-app depends on mongodb. This ensures that the MongoDB service is started before the application tries to connect to it.

    Command: Overrides the default command in the Dockerfile with pytest, which runs the tests when the container starts.

    Networks: Connects the service to the app-network, enabling it to communicate with the MongoDB service on the same network.

- Networks:

    app-network:

    Driver: Uses the bridge driver, which creates a network bridge in Docker to enable the communication between the containers on the same Docker host. This isolated network helps prevent interference with other networks or services on the host machine.

## when do we use this docker-compose? 

In the Jenkins file, there's a stage named "Unit Test". During this stage, Docker Compose is activated on the agent pod to set up the environment and execute the tests. Once testing is complete, it performs a cleanup by shutting down any services it started. If the tests pass, the process proceeds to the next stages.

