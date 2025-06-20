from webob import Response as WebobResponse
import json


class Response:
    def __init__(self):
        self.json = None
        self.html = None
        self.text = None
        self.body = b""
        self.content_type = None
        self.status = 200

    def set_body_and_content_type(self):
        if self.json is not None:
            self.body = json.dumps(self.json).encode()
            self.content_type = "application/json"

        if self.html is not None:
            self.body = self.html.encode()
            self.content_type = "text/html"

        if self.text is not None:
            self.body = self.text
            self.content_type = "text/plain"

    def __call__(self, environ, start_response):

        self.set_body_and_content_type()
        response = WebobResponse(
            body=self.body, content_type=self.content_type, status=self.status
        )
        return response(environ, start_response)
