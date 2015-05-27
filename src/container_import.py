from src.log import Log
from src.file import File
from src.pfp_regex import pfp_regex
class Container(Log, File, pfp_regex):
	def __init__(self):
		pass
