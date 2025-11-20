# notifiers/push_placeholder.py
"""
Placeholder & pseudo-code for mobile push (Firebase / OneSignal).

You can implement later with:
- Firebase Cloud Messaging (FCM) server API
- or OneSignal REST API

Pseudo:

def send_push(title, body, token_or_topic):
    # using Firebase Admin or OneSignal HTTP API
    # Build payload
    # POST to FCM or OneSignal
    pass

"""
def send_push(title: str, body: str, target: str):
    print("PUSH: (placeholder) ", title, body, target)
    # implement when you have FCM or OneSignal keys
