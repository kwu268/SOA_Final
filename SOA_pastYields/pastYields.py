import json
from flask import Flask, jsonify, request
import requests 
from datetime import datetime
import socket

class pastYields:
    def __init__(self, stock_symbol, start_date, end_date):
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date

    def fetchData(self, stockTableName, startDate, endDate):
        pgURL = "http://pg:4006/postgres"
        
        # Fetch data from PostgreSQL
        yieldQuery = f"Select trade_date, closing_price from \"{stockTableName}\" where trade_date = (select min(ticker.trade_date) from \"{stockTableName}\" ticker where ticker.trade_date>=\'{startDate}\') or trade_date = (select max(ticker.trade_date) from \"{stockTableName}\" ticker where ticker.trade_date<=\'{endDate}\');"
        params = {'query': yieldQuery}
        response = requests.get(pgURL, params=params)
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result
        else:
            print(f"Error calling container1 endpoint: {response.status_code}")
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
    
    def calculateYield(self, initialValue, finalValue):        
        yieldPercent = ((finalValue['Closing Price']-initialValue['Closing Price'])/initialValue['Closing Price'])*100
        return yieldPercent
    
app = Flask(__name__)

@app.route('/info', methods=['GET'])
def getContainerInfo():
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    port = request.environ.get('SERVER_PORT')
    return jsonify({"containerName": "pastyields", "ipAddress": ipAddress, "port": port, "endPoints": {"selection": "pastyieldSelection", "service": "pastyields"}, "description": "Displays the total ROI for a requested stock/company within a requested date range"})

@app.route('/pastyieldSelection', methods=['GET'])
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

@app.route('/pastyields', methods=['GET'])
def past_yieldsAPI():
    stock_symbol = request.args.get('stock_symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    service = pastYields(stock_symbol, start_date, end_date)
    
    pgData = service.fetchData(service.stock_symbol, service.start_date, service.end_date)
    jsonData = service.processData(pgData)
    
    if(len(jsonData)==0):
        return {"message": "Error fetching data or no data available."}
    else:
        yieldPercent = service.calculateYield(jsonData[0], jsonData[-1]) 
        # print(f"{yieldPercent}%")
        return {"message": "Past Yields calculated successfully!", "yield_percent": yieldPercent}
    # return {"message": "test success"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)