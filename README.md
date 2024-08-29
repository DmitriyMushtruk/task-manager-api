# task-manager-api
## Tables of content
* Introduction
* Technologies
* Launch
* API documentation

## Introduction
Task Manager API is a backend service built with Django and Django Rest Framework (DRF) designed
to help users manage their personal tasks. This API allows users to create, read, update,
and delete tasks, offering full CRUD functionality. The application supports user authentication,
enabling users to manage their own list of tasks securely.

## Technologies
This project was developed using the following technologies:

* Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
* Django REST Framework (DRF): A powerful and flexible toolkit for building Web APIs, used to create the RESTful API for this project.
* PostgreSQL: A powerful, open-source object-relational database system, used as the primary database for this project.

These technologies work together to provide a robust, scalable, and secure backend for the application.

## Launch
To run this project, Docker is required. Follow the steps below to launch the application:

* First, download or clone the repository using the following command:
```
git clone https://github.com/DmitriyMushtruk/task-manager-api.git
```

* Open your command line interface, and navigate to the directory containing the Docker files:
```
cd path/to/name_of_repository/task_manager
```


* Once inside the Docker directory, build and start the containers by running the following command:

```
docker-compose up --build
```

* After the containers have started, open the Docker application. Find the running container and follow the address provided 
to access the application in your web browser.

This process will get the project up and running in a Dockerized environment.

## API documentation
This project includes user registration and authentication using JWT tokens.
Below are the details on how to interact with these endpoints.

### User Registration
To register a new user, send a POST request to the following endpoint:

* POST /api/register/

The request must include the following JSON data:

```json
{
    "first_name": "your_first_name",
    "last_name": "your_last_name",
    "username": "your_username",
    "password": "your_password",
    "password_confirmation": "your_password"
}
```

### Authentication
After successful registration, the user can authenticate using the credentials provided during
registration.

* POST /api/login/

Request Body:\
The request should include the username and password in the following JSON format:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```
Response:\
If the authentication is successful, the response will include the following tokens:

* access: JWT access token, used for authenticated requests.
* refresh: JWT refresh token, used to obtain new access tokens.\
These tokens should be included in the Authorization header of subsequent requests to access protected resources.

### Authorization
After obtaining the JWT tokens from the login process, you can access routes that require authentication by including the access token in your request headers.

Using the Access Token

For any authenticated request, include the access token in the Authorization header of the HTTP request. The header should be formatted as follows:

```plaintext
Authorization: Bearer <your access token>
```
Replace <your access token> with the actual access token received from the /api/login/ endpoint.

This ensures that the server can verify your identity and authorize access to protected resources.

### Endpoints
Access to the application's functionality is restricted to authenticated users.\
Ensure that you include the access token in the Authorization header for each request as described in the Authorization section.

#### User Management
* View All Users
```plaintext
GET /api/users/
```
Retrieves a list of all registered users.\

* View a Specific User
```plaintext
GET /api/users/?username=<username>
```

Retrieves details for a specific user based on their username.\
Parameter: username - The username of the user you want to view.\

#### Task Management
* View All Tasks
```plaintext
GET /api/tasks/
```
Retrieves a list of all tasks in the system.

* Filter Tasks by User
```plaintext
GET /api/tasks/?user_id=<user_id>
```
Retrieves tasks assigned to a specific user.\
Parameter: user_id - The ID of the user whose tasks you want to filter.

* Filter Tasks by Status
```plaintext
GET /api/tasks/?status=<status_name>
```
Retrieves tasks based on their status.\
Parameter: status_name - The status of the tasks you want to filter.\
Available statuses: new, in progress, completed

* Filter Tasks by User and Status
```plaintext
GET /api/tasks/?user_id=<user_id>&status=<status_name>
```
Combines both user and status filters to retrieve tasks.

* View a Specific Task
```plaintext
GET /api/tasks/<task_id>/
```
Retrieves details for a specific task by its ID.

* Task Creation
```plaintext
POST /api/tasks/
```
Creates a new task. The title is required, the description is optional,
and the status defaults to "new" unless specified.\
Example Request Body:
```json
{
    "title": "Your title",
    "description": "Your description",
    "status": "in progress"
}
```
Note: The user ID is automatically assigned based on the authenticated user.

* Task Modification
```plaintext
PUT /api/tasks/<task_id>/
```
Updates an existing task. Only the task owner can modify the task.

* Mark a Task as Completed
```plaintext
PATCH /api/tasks/<task_id>/?completed
```
Updates the status of a task to "completed". This action is available **only** to the task owner.

* Task Deletion
```plaintext
DELETE /api/tasks/<task_id>/
```
Deletes a task. Only the task owner can delete the task.
