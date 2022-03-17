import re
import datetime
from src.Parsers.Whois_Parser import whois_parser

class Parser:
    class MarkMonitor:
        def __init__(self, domain_obj):
            self.data = domain_obj
            self.filter_data()

        def filter_data(self):
            # Domain
            if hasattr(self.data, 'domain_name'):
                if self.data['domain_name'] is not None:
                    self.data['domain_name'] = re.search('(([A-Za-z]|[0-9])*(\.[A-Za-z]+)+)', str(self.data['domain_name']))[0].lower()
            self.data['name_servers'] = re.sub("{|}", '', str(self.data['name_servers'])).lower() if 'name_servers' in self.data else None
            self.data['creation_date'] = Parser.if_it_is_list_return_first_element(self.data, 'creation_date')
            if self.data['creation_date'] is not None:
                self.data['creation_date'] = self.data['creation_date'].date()
            
            self.data['expiration_date'] = Parser.if_it_is_list_return_first_element(self.data, 'expiration_date')
            if self.data['expiration_date'] is not None:
                self.data['expiration_date'] = self.data['expiration_date'].date()
        
    class RegistroBR:
        def __init__(self, domain_obj):
            self.data = domain_obj
            self.filter_data()

        def filter_data(self):
            # Domain
            if hasattr(self.data, 'domain_name'):
                if self.data['domain_name'] is not None:
                    self.data['domain_name'] = re.search('([A-Za-z]*(\.[A-Za-z]+)+)', str(self.data['domain_name']))[0].lower()
            self.data['name_server'] = re.sub("{|}", '', str(self.data['name_server'])).lower() if 'name_server' in self.data else None
            self.data['creation_date'] = Parser.if_it_is_list_return_first_element(self.data, 'creation_date')
            if self.data['creation_date'] is not None:
                self.data['creation_date'] = self.data['creation_date'].date()
            
            self.data['expiration_date'] = Parser.if_it_is_list_return_first_element(self.data, 'expiration_date')
            if self.data['expiration_date'] is not None:
                self.data['expiration_date'] = self.data['expiration_date'].date()
            
            self.data['updated_date'] = Parser.if_it_is_list_return_first_element(self.data, 'updated_date')
            if self.data['updated_date'] is not None:
                self.data['updated_date'] = self.data['updated_date'].date()
        
    class GoDaddy:
        def __init__(self, domain_obj):
            self.data = domain_obj
            self.filter_data()

        def filter_data(self):
            # Domain
            if hasattr(self.data, 'domain_name'):
                if self.data['domain_name'] is not None:
                    self.data['domain_name'] = re.search('([A-Za-z]*(\.[A-Za-z]+)+)', str(self.data['domain_name']))[0].lower()
            
            self.data['name_servers'] = re.sub("{|}", '', str(self.data['name_servers'])).lower() if 'name_servers' in self.data else None
            
            self.data['creation_date'] = Parser.if_it_is_list_return_first_element(self.data, 'creation_date')
            if self.data['creation_date'] is not None:
                self.data['creation_date'] = self.data['creation_date'].date()
            
            self.data['expiration_date'] = Parser.if_it_is_list_return_first_element(self.data, 'expiration_date')
            if self.data['expiration_date'] is not None:
                self.data['expiration_date'] = self.data['expiration_date'].date()
            
            self.data['updated_date'] = Parser.if_it_is_list_return_first_element(self.data, 'updated_date')
            if self.data['updated_date'] is not None:
                self.data['updated_date'] = self.data['updated_date'].date()
                

    registrars = {
        'MarkMonitor' : MarkMonitor,
        'RegistroBR' : RegistroBR,
        'GoDaddy' : GoDaddy
    }

    def __init__(self, registrar, domain_obj):
        self.domain = self.registrars[registrar](domain_obj)
        self.registrar = registrar
    
    def get_structured_data(self):
        return whois_parser[self.registrar](self.domain.data)

    def if_it_is_list_return_first_element(object, attribute):
        if hasattr(object, attribute):
                if isinstance(object[attribute], list):
                    return object[attribute][0]
                return object[attribute]
        else:
            return None
