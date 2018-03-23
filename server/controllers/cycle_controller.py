from datetime import datetime
from flask import Blueprint, request, abort

from server.models.cycle_model import Cycle, CycleSchema
from server.modules import db

cycles = Blueprint('cycles', __name__)


"""
GET All Cycles
"""
@cycles.route('/cycles', methods=['GET'])
def get_all_cycles():
    return CycleSchema(many=True).jsonify(Cycle.query.all())


"""
GET Cycles by Id
"""
@cycles.route('/cycles/<int:id>', methods=['GET'])
def get_cycle(id):
    return CycleSchema().jsonify(Cycle.query.get(id))

"""
POST a cycle
Requires start and end time, start must be before end
"""
@cycles.route('/cycles', methods=['POST'])
def create_cycle():
    start = request.json.get('start_time')
    end = request.json.get('end_time')

    if not all ({start, end}):
        abort(400, {'message: Missing data for cycle'})

    start_time = datetime.strptime(start.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")
    end_time = datetime.strptime(end.split('+')[0], "%Y-%m-%dT%H:%M:%S.%f")

    if start_time > end_time:
        abort(400, {'message': 'Start time cannot be past end time'})

    cycle = Cycle(start_time=start_time, end_time=end_time)
    db.session.add(cycle)
    db.session.commit()

    return 'Cycle created with Start Time = {} and End Time = {}'.format(start_time, end_time)