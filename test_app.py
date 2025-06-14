import pytest
from app import PyShellApp


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