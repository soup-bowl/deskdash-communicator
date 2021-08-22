from http.server import BaseHTTPRequestHandler, HTTPServer
from shutil import Error
from urllib.parse import urlparse, parse_qs
from communicator.stats import Stats
from communicator.actions import Actions
from communicator.network import Network
import json
import time
import sys, os
import contextlib
if sys.platform.startswith('linux'):
	import daemon
	from daemon import pidfile

hostname = "0.0.0.0"
port     = 43594

class Server(BaseHTTPRequestHandler):
	"""Run a continuously serving HTTP server responding with system information and commands.
	"""
	def do_GET(self):
		"""Handles incoming GET requests to the server.
		"""
		input_key = parse_qs( urlparse(self.path).query).get('key', None)
		input_cmd = parse_qs( urlparse(self.path).query).get('cmd', None)
		input_net = parse_qs( urlparse(self.path).query).get('networkscan', None)

		currentdir = os.path.split(os.path.abspath(__file__))[0]
		use_key  = False
		key      = ''
		use_func = False
		use_scan = False
		try:
			with open(currentdir + "/config.json") as json_file:
				data = json.load(json_file)

				use_key  = data['auth'] if 'auth' in data else False
				key      = data['key'] if 'key' in data else ''
				use_func = data['permitCommands'] if 'permitCommands' in data else False
				use_scan = data['permitNetscan'] if 'permitNetscan' in data else False

		except FileNotFoundError:
			pass

		if use_key == False or ( use_key == True and ( input_key != None and input_key[0] == key ) ):
			# A key was provided and accepted, or password authentication is diabled.	
			if use_scan == True and input_net != None:
				# If network scan is enabled and requested, respond with network instead.
				all_devices = Network().get_all()
				self.fire_response(200, {
					'success': True,
					'content': all_devices
				})
			elif ( use_func == True and input_cmd != None and input_cmd[0] == "ls" ):
				# Command to list commands was issued.
				self.fire_response(200, {
					'success': True,
					'content': Actions( data ).list_actions()
				})
			elif ( use_func == True and input_cmd != None and input_cmd[0] != None ):
				# Command was issued.
				try:
					Actions( data ).run( input_cmd[0] )

					self.fire_response(200, {
						'success': True,
					})
				except Error:
					self.fire_response(400, {
						'success': False,
						'message': 'Incorrect command recieved.'
					})
			else:
				# No fancy stuff? Send the stat result, as per.
				self.fire_response(200, {
					'success': True,
					'content': Stats().get()
				})
		else:
			self.fire_response(401, {
				'success': False,
				'message': 'Either no key was provided, or it was incorrect.'
			})
	
	def set_headers(self, response_code, headers):
		"""Sets the response headers for the outgoing payload.

		Args:
			response_code (int): HTTP response code, corresponding to https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
			headers (dict): Dictionary of HTTP headers and their values.
		"""
		self.send_response(response_code)
		for key, value in headers.items():
			self.send_header(key, value)
		self.end_headers()
	
	def fire_response(self, code, respo):
		"""Sends off the payload response down the HTTP channel.

		Args:
			code (int): HTTP response code, corresponding to https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
			respo (mixed): Dictionary or array to serve as the JSON response.
		"""
		self.set_headers(code, {'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*'})
		self.wfile.write(bytes(json.dumps(respo), "utf-8"))

if __name__ == "__main__":
	# Has the user requested this to start as a daemon?
	daemon_mode  = False
	daemon_state = 0
	repo_url     = "https://github.com/soup-bowl/deskdash-communicator"
	for i in range(1, len(sys.argv)):
		if '--version' == sys.argv[i] or '-v' == sys.argv[i]:
			print("Deskdash Communicator API - Version 0.3-alpha.")
			print("This version is licensed under MIT.")
			print("<%s>" % repo_url)
			exit(0)
		elif '--help' == sys.argv[i] or '-h' == sys.argv[i]:
			print("Usage: command [-v|--version] [-h|--help] [-d|--daemon]")
			print("Opens up a JSON API of system information.")
			print("With no arguments, a temporary runner is opened in the current TTY, available until you cancel (ctrl-c) the command, or the TTY terminates.")
			print("")
			print("-v, --version   Prints the version number.")
			print("-h, --help      Shows this help information.")
			print("-d, --daemon    Runs the server as a daemon, continues after the TTY terminates.")
			print("")
			print("For more information, see the main repository at: <%s>" % repo_url)
			exit(0)
		elif '--daemon' == sys.argv[i] or '-d' == sys.argv[i]:
			try:
				if sys.argv[(i + 1)] == 'start':
					daemon_mode  = True
					daemon_state = 0
				if sys.argv[(i + 1)] == 'stop':
					daemon_mode  = True
					daemon_state = 1
			except IndexError:
				pass

	http_server = HTTPServer((hostname, port), Server)

	if (daemon_mode):
		if not sys.platform.startswith('linux'):
			print("Daemon mode only supports Linux for now.")
			exit(1)

		print("Deskdash Communicator - Daemon Mode (port %s)." % (port))
		daemon_context = daemon.DaemonContext(
			umask=0o002,
			files_preserve=[http_server.fileno()]
		)

		with daemon_context:
			http_server.serve_forever()
	else:
		print("Deskdash Communicator - Server started on port %s (ctrl-c to close)." % (port))

		try:
			http_server.serve_forever()
		except KeyboardInterrupt:
			pass

		http_server.server_close()
		print("Server stopped.")