from flask import Flask
from flask import request, jsonify

from controller import Controller

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route("/api/v1/bus_sec", methods=['GET'])
def bus_sec():

    if request.method == 'GET':
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if not start_time or not end_time:
            return 'Request missing start time or end time'

    data = {}
    data['start_time'] = start_time
    data['end_time'] = end_time

    cntrl = Controller()
    answer = cntrl.process(data)

    return answer

def main_run():
    app.run(debug=True)

if __name__ == "__main__":
    main_run()
