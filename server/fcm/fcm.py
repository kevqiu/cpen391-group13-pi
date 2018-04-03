from pyfcm import FCMNotification


class FCM:
    """
    Firebase Cloud Messaging Client Module.
    Leverages pyfcm library for API requests
    """

    def __init__(self):
        self.push_service = None


    def init_push_service(self, api_key):
        self.push_service = FCMNotification(api_key=api_key)


    def send_notification(self, topic, message, data, click_action):
        self.push_service.notify_topic_subscribers(topic_name=topic,
                                                   message_body=message,
                                                   data_message=data,
                                                   click_action=click_action)
