import sys
from src.container_import import Container
from src.manager import Manager

class XmlConfig(Container):
	def get_data(self, id_login):
		m = Manager()
		return m.get_xml_data_by_id(id_login)
