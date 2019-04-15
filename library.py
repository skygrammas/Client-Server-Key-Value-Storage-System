"""A set of libraries that are useful to both the proxy and regular servers."""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# The Python socket API is based closely on the Berkeley sockets API which
# was originally written for the C programming language.
#
# https://en.wikipedia.org/wiki/Berkeley_sockets
#

import socket
import time
import csv

# Read this many bytes at a time of a command. Each socket holds a buffer of
# data that comes in. If the buffer fills up before you can read it then TCP
# will slow down transmission so you can keep up. We expect that most commands
# will be shorter than this.
COMMAND_BUFFER_SIZE = 256


def CreateServerSocket(port):
		"""Creates a socket that listens on a specified port.

		Args:
			port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
					all predefined ports represent insecure protocols that have died out.
		Returns:
			An socket that implements TCP/IP.
		"""
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(('localhost', port))
		server.listen()
		return server


def ConnectClientToServer(server_sock):
		# Wait until a client connects and then get a socket that connects to the client.
		# server_sock.listen()
		return server_sock.accept()


def CreateClientSocket(server_addr, port):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((server_addr, port))
		return client


def ReadCommand(sock):
	"""Read a single command from a socket. The command must end in newline."""
	data = ""
	while '\n' not in data:
		buffer = sock.recv(COMMAND_BUFFER_SIZE)
		data += str(buffer, 'utf-8')
	return data
				


def ParseCommand(command):
		"""Parses a command and returns the command name, first arg, and remainder.

		All commands are of the form:
				COMMAND arg1 remaining text is called remainder
		Spaces separate the sections, but the remainder can contain additional spaces.
		The returned values are strings if the values are present or `None`. Trailing
		whitespace is removed.

		Args:
			command: string command.
		Returns:
			command, arg1, remainder. Each of these can be None.
		"""
		args = command.strip().split(' ')
		command = None
		if args:
				command = args[0]
		arg1 = None
		if len(args) > 1:
				arg1 = args[1]
		remainder = None
		if len(args) > 2:
				remainder = ' '.join(args[2:])
		return command, arg1, remainder


class KeyValueStore(object):
		"""A dictionary of strings keyed by strings.

		The values can time out once they get sufficiently old. Otherwise, this
		acts much like a dictionary.
		"""

		def __init__(self):
				self.store = {}
				with open('storage.csv', mode='r') as csv_file:
					csv_reader = csv.DictReader(csv_file)
					line_count = 0
					for row in csv_reader:
						if line_count == 0:
							line_count += 1
						self.store[row["key"]]['value'] = row["value"]
						self.store[row["key"]]['time'] = row["time"]
						line_count += 1

		def GetValue(self, key, max_age_in_sec=None):
				"""Gets a cached value or `None`.

				Values older than `max_age_in_sec` seconds are not returned.

				Args:
					key: string. The name of the key to get.
					max_age_in_sec: float. Maximum time since the value was placed in the
						KeyValueStore. If not specified then values do not time out.
				Returns:
					None or the value.
				"""
				if key in self.store:
						if max_age_in_sec and ((int(time.time()) - int(self.store[key]['time'])) < max_age_in_sec):
								return self.store[key]['value']
						elif not max_age_in_sec:
								return self.store[key]['value']
				return None

		def StoreValue(self, key, value):
				"""Stores a value under a specific key.

				Args:
					key: string. The name of the value to store.
					value: string. A value to store.
				"""
				self.store[key] = {}
				self.store[key]['value'] = value
				self.store[key]['time'] = time.time()

		def Keys(self):
				"""Returns a list of all keys in the datastore."""
				keys = []
				for key in self.store:
						keys.append(key)
				return keys
