import os
import requests
import json
from rest_framework.response import Response

def log_event(event_type: str, request=None, endpoint=None, content=None, headers=None):
    """
    Logs an event to the Rakam Analytics API.

    Parameters:
    event_type (str): The type of event to log.
    request (Request, optional): The Django REST Framework request object.
    endpoint (str, optional): The endpoint of the event.
    content (dict, optional): The content of the event.
    headers (dict, optional): The headers for the request.xe
    """
    if request:
        try:
            event_data = {
                "endpoint": request.path,
                "type": event_type,
                "content": json.loads(request.body.decode('utf-8')),
                "company": os.getenv("ANALYTICS_COMPANY", None),
                "project": os.getenv("ANALYTICS_PROJECT", "BASE")
            }
        except json.JSONDecodeError:
            return Response("Invalid JSON in request body", status=400)

        headers = {k: v for k, v in request.headers.items()}

    else:
        event_data = {
            "endpoint": endpoint,
            "type": event_type,
            "content": content,
            "company": os.getenv("ANALYTICS_COMPANY", None),
            "project": os.getenv("ANALYTICS_PROJECT", "BASE")
        }
        if not headers:
            headers={}

    url = os.getenv("ANALYTICS_URL", None)
    if not url:
        return Response("Analytics URL not configured. Please add ANALYTICS_URL to your environment file.", status=500)

    # Call Rakam Analytics Endpoint
    try:
        response = requests.post(url=url, json=event_data, headers=headers, timeout=10)
        if response.status_code != 201:
            return Response("External service is down", status=503)
    except requests.exceptions.RequestException as request_exception:
        return Response(str(request_exception), status=503)

    return Response({"message": "Event logged successfully"}, status=201)
