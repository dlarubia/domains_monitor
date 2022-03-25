import re
import datetime
from src.Parsers.Whois_Parser import whois_parser

class Parser:
    class MarkMonitor:
        def __init__(self, domain_obj):
            self.data = domain_obj
            self.filter_data()

        def filter_data(self):
            # If the data is not a dict, return the data because strings are immutable (will promp an error)
            if isinstance(self.data, str):
                return self.data
            # Domain
            if self.key_in_dict('domain_name'):
                self.filter_if_value_not_none('domain_name','(([A-Za-z]|[0-9]|[-])*(\.[A-Za-z]+)+)', 'search')
            # if hasattr(self.data, 'domain_name'):
            #     if self.data['domain_name'] is not None:
            #         self.data['domain_name'] = re.search('(([A-Za-z]|[0-9])*(\.[A-Za-z]+)+)', str(self.data['domain_name']))[0].lower()
            
            if self.key_in_dict('name_servers'):
                self.filter_if_value_not_none('name_servers', '{|}', 'sub')
            # if hasattr(self.data, 'name_servers'):
                # self.data['name_servers'] = re.sub("{|}", '', str(self.data['name_servers'])).lower() if 'name_servers' in self.data else None
            
            # if 'creation_date' in self.data:
            if self.key_in_dict('creation_date'):
                self.if_it_is_list_set_first_element('creation_date')
                self.convert_datetime_to_date_if_not_none('creation_date')
                # if self.data['creation_date'] is not None:
                #     self.data['creation_date'] = self.data['creation_date'].date()
            
            if self.key_in_dict('expiration_date'):
                self.if_it_is_list_set_first_element('expiration_date')
                self.convert_datetime_to_date_if_not_none('expiration_date')
                # if self.data['expiration_date'] is not None:
                #     self.data['expiration_date'] = self.data['expiration_date'].date()
        
        
        def key_in_dict(self, key):
            return True if key in self.data else False

        # Method = re.SEARCH or re.SUB
        def filter_if_value_not_none(self, key, regex, method):
            if method != 'sub' and method != 'search':
                raise Exception("Invalid 'method' in filter_value_if_not_none(). Only 'sub' or 'search' are valid.")
            if self.data[key] is not None:
                if method == 'sub':
                    self.data[key] = re.sub(regex, '', str(self.data[key])).lower()
                elif method == 'search':
                    self.data[key] = re.search(regex, str(self.data[key]))[0].lower()
        
        def convert_datetime_to_date_if_not_none(self, key):
            if self.data[key] is not None:
                self.data[key] = self.data[key].date()
        
        def if_it_is_list_set_first_element(self, key):
            if isinstance(self.data[key], list):
                self.data[key] = self.data[key][0]


    class RegistroBR:
        def __init__(self, domain_obj):
            self.data = domain_obj
            self.filter_data()

        def filter_data(self):
            # If the data is not a dict, return the data because strings are immutable (will promp an error)
            if isinstance(self.data, str):
                return self.data
            # Domain
            if hasattr(self.data, 'domain_name'):
                if self.data['domain_name'] is not None:
                    self.data['domain_name'] = re.search('(([A-Za-z]|[0-9]|[-])*(\.[A-Za-z]+)+)', str(self.data['domain_name']))[0].lower()
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
            # If the data is not a dict, return the data because strings are immutable (will promp an error)
            if isinstance(self.data, str):
                return self.data
            # Domain
            if hasattr(self.data, 'domain_name'):
                if self.data['domain_name'] is not None:
                    self.data['domain_name'] = re.search('(([A-Za-z]|[0-9]|[-])*(\.[A-Za-z]+)+)', str(self.data['domain_name']))[0].lower()
            
            if hasattr(self.data, 'name_servers'):
                self.data['name_servers'] = re.sub("{|}", '', str(self.data['name_servers'])).lower() if 'name_servers' in self.data else None
            
            if hasattr(self.data, 'creation_date'):
                self.data['creation_date'] = Parser.if_it_is_list_return_first_element(self.data, 'creation_date')
                if self.data['creation_date'] is not None:
                    self.data['creation_date'] = self.data['creation_date'].date()
            
            if hasattr(self.data, 'expiration_date'):
                self.data['expiration_date'] = Parser.if_it_is_list_return_first_element(self.data, 'expiration_date')
                if self.data['expiration_date'] is not None:
                    self.data['expiration_date'] = self.data['expiration_date'].date()
            
            if hasattr(self.data, 'updated_date'):
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