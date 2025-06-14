from app import PyShellApp

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