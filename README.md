**SOA_Final Repository**

# Description
This project was to showcase a software-oriented architecture where service providers register services for a client to see and use. In this case, the services are part of a stock app.


- This project uses:
    - docker
    - python
    - nodejs
    - flask
    - requests
    - tenacity


**TO TEST LOCALLY**
- Navigate to the root folder where the docker-compose file is 
- run "docker-compose up --build" to build the images and start the containers for the application 
- NOTE registry container may close on start up and will need to be started up again (It communicates with backup registry on start up but on the intial docker compose, backup   registry may be created after registry)

- application should start on http://localhost:3000/

# Login Information:
- "username": "nazim",
- "password": "ilove4471"

**COMMANDS TO USE WHEN TESTING**

To send a request to register a service: 
- URL: http://127.0.0.1:4003/send-register-request?serviceName=<serviceName>
  - serviceName options include:
      - pastyields
      - datadisplayer
      - rankbysector
To send a request to deregister a service:
- URL: http://127.0.0.1:4003/send-deregister-request?serviceName=<serviceName>
  - serviceName options include:
      - pastyields
      - datadisplayer
      - rankbysector
   
To check current registered services in the registry:
- Main Registry URL: http://127.0.0.1:4004/getList
- Backup Registry URL: http://127.0.0.1:4005/getList

 To check time of latest modification of registry:
- Main Registry URL: http://127.0.0.1:4004/getTime
- Backup Registry URL: http://127.0.0.1:4005/getTime
