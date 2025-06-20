import pytest
from middleware import Middleware


def test_basic_route_adding(app):

    @app.route("/home")
    def home(req, res):
        res.text = "Hello, from the home page!"


def test_duplicate_routes_throws_exception(app):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello, from the home page!"

    with pytest.raises(AssertionError):

        @app.route("/home")
        def home2(req, res):
            res.text = "Hello, from the home page!"


def test_can_be_sent_by_test_client(app, test_client):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello, from the home page!"

    response = test_client.get("http://testserver/home")

    assert response.text == "Hello, from the home page!"


def test_parameterized_route(app, test_client):
    @app.route("/hello/{name}")
    def home(req, res, name):
        res.text = f"Hello, {name}"

    assert test_client.get("http://testserver/hello/Alisher").text == f"Hello, Alisher"
    assert (
        test_client.get("http://testserver/hello/Jahongir").text == f"Hello, Jahongir"
    )


def test_default_response(test_client):
    response = test_client.get("http://testserver/unknown")

    assert response.status_code == 404
    assert response.text == "Not Found"


def test_class_based_get(app, test_client):
    @app.route("/books")
    class Books:
        def get(self, req, res):
            res.text = "Books page"

    assert test_client.get("http://testserver/books").text == "Books page"


def test_class_based_post(app, test_client):
    @app.route("/books")
    class Books:
        def post(self, req, res):
            res.text = "Book created"

    assert test_client.post("http://testserver/books").text == "Book created"


def test_class_based_method_not_allowed(app, test_client):
    @app.route("/books")
    class Books:
        def get(self, req, res):
            res.text = "Books page"

    response = test_client.post("http://testserver/books")

    assert response.status_code == 405
    assert response.text == "Method Not Allowed"


def test_alternative_route_adding(app, test_client):
    def new_handler(req, res):
        res.text = "This is a new handler response!"

    app.add_route("/new_handler", new_handler)

    assert (
        test_client.get("http://testserver/new_handler").text
        == "This is a new handler response!"
    )


def test_template_handler(app, test_client):
    @app.route("/test-template")
    def template(req, res):
        res.body = app.template(
            "home.html", context={"new_title": "Best title", "new_body": "Best body"}
        )
        res.status = 200

    response = test_client.get("http://testserver/test-template")

    assert response.status_code == 200
    assert "Best title" in response.text
    assert "Best body" in response.text
    assert "text/html" in response.headers["Content-Type"]


def test_custom_exception_handler(app, test_client):
    def on_exception(req, res, exc):
        res.status = 500
        res.text = "Something went wrong: "

    app.add_exception_handler(on_exception)

    @app.route("/exception")
    def exception_throwing_handler(req, res):
        raise AttributeError("some exception")

    response = test_client.get("http://testserver/exception")
    assert response.text == "Something went wrong: "
    assert response.status_code == 500


def test_non_existent_static_file(test_client):
    assert (
        test_client.get("http://testserver/static/non_existent_file.txt").status_code
        == 404
    )


def test_serving_static_file(test_client):
    response = test_client.get("http://testserver/static/test.css")
    assert response.text == "body {background-color: chocolate;}"


def test_middleware_methods_are_called(app, test_client):
    process_request_called = False
    process_response_called = False

    class SimpleMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, request):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, request, response):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(SimpleMiddleware)

    @app.route("/home")
    def index(req, res):
        res.text = "from handler!"

    test_client.get("http://testserver/home")

    assert process_request_called is True
    assert process_response_called is True


def test_allowed_methods_for_fucntion_based_handler(app, test_client):
    @app.route("/home", allowed_methods=["post"])
    def home(req, res):
        res.text = "Hello, from the home page!"

    res = test_client.get("http://testserver/home")
    assert res.status_code == 405
    assert res.text == "Method Not Allowed"


def test_json_response_helper(app, test_client):
    @app.route("/json")
    def json_handler(req, res):
        res.json = {"name": "pyshelleuz"}

    res = test_client.get("http://testserver/json")
    res_data = res.json()
    assert res.headers["Content-Type"] == "application/json"
    assert res_data["name"] == "pyshelleuz"


def test_text_response_helper(app, test_client):
    @app.route("/text")
    def text_handler(req, res):
        res.text = "This is a text response"

    res = test_client.get("http://testserver/text")
    assert "text/plain" in res.headers["Content-Type"]
    assert res.text == "This is a text response"


def test_html_response_helper(app, test_client):
    @app.route("/html")
    def html_handler(req, res):
        res.html = app.template(
            "home.html", context={"new_title": "Best title", "new_body": "Best body"}
        )

    res = test_client.get("http://testserver/html")
    assert "text/html" in res.headers["Content-Type"]
    assert "Best title" in res.text
    assert "Best body" in res.text
