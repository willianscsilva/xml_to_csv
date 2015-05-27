from src.container_import import Container
from src.write_csv import WriteCsv

from ctypes import *
import sys,pprint
class ParseXml(Container):
	def switch(self, args):		
		if args['multiline'] == True:
			self.parse_line(args['content_pointer'])
		else:
			self.parse_all_content(args)
		
	def parse_line(self,line_pointer):
		try:
			pass
			
		except Exception, e:
			self.log_msg("ERRO: ParseXml.parse_line() "+str(e),"log.txt")
			
	def parse_all_content(self,args):
		try:
			nome = "csv_data_%s"%(args['id_login'])
			w_csv = WriteCsv()
			# O bloco abaixo e para manter a ordem dos campos, 
			# com os campos da tabela de xml.
			ordem_campos_xml = args['config_xml']['ordem_campos_xml'].split(",")			
			list_campos  = []
			list_header = ['id', 'title', 'link', 'image_link', 'product_type', 'price', 'sale_price', 'mounth', 'amount', 'description', 'brand', 'cidade', 'estado', 'pais', 'data_inicio', 'data_fim', 'price', 'sale_price', 'availability', 'gtin', 'estabelecimento']
			
			line = ""
			list_csv = []
			arr_dict = {}
			
			for campos_xml in list_header:
				if campos_xml in ordem_campos_xml:
					list_campos.append(campos_xml)
				else:
					# Se o campo que nao foi encontrado em 'ordem_campos_xml',
					# e esse campo for 'sale_price', troca para 'price'.
					if campos_xml == "sale_price":
						list_campos.append("price")
					else:
						# Esse campo provavelmente nao estara no xml (ou por algum motivo, o cliente nao configurou isso na tela de integracao)
						# mante-lo na lista para que seja inserido, espaco em branco
						# e a ordem dos campos sejam mantida.
						
						list_campos.append(campos_xml)						
			
			result = self.node_item(args['content_pointer'], True)			
			i = 0
			for node_item in result:
				node_item_p = c_char_p(node_item[0])
				arr_dict['id'] =  self.node_id(node_item_p)
				arr_dict['title'] = self.node_title(node_item_p)
				arr_dict['link'] = self.node_link(node_item_p)
				arr_dict['image_link'] = self.node_image_link(node_item_p)				
				arr_dict['google_product_category'] = self.node_google_product_category(node_item_p)
				arr_dict['product_type'] = self.node_product_type(node_item_p)
				arr_dict['price'] = self.node_price(node_item_p)
				arr_dict['sale_price'] = self.node_sale_price(node_item_p)
				arr_dict['description'] = self.node_description(node_item_p)
				arr_dict['condition'] = self.node_condition(node_item_p)
				arr_dict['brand'] = self.node_brand(node_item_p)
				arr_dict['adwords_redirect'] = self.node_adwords_redirect(node_item_p)
				availability = self.node_availability(node_item_p)
				if availability == "in stock":
					availability = 1
				else:
					availability = 0
				arr_dict['availability'] = availability
				arr_dict['gtin'] = self.node_gtin(node_item_p)
				arr_dict['installment'] = self.node_installment(node_item_p)				
				if arr_dict['installment'] != None:
					arr_dict['mounth'] = self.get_installment_month(arr_dict['installment'])
					arr_dict['amount'] = self.get_installment_amount(arr_dict['installment'])				
				for campos_xml in list_campos:
					# Formatacao de preco
					if campos_xml == "price" or campos_xml == "sale_price":
						i = i+1
						# Esse contador eh para que apenas o 'preco' e 'preco_por',
						# sejam formatados. Mandento 'preco_num' e 'preco_por_num', no formato original
						if i <= 2:							
							price_format = "R$ "+arr_dict[campos_xml].replace(".", ",")
							if arr_dict.has_key(campos_xml):
								list_csv.append(price_format)
						else:
							if arr_dict.has_key(campos_xml):
								list_csv.append(arr_dict[campos_xml])
					else:
						# Para que o CSV contenha a mesma, 
						# quantidade de colunas que a tabela de xml
						if arr_dict.has_key(campos_xml):
							list_csv.append(arr_dict[campos_xml])
						else:
							list_csv.append("")
				i = 0
				
				w_csv.csv_handler(nome, list_csv)				
				arr_dict = {}
				list_csv = []
			
			print "arquivo %s.csv gerado com sucesso!"%(nome)
			args = {}
		except Exception, e:
			self.log_msg("ERRO: ParseXml.parse_all_content() "+str(e),"log.txt")
			
	def node_item(self, line_pointer, multiline=False):
		try:
			if multiline == True:
				line_pointer.value = line_pointer.value.replace("</item><","</item>\n<")			
				return self.preg_match_all('(<item>(.*?)<\/item>)',line_pointer.value)
			else:
				result = self.preg_match('<item>',line_pointer.value)			
				if result != None:
					return result.group()
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_item() "+str(e),"log.txt")
			
	def node_id(self, line_pointer, multiline=False):
		try:		
			result = self.preg_match("<g:id><!\[CDATA\[(.*?)\]\]><\/g:id>",line_pointer.value)
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match("<g:id>(.*?)<\/g:id>",line_pointer.value)
				if result != None:
					if result.group(1) != None:
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_id() "+str(e),"log.txt")
			
	def node_link(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<link><!\[CDATA\[(.*?)\]\]><\/link>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<link>(.*?)<\/link>',line_pointer.value)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_link() "+str(e),"log.txt")
	
	def node_title(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<title><!\[CDATA\[(.*?)\]\]><\/title>',line_pointer.value)
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<title>(.*?)<\/title>',line_pointer.value)
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_title() "+str(e),"log.txt")
		
	def node_price(self, line_pointer, multiline=False):
		try:		
			result = self.preg_match('<g:price><!\[CDATA\[(.*?)\]\]><\/g:price>',line_pointer.value)		
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:price>(.*?)<\/g:price>',line_pointer.value)
				if result != None:
					if result.group(1) != None:
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_price() "+str(e),"log.txt")
			
	def node_sale_price(self, line_pointer, multiline=False):
		try:		
			result = self.preg_match('<g:sale_price><!\[CDATA\[(.*?)\]\]><\/g:sale_price>',line_pointer.value)		
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:sale_price>(.*?)<\/g:sale_price>',line_pointer.value)
				if result != None:
					if result.group(1) != None:
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_sale_price() "+str(e),"log.txt")		
	
	def node_image_link(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:image_link><!\[CDATA\[(.*?)\]\]><\/g:image_link>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:image_link>(.*?)<\/g:image_link>',line_pointer.value)
				if result != None:
					if result.group(1) != None:
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_image_link() "+str(e),"log.txt")
	
	def node_google_product_category(self, line_pointer=False):
		try:
			result = self.preg_match('<g:google_product_category><!\[CDATA\[(.*?)\]\]><\/g:google_product_category>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:google_product_category>(.*?)<\/g:google_product_category>',line_pointer.value)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_google_product_category() "+str(e),"log.txt")
		
	def node_product_type(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:product_type><!\[CDATA\[(.*?)\]\]><\/g:product_type>',line_pointer.value)
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:product_type>(.*?)<\/g:product_type>',line_pointer.value)
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_product_type() "+str(e),"log.txt")
		
	def node_description(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<description><!\[CDATA\[(.*?)\]\]><\/description>',line_pointer.value)
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<description>(.*?)<\/description>',line_pointer.value)
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_description() "+str(e),"log.txt")
		
	def node_condition(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:condition><!\[CDATA\[(.*?)\]\]><\/g:condition>',line_pointer.value)
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:condition>(.*?)<\/g:condition>',line_pointer.value)
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_condition() "+str(e),"log.txt")
				
		
	def node_brand(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:brand><!\[CDATA\[(.*?)\]\]><\/g:brand>',line_pointer.value)
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:brand>(.*?)<\/g:brand>',line_pointer.value)
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_brand() "+str(e),"log.txt")
		
	def node_adwords_redirect(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:adwords_redirect><!\[CDATA\[(.*?)\]\]><\/g:adwords_redirect>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:adwords_redirect>(.*?)<\/g:adwords_redirect>',line_pointer.value)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_adwords_redirect() "+str(e),"log.txt")
		
	def node_availability(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:availability><!\[CDATA\[(.*?)\]\]><\/g:availability>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:availability>(.*?)<\/g:availability>',line_pointer.value)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_availability() "+str(e),"log.txt")
		
	def node_gtin(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:gtin><!\[CDATA\[(.*?)\]\]><\/g:gtin>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:gtin>(.*?)<\/g:gtin>',line_pointer.value)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_gtin() "+str(e),"log.txt")
		
	def node_installment(self, line_pointer, multiline=False):
		try:
			result = self.preg_match('<g:installment><!\[CDATA\[(.*?)\]\]><\/g:installment>',line_pointer.value)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:installment>(.*?)<\/g:installment>',line_pointer.value)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.node_installment() "+str(e),"log.txt")
			
	def get_installment_month(self,installment):
		try:
			result = self.preg_match('<g:months><!\[CDATA\[(.*?)\]\]></g:months>',installment)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:months>(.*?)</g:months>',installment)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.get_installment_month() "+str(e),"log.txt")
			
	def get_installment_amount(self,installment):
		try:
			result = self.preg_match('<g:amount><!\[CDATA\[(.*?)\]\]></g:amount>',installment)			
			if result != None:
				if result.group(1) != None:	
					return result.group(1)
			else:
				result = self.preg_match('<g:amount>(.*?)</g:amount>',installment)			
				if result != None:
					if result.group(1) != None:	
						return result.group(1)
		except Exception, e:
			self.log_msg("ERRO: ParseXml.get_installment_amount() "+str(e),"log.txt")
	
	
