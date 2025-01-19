# Building and Running the Application with Docker
## Overview
This guide provides the steps to quickly build and run the application using Docker. It includes setting up the environment, building the Docker image, and running the application with Docker Compose.

## Prerequisites
- Docker and Docker Compose installed on your system.
- Application files (including Dockerfile, docker-compose.yml, and requirements.txt).
    
## Steps to Run the Application
1. Clone the repository containing the Docker files

2. Build the Docker Image
    Use Docker Compose to build the application image:
    ```docker-compose build```
    This command builds the Docker image based on the Dockerfile in the current directory.

3. Run the Application
Once the build is complete, run the application using:

    In the Foreground: ```docker-compose up```\
    In the Background (Detached Mode): ```docker-compose up -d```\
    ***The application will now be accessible at http://localhost:7755.***

4. Stop the Application
To stop the application and remove the containers, run: ```docker-compose down```

Access the Application: Open browser and go to http://localhost:7755 to access the running application.

Optional: Running Database Migrations
To run database migrations, execute the following inside the container:\
```docker-compose exec fyle-backend flask db upgrade -d core/migrations/```

## Conclusion
By following these steps, the application will run in a Docker container.
