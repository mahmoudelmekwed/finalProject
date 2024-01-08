import flask

app = flask.Flask("Online Store")

def get_html(page_name):
    html_file = open(page_name + ".html")
    content = html_file.read()
    html_file.close()
    return content

@app.route("/")
def home():
    return get_html("index")