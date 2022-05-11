## Creating a REST API to Analyze Near-Earth Comets
We live in a universe that holds billions of particles, planets, asteroids, comets, galaxies… Uncertainty lies amongst not only the planet Earth but also in space. The objective of this project was to create a REST API front-end to a time series data set, near-earth comets, that allows for basic CRUD - Create, Read, Update, Delete - operations and for users to submit analysis jobs throu. Our application supports on the back-end an analysis job to create a plot of comets within a certain aphelion (farthest distance from sun) range. For others to access and interact with our API, we will have hosted it on the Kubernetes cluster. 

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
  * `worker.py`: A worker file that 
  * `jobs.py`: 
- `test/`
  * `test_flask.py`: A test file that runs unit tests and integration tests to check the functionality of the application.
- `Makefile`: A text file that contains shortcuts of commands to utilize in the command line.

