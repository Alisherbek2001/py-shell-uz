from app import PyShellApp
from middleware import Middleware

app = PyShellApp()


@app.route("/home")
def home(request, response):
    response.text = "Hello, from the home page!"


@app.route("/about")
def about(request, response):
    response.text = "This is the about page."


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}!"


@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "List of books"

    def post(self, request, response):
        response.text = "Book created"


def new_handler(req, res):
    res.text = "This is a new handler response!"


app.add_route("/new_handler", new_handler)


@app.route("/template")
def template_handler(req, res):
    res.body = app.template(
        "home.html", context={"new_title": "New title", "new_body": "Best body 123"}
    )


def on_exception(req, res, exc):
    res.status = 500
    res.text = f"An error occurred: {exc}"


app.add_exception_handler(on_exception)


@app.route("/exception")
def exception_throwing_handler(req, res):
    raise AttributeError("some exception")


class LoggingMiddleware(Middleware):

    def __init__(self, app):
        super().__init__(app)

    def process_request(self, request):
        print("request is being called", request.url)

    def process_response(self, request, response):
        print("response has been  called", request.url)


app.add_middleware(LoggingMiddleware)
