from flask_session import Session
from flask import session, redirect, url_for, abort, send_from_directory
import os

class SecureFileRendering:
	def __init__(self, app=None):
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		self._set_interface(app)

	def _set_interface(self, app):
		self.app = app
		self.app.config['SESSION_TYPE'] = 'filesystem'
		Session(self.app)
		secure_route = self.app.config.get("SECURE_ROUTE_STRING", "/protected") 
		if secure_route.strip() == "" or secure_route.strip() == "/" or (len(secure_route.strip())>1 and secure_route.strip()[-1] == '/'):
			raise Exception("SECURE_ROUTE_STRING can't be blank or slash or have trailing slash. Corrent Route Eg: /test, /protected")
		sanitized_route = secure_route.strip() + "/<int:file_id>"
		self.app.add_url_rule(sanitized_route,"secure_file_endpoint",self._secure_file_endpoint)


	def _secure_file_endpoint(self, file_id:int):
		if "file_id" in session and session.get('file_id','')==file_id:
			path = session.get('path','')
			file = session.get('file','')
			session.pop('path', None)
			session.pop('file_id', None)
			session.pop('file', None)
			response = send_from_directory(path, file, as_attachment=True)
			if session.get("delete") and os.path.exists(os.path.join(path, file)):
				os.remove(os.path.join(path, file))

			return response
		else:
			abort(403)
		

	def securely_render_file(self, file_path:str|list|tuple, many: bool = False):
		if not many and not os.path.exists(file_path):
			abort(404)

		is_delete=False
		if many:
			if type(file_path) != list and type(file_path) != tuple:
				raise Exception("List or tuple of paths expected, for many=True")
			output_path = 'output.zip'
			from zipfile import ZipFile 
			with ZipFile(output_path,'w') as z:
				for f in file_path:
					if os.path.exists(f):
						z.write(f)
			file_path = output_path
			is_delete = True

		session["file_id"] = id(file_path)
		session['path'] = os.path.dirname(file_path)
		session['file'] = os.path.basename(file_path)
		session['delete'] = is_delete
		return redirect(url_for('secure_file_endpoint', file_id=session.get("file_id"), _external=True))
