import json
from flask import Flask, jsonify, request
import requests 
from datetime import datetime
import socket


class dataDisplayer:
    def __init__(self, stock_symbol, start_date, end_date):
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date

    def fetchData(self, stockTableName, startDate, endDate):
        pgURL = "http://pg:4006/postgres"
        
        # Fetch data from PostgreSQL
        displayQuery = f"SELECT trade_date, closing_price from \"{stockTableName}\" where trade_date >=\'{startDate}\' and trade_date <=\'{endDate}\';"
        params = {'query': displayQuery}
        response = requests.get(pgURL, params=params)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            print(f"Error calling container2 endpoint: {response.status_code}")
            return {"message": f"Error calling pg container endpoint: {response.status_code}"}

    
    def processData(self, pgRawData):
        
        processed_data = []
        for row in pgRawData:
            # Process each row, convert it to JSON
            trade_date_object = datetime.strptime(row[0], '%a, %d %b %Y %H:%M:%S GMT')
            trade_date_formatted = trade_date_object.strftime('%Y-%m-%d')

            json_row = {'Trade Date': trade_date_formatted, 'Closing Price': row[1]}  
            processed_data.append(json_row)

        # Convert processed data to JSON
        json_data = json.loads(json.dumps(processed_data))
        return json_data
    
    
app = Flask(__name__)

@app.route('/info', methods=['GET'])
def getContainerInfo():
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    port = request.environ.get('SERVER_PORT')
    return jsonify({"containerName": "datadisplayer", "ipAddress": ipAddress, "port": port, "endPoints": {"selection": "displaySelection", "service": "displayData"}, "description": "Displays company's roi over a period of time as a line graph"})


@app.route('/displaySelection', methods=['GET'])
def getAvailableStocks():
    pgURL = "http://pg:4006/postgres"
    query = f"SELECT stock_symbol, stock_name from \"STOCKS\" order by stock_symbol asc;"

    params = {'query': query}
    response = requests.get(pgURL, params=params)
    if response.status_code == 200:
        result = response.json()
        processed_data = []
        for row in result:
            json_row = {"symbol": row[0], "companyName": row[1]}
            processed_data.append(json_row)
        # Convert processed data to JSON

        return jsonify(processed_data)

    else:
        print(f"Error calling container2 endpoint: {response.status_code}")
        return {"message": f"Error calling pg container endpoint: {response.status_code}"}
    
@app.route('/displayData', methods=['GET'])
def renderingDataAPI():
    stock_symbol = request.args.get('stock_symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    service = dataDisplayer(stock_symbol, start_date, end_date)
    
    pgData = service.fetchData(service.stock_symbol, service.start_date, service.end_date)
    jsonData = service.processData(pgData)
    
    if(len(jsonData)==0):
        return {"message": "Error fetching data or no data available."}
    else:
        return jsonify(jsonData)
    # TODO will need to add a way to use this json data to show it in a graph format. 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4001)