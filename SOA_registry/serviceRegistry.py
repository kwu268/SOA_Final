import json
from flask import Flask, jsonify, request
import requests 
import datetime


activeServices = {}
variable_modified_times = {}

def updateToBackup():
    data = {"activeServices": activeServices, "time": variable_modified_times['activeServices'].strftime('%Y-%m-%d %H:%M:%S')}
    backupregisterURL = "http://backupregistry:4005/updatebackup"
    response = requests.post(backupregisterURL, json=data)
    response_data = {
        "status_code": response.status_code,
        "content": response.text  # You can adjust this based on the content type of the response
    }  
    return {'response': response_data}


class ServiceRegistry:
    app = Flask(__name__)

    def __init__(self):
        self.services = {}
        pass
        
    

    def checkBackupOnFailure():
        global activeServices
        if 'activeServices' not in variable_modified_times:
            # will need to fetch the data from backup 
            getActiveServicesBackup = "http://backupregistry:4005/getList"
            response = requests.get(getActiveServicesBackup)
            activeServices = response.json()

            getTime = "http://backupregistry:4005/getTime"
            response = requests.get(getTime)
            if 'time' in response.json():
                variable_modified_times['activeServices'] = (response.json())['time']
                    
    @app.route('/getTime', methods=['GET'])
    def test(): 
        if 'activeServices' in variable_modified_times:
            return jsonify({'time': variable_modified_times['activeServices']})
        else:
            return jsonify({'message': 'No active services time available'})
                
                
    @app.route('/updatemain', methods=['POST'])
    def updateFromMain(): 
        if request.is_json:
            data = request.get_json()
            activeServ = data['activeServices']
            backupTime = data['time'] 
            # backupTime = datetime.datetime.strptime(backupTime, '%Y-%m-%d %H:%M:%S')
            global activeServices
            if 'activeServices' in variable_modified_times:
                if backupTime > variable_modified_times['activeServices'].strftime('%Y-%m-%d %H:%M:%S'):
                    activeServices = activeServ
                    variable_modified_times['activeServices'] = datetime.datetime.now()
                    return jsonify({'mes': activeServices}, 200)
                else:
                    response = updateToBackup()
            else:
                activeServices = activeServ
                variable_modified_times['activeServices'] = datetime.datetime.now()
                return jsonify({'mes': activeServices}, 200)
                
                

    @app.route('/getList', methods=['GET'])
    def getList():
        return activeServices
            

    @app.route('/register-service', methods=['POST'])
    def registerService():
        global activeServices
        if 'activeServices' not in variable_modified_times:
            # will need to fetch the data from backup 
            getActiveServicesBackup = "http://backupregistry:4005/getList"
            response = requests.get(getActiveServicesBackup)
            activeServices = response.json()

            getTime = "http://backupregistry:4005/getTime"
            response = requests.get(getTime)
            if 'time' in response.json():
                variable_modified_times['activeServices'] = (response.json())['time']
                

        if request.is_json:
            data = request.get_json()
            if data["containerName"] in activeServices:
                return jsonify({"message": "Service already exists"}), 400  
            if "containerName" in data:
                service_name = data["containerName"]
            if "description" in data:
                service_description = data["description"]
            else:
                service_description = ""
            if "ipAddress" in data:
                service_ip = data["ipAddress"]
            if "port" in data:
                service_port = data["port"]
            if "endPoints" in data:
                service_endpoints = data["endPoints"]
                serviceInformation = {"Name": service_name, "Description": service_description, "IP": service_ip, "Port": service_port, "Endpoints": service_endpoints}
                activeServices[service_name] = serviceInformation
        #         #here is where we make a request to the front end.
                variable_modified_times['activeServices'] = datetime.datetime.now()
                response = updateToBackup()
            return jsonify({"message": "Successfully registered this service"} ), 200
        else:
            return jsonify({"message": "Unable to add this Service"}), 400


        
    @app.route('/deregister-service', methods=['DELETE'])
    def deregisterService():  
        global activeServices
        if 'activeServices' not in variable_modified_times:
            # will need to fetch the data from backup 
            getActiveServicesBackup = "http://backupregistry:4005/getList"
            response = requests.get(getActiveServicesBackup)
            activeServices = response.json()

            getTime = "http://backupregistry:4005/getTime"
            response = requests.get(getTime)
            if 'time' in response.json():
                variable_modified_times['activeServices'] = (response.json())['time']

        if request.is_json:
            data = request.get_json()
            service_name = data["containerName"]
            removedService = activeServices.pop(service_name, None)

            if removedService is None:
                return jsonify({"message": "Service does not exist"}), 400
            else:
                # ServiceRegistry.updateToBackup()
                variable_modified_times['activeServices'] = datetime.datetime.now()
                response = updateToBackup()
                return jsonify({"message": "Successfully de-registered this service"}), 200

        else:
            return jsonify({"message": "Unable to remove this Service"}), 400    
            
        
        
    def findService(self, service_name):
        # return self.services.get(service_name)
        return activeServices.get(service_name)

    
    
    if __name__ == "__main__":
        checkBackupOnFailure()

        app.run(host='0.0.0.0', port=4004, debug=True)
