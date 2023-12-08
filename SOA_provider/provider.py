import json
from flask import Flask, jsonify, request
import requests 
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class Provider:

    def serviceInfoRequest(serviceName):
        port = 0
        containerName = ""
        serviceFound = False

        if serviceName == "pastyields":
            port = 4000
            containerName = "pastyields"
            serviceFound = True

        elif serviceName == "datadisplayer":
            port = 4001
            containerName = "datadisplayer"
            serviceFound = True

        elif serviceName == "rankbysector":
            port = 4002
            containerName = "ranker"
            serviceFound = True
        
        if serviceFound:
            endpoint = f"http://{containerName}:{port}/info"
            response = requests.get(endpoint)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error calling container1 endpoint: {response.status_code}")
                return {"message": f"Error calling container2 endpoint: {response.status_code}"}
        else:
            return None



app = Flask(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(requests.exceptions.ConnectionError)
)
def try_register(registerURL, serviceInfo):
    try:
        response = requests.post(registerURL, json=serviceInfo)
        # Continue processing the response or perform other actions
        return response
    except requests.exceptions.ConnectionError as e:
        # Check if the error is due to DNS resolution failure
        if 'Name or service not known' in str(e):
            # Handle the DNS resolution error here
            error_data = {
                "status_code": 500,
                "message": "Name or service not known"
            }
            return {'response': error_data}
        else:
            # Handle other connection errors
            error_data = {
                "status_code": 500,
                "message": " registry error"
            }
            return {'response': error_data}
        
@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(requests.exceptions.ConnectionError)
)
def try_deregister(registerURL, serviceInfo):
    try:
        response = requests.delete(registerURL, json=serviceInfo)
        # Continue processing the response or perform other actions
        return response
    except requests.exceptions.ConnectionError as e:
        # Check if the error is due to DNS resolution failure
        if 'Name or service not known' in str(e):
            # Handle the DNS resolution error here
            error_data = {
                "status_code": 500,
                "message": "Name or service not known"
            }
            return {'response': error_data}
        else:
            # Handle other connection errors
            error_data = {
                "status_code": 500,
                "message": " registry error"
            }
            return {'response': error_data}


#Manual Register
@app.route('/send-register-request', methods=['GET'])
def manualRegister():
    #get service information and regsitry url 
    serviceName = request.args.get('serviceName')
    serviceInfo = Provider.serviceInfoRequest(serviceName)
    if serviceInfo is not None:
    #send request to register into registry 
        mainRegistryFailed = False
        try:
            registerURL = "http://registry:4004/register-service"
            response = try_register(registerURL, serviceInfo)
            if response is not None:
            # response = requests.post(registerURL, json=serviceInfo)        
                if response.status_code in [200, 400]:
                    response_data = {
                        "status_code": response.status_code,
                        "content": response.text  # You can adjust this based on the content type of the response
                    }
                    return {"mes": response_data}
                if response.status_code == 500:
                    raise Exception("main registry failed")
        except (requests.exceptions.ConnectionError, Exception) as e:
            mainRegistryFailed = True

            
        if mainRegistryFailed:
            try:
                backupregisterURL = "http://backupregistry:4005/register-service"
                response = try_register(backupregisterURL, serviceInfo)
                # response = requests.post(backupregisterURL, json=serviceInfo)
                response_data = {
                    "status_code": response.status_code,
                    "content": response.text  # You can adjust this based on the content type of the response
                }
                mainRegistryFailed = False
                return {"mes": response_data}
            except requests.exceptions.RequestException as e:
                return {"mes": e}
            except Exception as e:
                return {"mes": e}
    else:
        return {'mes': "Service cannot be found with the given name"}
    

@app.route('/send-deregister-request', methods=['GET'])
def manualDeregister():
    #get service information 
    serviceName = request.args.get('serviceName')
    serviceInfo = Provider.serviceInfoRequest(serviceName)
    if serviceInfo is not None:
        containerName = serviceInfo.get("containerName", "")
        param = {"containerName": containerName}
        mainRegistryFailed = False
        #Attempt with main registry
        try:
            registerURL = "http://registry:4004/deregister-service"
            response = try_deregister(registerURL,param)
            if response.status_code in [200, 400]:
                    response_data = {
                        "status_code": response.status_code,
                        "content": response.text  # You can adjust this based on the content type of the response
                    }
                    return {"mes": response_data}
            if response.status_code == 500:
                raise Exception("main registry failed")
        except (requests.exceptions.ConnectionError, Exception) as e:
            mainRegistryFailed = True

        #attempt with backup
        if mainRegistryFailed:
            try:
                
                backupregisterURL = "http://backupregistry:4005/deregister-service"
                response = try_deregister(backupregisterURL, param)
                # response = requests.post(backupregisterURL, json=serviceInfo)
                response_data = {
                    "status_code": response.status_code,
                    "content": response.text  # You can adjust this based on the content type of the response
                }
                mainRegistryFailed = False
                return {"mes": response_data}
            except requests.exceptions.RequestException as e:
                return {"mes": e}
            except Exception as e:
                return {"mes": e}
        
    else:
        return {'mes': "Service cannot be found with the given name"}
    
    
    mainRegistryFailed = False

    #attempt to deregister from main registry
    
    #send request to register into registry 

    if response.status_code == 200:
        response_data = {
            "status_code": response.status_code,
            "content": response.text  # You can adjust this based on the content type of the response
        }
        return {"mes": response_data}
    else:
        backupregisterURL = "http://backupregistry:4005/deregister-service"
        response = requests.delete(backupregisterURL, json=param)
        response_data = {
            "status_code": response.status_code,
            "content": response.text  # You can adjust this based on the content type of the response
        }
        return {"mes": response_data}
    

#Manual Deregister
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4003)