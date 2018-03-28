from flask import Blueprint, request

from server.modules import fcm

notifications = Blueprint('notifications', __name__)


"""
POST notify
Body must contain start and end times of the cycle
"""
@notifications.route('/notify', methods=['POST'])
def notify():
    topic = request.json.get('topic')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')

    notification_msg = 'Sorting complete! Tap to see results.'

    data = {
        'start_time': start_time,
        'end_time': end_time,
    }

    fcm.send_notification(topic, notification_msg, data, 'MainMenu')

    return 'Notification sent'
