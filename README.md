
# Knapsack Optimizer Service

# Introduction
This code provides functionality for an Optimization Service using the Knapsack Optimization Algorithm.

### Motivation

Preamble: We are the largest container shipping company in the world. Each container has a maximal weight it may hold. Customers need to plan which of their products they can pack into a single shipping container in a manner of utmost Efficiency.

# Development Setup

### Prerequisites

This Project Requires the [Docker Community Engine](https://docs.docker.com/engine/install/) to Run. It has no Additional Dependencies.

### Code Structure
The System Contains the Following File Structure

- docker-compose.yml → This file is the composer for our Docker Container Structure. This defines our services and exposes our ports.

- DockerFile → This file is responsible for building out container and initialization our Python Flask Setup with Logging.

-  [setup.py](http://setup.py) → This File Bootstraps our Application together.

- src/ → This Folder Contains our main Code

- tests/ → This Folder contains the relevant tests for our Application.

  

```jsx

knapsack/

|-- src/

| |-- __init__.py

| |-- flask_app.py

|

|-- tests/

| |-- test_functionality.py

|

|-- Dockerfile

|-- docker-compose.yml

|-- requirements.txt

|-- setup.py

|-- setup.cfg

|-- README.MD

```

  

### Run The Code

To Run the Code, checkout this repository, navigate to the project directory [knapsack], and simply execute

  

```bash

docker-compose up

```

  

This will build the compose and execute the container Giving you the Logs of the API.

  

### Run the Tests

  

To run the tests, please install **pytest** using the command

  

```bash

pip install pytest

```

  

Then navigate to the tests folder and run

  

```bash

pytest

```

  

### Sample Session



The following is a hypothetical session with a knapsack optimiser service, using docker compose to start a composite service, listening on port 6543:

  

```bash

docker-compose up

```

  

This will fire up our System.

  

### Initialize A Problem


To Initialize a Problem, we fire a POST request from Terminal/Postman or any Other Application of our choice with the following payload.

  

```bash

$ curl -XPOST -H 'Content-type: application/json' http://localhost:6543/knapsack \

-d '{"problem": {"capacity": 60, "weights": [10, 20, 33], "values": [10, 3, 30]}}'

```

  

This will create a file inside the container with the timestamps and the problem JSON. The API then sends us back the contents of this file. We note the id of the task for referencing the problem and it's solution.

  

This is a sample Output of the above command

  

```bash

{"task": "nbd43jhb", "status": "submitted", "timestamps": {"submitted": 1505225308, "started": null, "completed": null}, "problem": {"capacity": 60, "weights": [10, 20, 33], "values": [10, 3, 30]}, "solution": {}}

```

  

### Check the Results



To Check the solution, we capture the id given as the **task** in the response of the previous request. We then fire a GET request with the id as part of the url in the following fashion:

  

```bash

  

$ curl -XGET http://localhost:6543/knapsack/nbd43jhb

```

  

In the above result, we see that the status is started, This means that the scheduler has triggered the Knapsack script and now we need to wait a bit more to get the result of the solution.

  

The above command gives a sample output

  

```bash

{"task": "nbd43jhb", "status": "started", "timestamps": {"submitted": 1505225308, "started": 1505225342, "completed": null}, "problem": {"capacity": 60, "weights": [10, 20, 33], "values": [10, 3, 30]}, "solution": {}}

```

  

After waiting for some more time, we fire the script again.

  

```bash

$ curl -XGET http://localhost:6543/knapsack/nbd43jhb

```

  

If the file is processed, we get the output

  

```bash

{"task": "nbd43jhb", "status": "completed", "timestamps": {"submitted": 1505225308, "started": 1505225342, "completed": 1505225398}, "problem": {"capacity": 60, "weights": [10, 20, 33], "values": [10, 3, 30]}, "solution": {"packed_items": [0, 2], "total_value": 40}

```

  

Here, we see the status is completed. Now we can access the solution to the problem in the solution field of the output.

  

# System Specification



### System Stack


This System is built using:

  

-  **Docker** → Containerization

-  **Python**  **+**  **Flask** → Rest API + Scheduler + Core Algorithm

-  **pip** → Python's Dependency Management

  

### **REST API**



We present 2 API endpoints to the user

  

-  **POST**  `/knapsack`content: `application/json` with JSON knapsack problem specificationoutput: `json` with JSON knapsack object

- This Initializes the Problem and Creates a file for the Problem.

- The Scheduler running in the Background will pick up this file and then process it to generate the results.

-  **GET**  `/knapsack/<id>`output: `json` with JSON knapsack object

- This provides the output of the problem, with the relevant status and timestamps

  

### JSON specifications


The json requests and responses have the following formats:

  

```json

# problem specification

{

"problem": {

"capacity": #  non-negative  integer

"weights":  #  array  of  non-negative  integers

"values":  #  array  of  non-negative  integers, as  many  as  weights

}

}

  

# knapsack object

{

"task": #  Task  ID  (ASCII  string)

"status":  #  one  of  "submitted", "started",  "completed"

"timestamps": {

"submitted": #  unix/epoch  time

"started":  #  unix/epoch  time  or  null  if  not  started

"completed":  #  unix/epoch  time  or  null  if  not  completed

}

"problem":  #  problem  specification  as  above  (including  capacity, weights,  values)

"solution": { #  if  completed

"packed_items" : #  array  of  integers  (indices  to  weights  and  values)

"total_value":  #  sum  of  value  of  packed_items

}

}

```

  

### Architecture



The System Contains the Following Components

  

-  **REST API** → This is the Component Exposed to the User. He can create Problems and view their solutions using these endpoints.

-  **Scheduler** → This runs independent of the **REST** Endpoints. This Component checks for new problems at regular intervals, and if any new ones have been created, sends them to the knapsack component for processing.

-  **Knapsack Service** → This Component is the one that actually processes the input, marks the timestamps and provices the solution to a given problem.

  

### Scaling the Solution for Production



To scale the system for Production readiness, we need to make some optimizations to the system.

  

-  **RDBMS** → Currently the system uses the File System to store and retrieve problems and their solutions and other details. For a large scale system, we need to shift to a proper RDBMS on a dedicated Engine to process the inputs.

-  **Parallelization & GIL →** Currently the Knapsack Script processes each problem sequentially. We need to bring **Multi Threading** for **Parallel Processing** and need to disable the **GIL(Global Interpreter Lock)** of Python.

-  **Load Balancer** → A **Load Balancer** is always a good idea when it comes to handling a lot of simultaneous inputs. The **Load Balancer** needs to be active in scheduling the handling of the API Calls
