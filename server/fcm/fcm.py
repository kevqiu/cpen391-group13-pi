from pyfcm import FCMNotification


class FCM:

    def __init__(self):
        self.push_service = None


    def init_push_service(self, api_key):
        self.push_service = FCMNotification(api_key=api_key)


    def send_notification(self, topic, message):
        print("hello")
        self.push_service.notify_topic_subscribers(topic_name=topic, message_body=message)
