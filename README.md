# SOA_Final Repository

- To run the project ensure that docker desktop is installed

# TO TEST LOCALLY
- Navigate to the root folder where the docker-compose file is 
- run "docker-compose up --build" to build the images and start the containers for the application 
- application should start on http://localhost:3000/

# COMMANDS TO USE WHEN TESTING

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
