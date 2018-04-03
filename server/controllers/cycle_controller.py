from datetime import datetime
from flask import Blueprint, request, abort, json

from server.models.cycle_model import Cycle, CycleSchema
from server.modules import db

cycles = Blueprint('cycles', __name__)


@cycles.route('/cycles', methods=['GET'])
def get_all_cycles():
    """
    GET All Cycles
    """
    return CycleSchema(many=True).jsonify(Cycle.query.all())


@cycles.route('/cycles/<int:id>', methods=['GET'])
def get_cycle(id):
    """
    GET Cycle by Id
    """
    return CycleSchema().jsonify(Cycle.query.get(id))


@cycles.route('/cycles', methods=['POST'])
def create_cycle():
    """
    POST a cycle
    JSON Body:
        start_time
            start time of the auto sort cycle
    """

    start = request.json.get('start_time')

    if not start:
        abort(400, {'message': 'Start time missing from body'})

    # parse datetime into DateTime to be stored in database
    start_time = datetime.strptime(start.split('+')[0].replace('T', ' '), "%Y-%m-%d %H:%M:%S.%f")

    cycle = Cycle(start_time=start_time, end_time=start_time)
    db.session.add(cycle)
    db.session.commit()
    db.session.flush()

    response = {
        'id': cycle.id,
        'message': 'Cycle created with Start Time = {}'.format(start_time)
    }
    return json.dumps(response)


@cycles.route('/cycles/<int:id>', methods=['PATCH'])
def patch_cycle(id):
    """
    PATCH a Cycle
    Id:
        id of the cycle to be modified
    JSON Body:
        end_time
            end time of the auto sort cycle
    """

    end = request.json.get('end_time')

    if not end:
        abort(400, {'message': 'End time missing from body'})

    end_time = datetime.strptime(end.split('+')[0].replace('T', ' '), "%Y-%m-%d %H:%M:%S.%f")

    Cycle.query.filter(Cycle.id == id).update({'end_time': end_time})
    db.session.commit()

    response = {
        'message': 'Cycle updated successfully'
    }

    return json.dumps(response)