"""
Simplify requests writing
"""

import requests

def x_www_request(headers, body):
    """Serialize the body and send the request"""

    body_str = ""

    for key in body.keys():
        body_str+=f"{key}={body[key]}&"

    body_str = body_str[:-1]

    rq = requests.post(request_IRL, data=body_str, headers=headers)

    if not rq.ok:
        throw Exception("Something bad happened with the request.")

    return json.loads(rq.content.decode('utf-8'))
