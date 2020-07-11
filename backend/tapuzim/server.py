from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from functools import partial

app = Flask(__name__)
CORS(app)

mongo_client = MongoClient()
tapuzim_db = mongo_client.tapuzim
reports_collection = tapuzim_db.reports


def serialize_report(report):
    return dict(
        id=str(report['_id']),
        name=report['name'],
        status=report['status'],
        time=report['time'].timestamp(),
    )


def ensure_required_args(args, required):
    missing = set(required).difference(set(args.keys()))
    if missing:
        abort(400, f'Missing required args: {", ".join(missing)}')


@app.route('/report', methods=['POST'])
def create_report():
    args = request.get_json()
    ensure_required_args(args, ['name', 'status'])
    report_id = reports_collection.insert_one(dict(
        time=datetime.now(),
        name=str(args['name']),
        status=bool(args['status']),
    )).inserted_id

    return str(report_id)


@app.route('/report/all', methods=['GET'])
def get_all_reports():
    all_reports = reports_collection.find()
    return jsonify([serialize_report(r) for r in all_reports])


@app.route('/report/today', methods=['GET'])
def get_today_reports():
    midnight = datetime.combine(datetime.now(), datetime.min.time())
    today_reports = reports_collection.find({'time': {'$gt': midnight}})
    return jsonify([serialize_report(r) for r in today_reports])


if __name__ == '__main__':
    app.run()
