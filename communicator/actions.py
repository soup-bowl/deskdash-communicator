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
			elif (act["function"] == 'dd-reboot'):
				self.reboot()
			elif (act["function"] == 'dd-volup'):
				self.volume_control("up")
			elif (act["function"] == 'dd-voldwn'):
				self.volume_control("down")
			elif (act["function"] == 'dd-volmute'):
				self.volume_control("mute")
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

	def reboot(self):
		"""Reboots the API host.
		"""
		if ( platform.system() == "Windows" ):
			subprocess.call(["shutdown", "/r", "/t", "10"])
		else:
			subprocess.call(["shutdown", "-r", "-t", "10"])

	def volume_control(self, act):
		"""Controls the audio output on the host system.

		Args:
			action (string): Desired command (from 'up', 'down' and 'mute').
		"""
		if ( act == "up" ):
			if ( platform.system() != "Windows" ):
				subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "5%+"])
		elif ( act == "down" ):
			if ( platform.system() != "Windows" ):
				subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "5%-"])
		elif ( act == "mute" ):
			if ( platform.system() != "Windows" ):
				subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "0%"])
		else:
			return

