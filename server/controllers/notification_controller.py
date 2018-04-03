from flask import Blueprint, request, abort, json

from server.modules import fcm

notifications = Blueprint('notifications', __name__)


@notifications.route('/notify', methods=['POST'])
def notify():
    """
    POST notify
    JSON Body:
        topic
            FCM topic to notify
        start_time, end_time
            Time range for app to filter upon
    """

    topic = request.json.get('topic')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')

    if not all((topic, start_time, end_time)):
        abort(400, {'message': 'Missing data for notification'})

    notification_msg = 'Sorting complete! Tap to see results.'

    data = {
        'start_time': start_time,
        'end_time': end_time,
    }

    fcm.send_notification(topic, notification_msg, data, 'MainMenu')

    response = {
        'message': 'Notification sent'
    }

    return json.dumps(response)
