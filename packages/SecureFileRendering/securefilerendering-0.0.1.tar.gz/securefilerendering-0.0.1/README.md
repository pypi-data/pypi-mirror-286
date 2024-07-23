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


@app.route("/download")
def test():
	path = "<path_of_the_file>"
	return sfr.securely_render_file(path)

if __name__ == '__main__':
	app.run()
```

## Dependencies

-	Flask-Session
-	Flask
