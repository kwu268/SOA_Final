import psycopg2
from flask import Flask, jsonify, request

class PostgresAPI:
    def __init__(self):
        awsConnectionParamaters = {
            'dbname': 'stock_data',
            'user':'postgres',
            'password':'nazim4471',
            'host':'my-db-instance.cxjzjls8ya5o.us-east-2.rds.amazonaws.com',
            'port':'5432' }
        self.connection_params = awsConnectionParamaters

    def fetchDataFromDatabase(self, query):
        conn = psycopg2.connect(**self.connection_params)
        cursor = conn.cursor()

        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
        return data

app = Flask(__name__)

@app.route('/postgres', methods=['GET'])
def sendQuery():
    query = request.args.get('query')
    pg = PostgresAPI()
    results = pg.fetchDataFromDatabase(query)
    return jsonify(results)

@app.route('/test', methods=['GET'])
def sendQuery2():
    print("Request received for /test")
    mes = {"mes": "here"}
    return jsonify(mes)

if __name__ == "__main__":
    print("hi")
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    app.run(debug=True, host='0.0.0.0', port=4006)
    # pgTest = PostgresAPI()
    # q = "SELECT * FROM \"STOCKS\";"
    # print(pgTest.fetchDataFromDatabase(q)) 