from flask import Blueprint, request

from server.extensions import fcm

notifications = Blueprint('notifications', __name__)


"""
POST notify
Body must contain the values for Red, Green, Blue, and Other
"""
@notifications.route('/notify', methods=['POST'])
def notify():
    red = request.json.get('red')
    green = request.json.get('green')
    blue = request.json.get('blue')
    other = request.json.get('other')

    notification_msg = 'Sorting complete! Results - Red: {0}, Green: {1}, Blue: {2}, Other: {3}' \
        .format(red, green, blue, other)

    fcm.send_notification("sort", notification_msg)

    return 'Notification sent'
