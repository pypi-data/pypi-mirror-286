import os
import requests
import json
from functools import wraps
from rest_framework.response import Response
from rest_framework.request import Request

def register_endpoint_event(event_type: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            # Determine if this is a class-based view (CBV) or function-based view (FBV)
            if isinstance(args[0], Request):
                # Function-based view (FBV)
                request = args[0]
                view_instance = None
                func_args = args[1:]
            else:
                # Class-based view (CBV)
                view_instance = args[0]
                request = args[1]
                func_args = args[2:]

            # Build the Data
            body = request.body.decode('utf-8')
            if not body:
                body = {}

            event_data = {
                "endpoint": request.path,
                "type": event_type,
                "content": body,
                "company": os.getenv("ANALYTICS_COMPANY", None),
                "project": os.getenv("ANALYTICS_PROJECT", "BASE")
            }

            # Extract headers from the incoming request
            headers = {k: v for k, v in request.headers.items()}
            headers["Content-Type"] = "application/json"

            # Rakam Analytics API event URL
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

            # Call the original view
            if view_instance:
                return view_func(view_instance, request, *func_args, **kwargs)
            else:
                return view_func(request, *func_args, **kwargs)
        return _wrapped_view
    return decorator
