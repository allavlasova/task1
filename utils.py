__author__ = 'alla'
import ujson as json
from flask import Response
import datetime


def make_result(value):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {'result': value, 'time': time}

def make_response(result):
    return Response(mimetype='application/json', response=json.dumps(make_result(result)))


