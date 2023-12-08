import json
from flask import Flask, jsonify, request
import requests 
from datetime import datetime
import socket

class rankBySector:
    def __init__(self, stock_symbol, start_date, end_date):
        self.stock_symbol = stock_symbol
        self.start_date = start_date
        self.end_date = end_date 

    def fetchData(self, stock_symbol):
        pgURL = "http://pg:4006/postgres"
        
        # Fetch data from PostgreSQL
        
        getSector = f"SELECT stock_gics_sector from \"STOCKS\" where stock_symbol = \'{self.stock_symbol}\';"
        params = {'query': getSector}
        response = requests.get(pgURL, params=params)
        if response.status_code == 200:
            stock_sector = response.json()

            getAllCompaniesInSector = f"SELECT stock_symbol, stock_name from \"STOCKS\" where stock_gics_sector = \'{stock_sector[0][0]}\' ;"
            params = {'query': getAllCompaniesInSector}
            response = requests.get(pgURL, params=params)

            if response.status_code == 200:
                result = response.json()
                print(result)
                return result
            else:
                print(f"Error calling container3 endpoint: {response.status_code}")
                return {"message": f"Error calling pg container endpoint: {response.status_code}"}
            
        else:
            print(f"Error calling container3 endpoint: {response.status_code}")       
            return {"message": f"Error calling pg container endpoint: {response.status_code}"}
        
        # 

    
    def processData(self, pgRawData):
        
        processed_data = []
        for row in pgRawData:
            # Process each row, convert it to JSON
            json_row = {'Stock Symbol': row[0], 'Stock Name': row[1]}  
            processed_data.append(json_row)
            
        # Convert processed data to JSON
        json_data = json.loads(json.dumps(processed_data))
        return json_data
    
    def getIndividualCompanyData(self, companiesJsonData):
        # Fetch data from PostgreSQL
        individualDataDict = {}
        pgURL = "http://pg:4006/postgres"
        for row in companiesJsonData:
            stockSymbol = row['Stock Symbol']
            stockName = row['Stock Name']
            individualCompanyData = f" Select trade_date, closing_price from \"{row['Stock Symbol']}\" where trade_date = (select min(ticker.trade_date) from \"{row['Stock Symbol']}\" ticker where ticker.trade_date>=\'{self.start_date}\') or trade_date = (select max(ticker.trade_date) from \"{row['Stock Symbol']}\" ticker where ticker.trade_date<=\'{self.end_date}\');"
            #this is a postgres fetch
            # postgresData = self.postgres_api.fetchDataFromDatabase(individualCompanyData)
            params = {'query': individualCompanyData}
            response = requests.get(pgURL, params=params)
            if response.status_code == 200:
                postgresData = response.json()
                if len(postgresData)!=0:
                    firstDataRow = postgresData[0]
                    lastDataRow = postgresData[-1]
                    performance = ((lastDataRow[1]-firstDataRow[1])/firstDataRow[1])*100
                    individualDataDict[stockSymbol] = (stockName, performance)
            else:
                print(f"Error calling container3 endpoint: {response.status_code}")            
                return {"message": f"Error calling pg container endpoint: {response.status_code}"}
            
            
            #sorting the dictionary 
        individualDataDictSorted = dict(sorted(individualDataDict.items(), key=lambda item: item[1][1], reverse = True))
        return individualDataDictSorted
    
    
app = Flask(__name__)

@app.route('/info', methods=['GET'])
def getContainerInfo():
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    port = request.environ.get('SERVER_PORT')
    return jsonify({"containerName": "ranker", "ipAddress": ipAddress, "port": port, "endPoints": {"selection": "rankSelection", "service": "rankbysector"}, "description": "Ranks the companies by their roi over a date range"})

@app.route('/rankSelection', methods=['GET'])
def getAvailableStocks():
    pgURL = "http://pg:4006/postgres"
    query = f"SELECT * from \"STOCKS\" order by stock_symbol asc;"

    params = {'query': query}
    response = requests.get(pgURL, params=params)
    if response.status_code == 200:
        result = response.json()
        processed_data = []
        for row in result:
            json_row = {"symbol": row[0], "companyName": row[2], "sector": row[1]}
            processed_data.append(json_row)
        # Convert processed data to JSON

        return jsonify(processed_data)

    else:
        print(f"Error calling container2 endpoint: {response.status_code}")
        return {"message": f"Error calling container2 endpoint: {response.status_code}"}
    
@app.route('/rankbysector', methods=['GET'])
def renderingDataAPI():
    stock_symbol = request.args.get('stock_symbol')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    service = rankBySector(stock_symbol, start_date, end_date)
    
    pgData = service.fetchData(service.stock_symbol)
    
    companiesDataJson = service.processData(pgData)
    
    if(len(companiesDataJson)==0):
        return {"message": "Error fetching data or no data available."}
    else:
        companiesDataDict = service.getIndividualCompanyData(companiesDataJson)
        inputtedTickerIndex = list(companiesDataDict).index(stock_symbol)
        firstFiveDictItems = list(companiesDataDict.items())
            # print(inputtedTickerIndex)
            # print(f'\n{firstFiveDictItems}')
        return jsonify((inputtedTickerIndex, firstFiveDictItems))    # TODO will need to add a way to use this json data to show it in a graph format. 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4002)