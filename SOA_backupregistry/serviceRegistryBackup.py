import json
from flask import Flask, jsonify, request
import requests 
import datetime
# import pytz

activeServices = {}
variable_modified_times = {}
# est = pytz.timezone('US/Eastern')


def updateToMain():
    mainRegistryFailed = False
    data = {"activeServices": activeServices, "time": variable_modified_times['activeServices'].strftime('%Y-%m-%d %H:%M:%S')}
            # will need to fetch the data from backup 
    try: 
        backupregisterURL = "https://registry:4004/updatemain"
        response = requests.post(backupregisterURL, json=data)
        if response.status_code == 500:
                raise Exception("main registry failed")
    except (requests.exceptions.ConnectionError, Exception) as e:
        mainRegistryFailed = True
    
    if(not mainRegistryFailed):
        response_data = {
            "status_code": response.status_code,
            "content": response.text  # You can adjust this based on the content type of the response
        }  
        return {'response': response_data}
    else:
        error_data = {
            "status_code": "500",
            "message": "Failed to register service."
        }
        return {'response': error_data}



class ServiceRegistryBackup:
    app = Flask(__name__)

    def __init__(self):
        self.services = {}
        pass
        

    
    @app.route('/getTime', methods=['GET'])
    def test(): 
        if 'activeServices' in variable_modified_times:
            return jsonify({'time': variable_modified_times['activeServices']})
        else:
            return jsonify({'message': 'No active services time available'})
    
    
    @app.route('/updatebackup', methods=['POST'])
    def updateFromMain(): 
        if request.is_json:
            data = request.get_json()
            activeServ = data['activeServices']
            mainTime = data['time'] 
            # mainTime = datetime.datetime.strptime(mainTime, '%Y-%m-%d %H:%M:%S')
            global activeServices
            if 'activeServices' in variable_modified_times:
                if mainTime > variable_modified_times['activeServices'].strftime('%Y-%m-%d %H:%M:%S'):
                    activeServices = activeServ 
                    variable_modified_times['activeServices'] = datetime.datetime.now()
                    return jsonify({'mes': activeServices}, 200)
                else:
                    response = updateToMain()
            else:
                activeServices = activeServ
                variable_modified_times['activeServices'] = datetime.datetime.now()
                return jsonify({'mes': activeServices}, 200)
 
        
    @app.route('/getList', methods=['GET'])
    def getList():
        return activeServices      
        

    @app.route('/register-service', methods=['POST'])
    # def registerService(self, service_name, service_url, service_port, service_description):
    def registerService():
        global activeServices
        if 'activeServices' not in variable_modified_times:
            mainRegistryFailed = False
            # will need to fetch the data from backup 
            try: 
                getActiveServicesMain = "https://registry:4004/getList"
                response = requests.get(getActiveServicesMain)
                if response.status_code == 500:
                        raise Exception("main registry failed")
            except (requests.exceptions.ConnectionError, Exception) as e:
                mainRegistryFailed = True
            
            if(not mainRegistryFailed):
                activeServices = response.json()
        
                getTime = "https://registry:4004/getTime"
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
                variable_modified_times['activeServices'] = datetime.datetime.now()

                response = updateToMain()
        #         #here is where we make a request to the front end.
           
            return jsonify({"message": "Successfully registered this service"}), 200
            
        else:
            return jsonify({"message": "Unable to add this Service"}), 400


        
    @app.route('/deregister-service', methods=['DELETE'])
    def deregisterService():
        global activeServices
        #If Our last modified time is empty, no changes have been made, fresh startup
        if 'activeServices' not in variable_modified_times:
            mainRegistryFailed = False
            #Attempt to request to main registry to get their list and time if they are running
            try: 
                getActiveServicesMain = "https://registry:4004/getList"
                response = requests.get(getActiveServicesMain)
                #If status code is 500, main registry is offline 
                if response.status_code == 500:
                        raise Exception("main registry failed")
            except (requests.exceptions.ConnectionError, Exception) as e:
                #set mainRegistryFailed to true
                mainRegistryFailed = True
            #If main Registry is online
            if(not mainRegistryFailed):
                #request was suscessfull and set backup activeService to response
                activeServices = response.json()
                #create a new request to set backup timestamp to response
                getTime = "https://registry:4004/getTime"
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
                variable_modified_times['activeServices'] = datetime.datetime.now()
                response = updateToMain()
                return jsonify({"message": "Successfully de-registered this service"}), 200

        else:
            return jsonify({"message": "Unable to remove this Service"}), 400    
            

    
    
    def findService(self, service_name):
        return activeServices.get(service_name)

    
    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=4005, debug=True)
