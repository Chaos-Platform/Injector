from flask import Flask,request
import injector
import os

db_url = os.environ.get("DB_API", "http://chaos.db.openshift:5001")
server_port = int(os.environ.get("SERVER_PORT", 5002))


app = Flask(__name__)
injection_slave = injector.Injector(db_url)

@app.route('/inject_fault',methods=['GET'])
def get_instructions():
    return "send dns and fault name in json object"

@app.route('/inject_fault',methods=['POST'])
def inject_fault():
    dns = request.json['dns']
    fault = request.json['fault']
    output = call_slave(dns,fault)
    return output

def call_slave(dns,fault):
    output = injection_slave.start_experiment(dns, fault)
    return  output
if __name__ == '__main__':
    app.run(host='0.0.0.0', port= server_port)
