# Final Project: Creating a REST API to Analyze Near-Earth Comets

We live in a universe that holds billions of particles, planets, asteroids, stars, comets… and there lies uncertainty all across space - have you ever seen a shooting star or a comet? The objective of this project was to create a REST API front-end to a time series data set, near-earth comets, that allows for basic CRUD - Create, Read, Update, Delete - operations and for users to submit analysis jobs. Our application supports on the back-end an analysis job to create a plot of comets within a certain aphelion (farthest distance from sun) range. For others to access and interact with our API, we will have hosted it on the Kubernetes cluster. This project utilizes Python 3, Flask, Docker, and Redis. 


## Contents

This repository contains the following scripts and files:

- `docker/`
  * `Dockerfile.api`: text file that contains all commands to build the image for `flask_api.py`.
  * `Dockerfile.wrk`: text file that contains all commands to build the image for `worker.py`.

- `kubernetes/prod/`
  * `app-prod-redis-pvc.yml`: A YAML file that stores data from the deployment file.
  * `app-prod-redis-deployment.yml`: A YAML file that creates a deployment for the Redis database.
  * `app-prod-redis-service.yml`: A YAML file that provides a persistent IP address to interact with the Redis database.
  * `app-prod-api-deployment.yml`: A YAML file that creates a deployment for the Flask application.
  * `app-prod-api-service.yml`: A YAML file that provides a persistent IP address to interact with the Flask application.
  * `app-prod-wrk-deployment`: A YAML file that creates a deployment for the worker file.

- `src/`
  * `flask_api.py`: A Flask application that parses data about comets close to earth to return information about comet names, epochs, aphelions, perihelions, orbital periods, and more, through routes.
  * `worker.py`: A file that captures submitted jobs and performs the analysis.
  * `jobs.py`: A file that allows for jobs to be generated and added to a queue. 

- `test/`
  * `test_flask.py`: A file that implements `pytest` to run unit tests and integration tests to check the functionality of the application.

- `Makefile`: A text file that contains shortcuts of commands to utilize in the command line.


## Instructions for Deploying API

Run the code sequentially as follows:

#### Step 1: Clone the GIT Repository

```
$ git clone git@github.com:nikhil-sharma710/comet-analyzer.git
```

#### Step 2: Download the Near-Earth Comets Dataset

To download the dataset, first navigate to the `src/` directory within the repository. Then use `wget` to retrieve the data. Lastly, rename the data to `comets_data.json`.

```
$ cd src/
$ wget https://data.nasa.gov/resource/b67r-rgxc.json
$ mv b67r-rgxc.json comets_data.json
```

#### Step 3: Build and Run All the Containers

To get the `flask_api`, `worker`, and `redis` containers up and running, simply call the following in the command line:

 ```
$ make all 
```

This command utilizes a command in `Makefile` which cleans and removes previous images, builds new images for the Flask application, Redis, and the worker file, and runs the containers. 
  * NOTE: make sure you are in the `comet-analyzer/` directory within the repository when calling commands from `Makefile`. 

#### Step 4: Check the Images and Containers are Up and Running

Once again, we will use a command in `Makefile`:
```
$ make list
```

This command shows a list of all the user’s personal images and containers that have been built and run. Make sure that the containers’ statuses display `Up <followed by a time>` - this indicates that there were no errors in the python files.

#### Step 5: Read Data from File into Redis Database

Before navigating the routes, data must be read from the file into Redis. To do so, use the following command:

```
$ curl localhost:5014/read-data -X POST
```

This will use the `POST` operation to load the data from the file into memory.


#### Step 6: Run Function Tests for the Flask API

The user can simply do this through the following command:

```
$ pytest
```

This command makes sure each function in `flask_api.py` has no errors. If all tests pass, you should expect something like this:
```
======================================================== test session starts =========================================================
platform linux -- Python 3.6.8, pytest-7.0.1, pluggy-1.0.0
rootdir: /home/kasonjim/coe-332/comet-analyzer
collected 5 items

test/test_flask.py .....                                                                                                       [100%]

========================================================= 5 passed in 11.44s =========================================================
```
 

## Instructions for Using the API

Yay! Now that the user has deployed the application, made sure their images and containers are functional, and ran a successful pytest, they may begin interacting with the application through their local machine.

#### Step 1: Curl Desired Routes From API

The general syntax for calling a route:

```
$ curl localhost:5014/<route>
```

Here are the routes that the user may curl:

- `/info` (`GET`) - displays all the routes

- `/read-data`
  * `POST` - reads the data into Redis database
  * `GET` - shows list of all comets data
  * `DELETE` - deletes existing data from the Redis database

- `/symbols` (`GET`) - displays info on what each symbol means

- `/comets` (`GET`) - displays a list of comet names and their respective IDs (note these IDs are important later on)

- `/comets/<comet_id>` (`GET`) - displays info about specific comet
  * The <comet_id> is the ID from the `/comets` route

- `/comets/delete/<comet_id>` (`DELETE`) - deletes data on specific comet

- `/comets/update/<comet_id>/<key_value>/<new_value>` (`PUT`) - update/change a specific piece of info on a specific comet.
  * i.e. `curl localhost:5014/comets/update/<comet_id>/e/7` -> updates the value `e` to `7`

- `/jobs` 
  * `GET` - info on how to submit a job
  * `POST` - submit a job

- `/jobs/<jobid>` (`GET`) - info on specific job

- `/list-of-jobs` (`GET`) -  list of all the jobs 

For routes that do not use the `GET` method (`POST`, `PUT`, or `DELETE`), `-X <method type>` must be included after the route.

#### Step 2: Submit a Job and Download Histogram Image

To submit a job, use the `/jobs` route listed above. After typing the route into the command line, the variable values for job must be added. The whole command should look as follows:

```
$ curl localhost:5014/jobs -d ‘{“min_au”: “<minimum AU value>”, “max_au”: “<maximum AU value>”, “num_bins”, “<number of bins>”}’ -H “Content-Type: application/json”
```

For `minimum AU value` and `maximum AU value`, look at the data to see what values would be appropriate for these inputs and `<number of bins>`, 

To download the histogram image, use the following command:

```
curl localhost:5014/download/<jobid> > output.png
```

The image will be saved as a PNG file, and the histogram can be viewed in the repository.

## Deploying in Kubernetes

#### Step 1: Log into isp -> log into k8s
```
$ ssh <username>@coe332-k8s.tacc.cloud
```
#### Step 2: Acquire `.yml` Files from Repo into k8s

#### Step 3: Apply all the `.yml` files and make sure to do it in this order:

```
$ kubectl apply -f app-prod-db-service.yml
$ kubectl apply -f app-prod-db-pvc.yml
$ kubectl apply -f app-prod-db-deployment.yml
$ kubectl apply -f app-prod-api-service.yml
$ kubectl apply -f app-prod-api-deployment.yml
$ kubectl apply -f app-prod-wrk-deployment.yml
```
#### Step 4: Make Sure Pods are Up and Running
```
kubectl get all -o wide
```

#### Step 5: Find the IP Address Container is Using for Flask

```
$ kubectl describe service <container name>
```

#### Step 6: Exec into a Container to Curl the Route using the IP address

```
$ kubectl exec -it <pod name> -- /bin/bash
$ curl <ip_address>:5000/read-data -X POST
```

## Data Citations

NASA. “Near-Earth Comets - Orbital Elements.” 2 Apr. 2015, [https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements/b67r-rgxc](https://data.nasa.gov/Space-Science/Near-Earth-Comets-Orbital-Elements/b67r-rgxc). Accessed 11 May 2022. 
