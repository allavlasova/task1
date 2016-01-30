__author__ = 'alla'
from flask import Flask, request
from werkzeug.exceptions import abort
import ujson as json
from utils import make_response

app = Flask(__name__)
dict= {}
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
        except KeyError:
            abort(400)
        if(dict.get(key) != None):
            abort(409)
        else:
            dict.update({key : value})
            return make_response(value)
    elif(request.method == 'PUT'):
        data = json.loads(request.data)
        try:
           key = data['key']
           value = data['value']
        except KeyError:
            abort(400)
        if(dict.get(key) == None):
            abort(404)
        else:
            dict[key] = value
            return make_response(value)
    elif(request.method == 'DELETE'):
        data = json.loads(request.data)
        try:
            key = data['key']
        except KeyError:
            abort(404)
        if(dict.get(key) != None):
            dict.pop(key)
        return make_response(None)


if __name__ == '__main__':
    app.run()