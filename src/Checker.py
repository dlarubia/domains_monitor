# Realizar whois e checar informações do domínio, adicionando à Database
from operator import contains
import whois as who
import json
import pandas as pd
import src.queries as queries
from src.Individual_queries import queries as Q
from src.Whois_Parser import parser

class Checker:
    
    def __init__(self, database = None, domains_txt = 'dominios.txt', first_time = False):
        self.domains = {}
        # If is the first insert, is necessary a input with file - then database will be populated
        if not database or first_time:
            #f = open('dominios.txt', 'r')
            if domains_txt:
                f = open(domains_txt, 'r')
            else:
                print("ERROR: Provide a database or txt file with domains to check")
                return

            for line in f:
                if '[' and ']' in line:
                    provider = line.strip().strip('[').strip(']')
                    self.domains[provider] = {}
                    continue
                elif line == "\n":
                    continue
                self.domains[provider][line.strip()] = None
                if database:
                    self.database = database
        else:
            self.database = database
            domain_list = self.database.execute_query(
                "select domains.name, registrar.name from domains INNER JOIN registrar ON registrar_id = registrar.id;")
            for domain, provider in domain_list:
                self.domains[provider][domain] = None
    
    # Get whois information for the domains
    def whois(self):
        for provider in self.domains:
            total = len(self.domains[provider])
            for i, domain in enumerate(self.domains[provider]):
                try:
                    # TODO -> checar se houveram alterações e atualizar o banco de dados, caso tenha ocorrido
                    informations = who.whois(domain)
                    print("WhoIs (" + str(i+1) + "/" + str(total) + ") --> " + domain)
                    # print(informations)
                    self.domains[provider][domain] = informations
                except Exception as e:
                    print(e)
                    self.domains[provider][domain] = "Error - " + str(e)


    def export_domains_info_as_xlsx(self, filename="domains_information.xlsx"):
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        for provider in self.domains:
            df = pd.DataFrame.from_dict(self.domains[provider], orient='index')
            df.to_excel(writer, sheet_name=provider)
        writer.save()


    def export_domains_info_as_csv(self, filename="domains_information.csv"):
        aux_dict = {}
        for provider in self.domains:
            for domain in self.domains[provider]:
                aux_dict[domain] = self.domains[provider][domain]
        df = pd.DataFrame.from_dict(aux_dict, orient='index')
        df.to_csv(filename)


    def insert_domains_in_database(self):
        for provider in self.domains:
            for domain_name in self.domains[provider]:
                try:
                    domain = self.domains[provider][domain_name]
                    parsed_data = parser[provider](domain)
                    if parsed_data['domain'][0] == None:
                        parsed_data['domain'][0] = "UNSUPORTED: " + domain_name
                    # Return id if already inserted
                    registrar_id = self.insert_("registrar", provider, parsed_data)
                    registrant_id = self.insert_("registrant", provider, parsed_data)
                    admin_id = self.insert_("admin", provider, parsed_data)
                    tech_id = self.insert_("tech", provider, parsed_data)
                    print([registrar_id, registrant_id, admin_id, tech_id, domain_name])
                    # Inserting domain
                    self.database.execute_query(Q[provider]['insert_domain'], parsed_data['domain'])
                    # Update Foreign Keys
                    self.database.execute_query(Q['Global']['update_domain_keys'], [registrar_id, registrant_id, admin_id, tech_id, domain_name])

                except Exception as e:
                    if "Error" in domain:
                        invalid_domain = ["INVALID: " + domain_name]
                        self.database.execute_query(Q['Global']['insert_invalid_domain'], invalid_domain)
                    if hasattr(domain, 'text'):
                        if domain.text == "Socket not responding" or "Error trying to connect" in domain.text:
                            invalid_domain = ["ERROR: " + domain_name]
                            self.database.execute_query(Q['Global']['insert_invalid_domain'], invalid_domain)
                    print(e)

    def check_all_domains_and_update_db(self):
        self.whois()
        pass

    
    def insert_(self, item, provider, parsed_data):
        if item in parsed_data:
            if parsed_data[item][0] != None:
                row_id = self.database.execute_query(Q[provider]["insert_"+item], parsed_data[item])
                if row_id == None:
                    name = [parsed_data[item]] if isinstance(parsed_data[item], str) else [parsed_data[item][0]]
                    return self.database.execute_query(Q['Global']["select_"+item+"_id_by_name"], name)[0][0]
        else:
            return None

# ch = Checker()
# ch.whois()
# f = open("new", 'w')
# f.write(str(ch.domains))

# # js = json.dumps(ch.domains)
# with open("domains.json", 'w') as json_file:
#     json.dump(ch.domains, json_file, default=str)