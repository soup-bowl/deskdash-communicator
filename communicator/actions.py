from shutil import Error
import subprocess
import platform


class Actions(object):
	"""Runs system interactions.
	"""
	def __init__(self, data):
		self.data = data

	def run(self, action):
		"""Executes a command from the API on the system.

		Args:
			action (string): The function called from the dashboard.

		Raises:
			Error: Command not found
		"""
		if action in self.data["commands"] and "function" in self.data["commands"][action]:
			act = self.data["commands"][action]
			if (act["function"] == 'dd-shutdown'):
				self.shutdown()
			else:
				cmd = act["function"].split()
				subprocess.call(cmd)

	
	def list_actions(self):
		"""Lists all the commands supported by the host.

		Returns:
			dict: Segment from the JSON config.
		"""
		return self.data["commands"]

	def shutdown(self):
		"""Shuts down the API host.
		"""
		if ( platform.system() == "Windows" ):
			subprocess.call(["shutdown", "/s", "/t", "10"])
		else:
			subprocess.call(["shutdown", "-h", "-t", "10"])
