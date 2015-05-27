import csv, sys
from src.container_import import Container
class WriteCsv(Container):
	def csv_handler(self, name, line_header):
		csv_file = self.get_path_csv(name)
		with open(csv_file, 'a+') as csvfile:
			handler = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			handler.writerow(line_header)
	"""		
	def write_header(self, handler, line_header):
		handler.writerow(line_header)
		
	def write_body(self, handler, line):
		handler.writerow(line)
	"""
