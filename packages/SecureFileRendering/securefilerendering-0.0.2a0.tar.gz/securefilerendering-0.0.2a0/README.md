# SecureFileRendering

## Installing

Install and update using pip:

```py
$ pip install SecureFileRendering
```

## A Simple Example

```py
from SecureFileRendering import SecureFileRendering

app = Flask(__name__)
app.config['SECURE_ROUTE_STRING'] = "/test"
sfr = SecureFileRendering(app)

@app.route("/downloadpdf")
def test_pdf():
	path = "static/a.pdf"
	return sfr.securely_render_file(path)

@app.route("/downloadzip")
def test_zip():
	paths = ["static/a.pdf"]
	return sfr.securely_render_file(paths, many=True)

if __name__ == '__main__':
	app.run()
```

## Dependencies

-	Flask-Session
-	Flask

## Description

Mention any path of a file and render the file securely without exposing the folder structure. File will be downloaded with a secure link which can be accessed only once. Example: /test/12345678