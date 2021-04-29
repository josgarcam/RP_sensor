from flask import jsonify


def to_json(*args, **kwargs):
    return jsonify(*args, **kwargs)