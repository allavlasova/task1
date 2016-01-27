__author__ = 'alla'
from flask import Flask, request
from werkzeug.exceptions import abort
import ujson as json
from flask import Response
import datetime

app = Flask(__name__)

dict= {}

def make_response(result):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Response(mimetype='application/json', response=json.dumps({'result': result, 'time': time}))


@app.route('/dictionary/', methods=['POST','GET', 'PUT', 'DELETE'])
def dictionary():
    if(request.method == 'GET'):
        key = request.args.get('key')
        try:
            result = dict[key]
        except KeyError:
            abort(404)
        return make_response(result)
    elif(request.method == 'POST'):
        data = json.loads(request.data)
        try:
           key = data['key']
           value = data['value']
        except (KeyError):
            abort(400)
        if(dict.get(key) != None):
            abort(409)
        else:
            dict.update({key : value})
            return make_response(value)
    elif(request.method == 'PUT'):
        key = request.args.get('key')
        value = request.args.get('value')
        if key == None or value == None:
            abort(400)
        if(dict.get(key) == None):
            abort(404)
        else:
            dict[key] = value
            return make_response(value)
    elif(request.method == 'DELETE'):
        key = request.args.get('key')
        if(dict.get(key) != None):
            dict.pop(key)
        return make_response(None)


if __name__ == '__main__':
     app.run()