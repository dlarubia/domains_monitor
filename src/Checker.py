# Realizar whois e checar informações do domínio, adicionando à Database
from operator import contains
import whois as who
import pandas as pd
from os import listdir
from os.path import isfile, join
import re
from src.Parsers.Individual_queries import queries as Q
from src.Parsers.Parser import Parser
from src.Database import Database


class Checker:

    def __init__(self, database : Database = None, first_time = False, domains_folder = 'domains'):
        self.domains = {}
        # If is the first insert, is necessary a input with file - then database will be populated
        if not database or first_time:
            #f = open('dominios.txt', 'r')
            if domains_folder:
                filenames = [f for f in listdir(domains_folder) if isfile(join(domains_folder, f))]
                files = []
                for file in filenames:
                    files.append(open(domains_folder + '/' + file, 'r'))
            else:
                print("ERROR: Provide a database or txt file with domains to check")
                return

            for f in files:
                provider = re.sub('\/.*\/', '', re.sub('\.[a-z]*', '', f.name)) # Clean provider name
                self.domains[provider] = {}
                for line in f:
                    if line == "\n":
                        continue
                    self.domains[provider][line.strip()] = None   # Defining domain in dict of providers
            if database:  # If its the first time and there is a database to perform actions
                self.database = database

        else:
            self.database = database
            domain_list = self.database.execute_query(Q['Global']['select_domains_with_provider'])
            for domain, provider in domain_list:
                self.domains[provider][domain] = None

    
    # Get whois information for the domains
    def whois(self):
        for provider in self.domains:
            total = len(self.domains[provider])
            for i, domain in enumerate(self.domains[provider]):
                try:
                    # TODO -> checar se houveram alterações e atualizar o banco de dados, caso tenha ocorrido
                    print("WhoIs (" + str(i+1) + "/" + str(total) + ") --> " + domain)
                    informations = who.whois(domain)
                    # print(informations)
                    self.domains[provider][domain] = informations
                except Exception as e:
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
            # Insert provider em database and get id
            self.database.execute_query(Q['Global']['insert_provider'], [provider])
            provider_id = self.database.execute_query(Q['Global']['select_provider_id_by_name'], [provider])[0][0]
            for domain_name in self.domains[provider]:
                try:
                    domain = self.domains[provider][domain_name]
                    #parsed_data = parser[provider](domain)
                    if isinstance(domain, str):
                        raise Exception("Error with domain '" + domain_name + "'")
                    parsed_data = Parser(provider, domain).get_structured_data()
                    # parsed_data = parsed_data.get_structured_data()
                    if parsed_data['domain'][0] == None:
                        parsed_data['domain'][0] = "UNSUPORTED: " + domain_name
                    # Return id if already inserted
                    registrar_id = self.insert_("registrar", provider, parsed_data)
                    registrant_id = self.insert_("registrant", provider, parsed_data)
                    admin_id = self.insert_("admin", provider, parsed_data)
                    tech_id = self.insert_("tech", provider, parsed_data)
                    # print([registrar_id, registrant_id, admin_id, tech_id, domain_name])
                    # Inserting domain
                    self.database.execute_query(Q[provider]['insert_domain'], parsed_data['domain'])
                    # Update Foreign Keys
                    self.database.execute_query(Q['Global']['update_domain_keys'], [provider_id, registrar_id, registrant_id, admin_id, tech_id, parsed_data['domain'][0]])

                except Exception as e:
                    if "Error" in domain:
                        invalid_domain = "UNSUPORTED: " + domain_name
                        self.database.execute_query(Q['Global']['insert_invalid_domain'], [invalid_domain, provider_id])
                    elif hasattr(domain, 'text'):
                        if domain.text == "Socket not responding" or "Error trying to connect" in domain.text:
                            error_domain = ["ERROR: " + domain_name]
                            self.database.execute_query(Q['Global']['insert_invalid_domain'], [error_domain, provider_id])
                    print('Exception: ' + str(e) + ' (' + domain_name + ')')

    # This code is awful :'(
    def check_all_domains_and_update_db(self, domains_folder):
        # Select domains from database and compare with domains list
        domains_in_db = self.database.execute_query(Q['Global']['select_domains_with_provider'])
        all_domains_in_db = []
        if domains_in_db:
            for i in range(len(domains_in_db)):
                domains_in_db[i] = list(domains_in_db[i])
                domains_in_db[i][0] = re.sub('[^:]*: ', '', domains_in_db[i][0])
                all_domains_in_db.append(domains_in_db[i][0])
        else:
            # Change 'domains_in_db' type to a void list instead NoneType
            domains_in_db = []
        # Domains to be removed of database
        all_domains = []
        for provider in self.domains:
            for domain_name in self.domains[provider]:
                all_domains.append(domain_name)
        
        domains_removed_from_txt_that_are_in_db = list(set(all_domains_in_db) - set(all_domains))
        print("Diff: " + str(domains_removed_from_txt_that_are_in_db))


        # Add new domains in txt to database
        for provider in self.domains:
            self.database.execute_query(Q['Global']['insert_provider'], [provider])
            provider_id = self.database.execute_query(Q['Global']['select_provider_id_by_name'], [provider])[0][0]
            for domain_name in self.domains[provider]:
                # Check for new domain
                if (domain_name,provider) not in domains_in_db:
                    # ADD DOMAIN TO DB
                    self.add_domain_in_database(domain_name,provider)

        # Remove domains 
        # for domain in domains_removed_from_txt_that_are_in_db:
        #     print("Removing '" + domain + "' from the database")
        #     self.database.execute_query(Q['Global']['remove_domain'], [domain])
        #     print("wait")




    def insert_(self, item, provider, parsed_data):
        if item in parsed_data:
            if parsed_data[item][0] != None:
                row_id = self.database.execute_query(Q[provider]["insert_"+item], parsed_data[item])
                if row_id == None:
                    name = [parsed_data[item]] if isinstance(parsed_data[item], str) else [parsed_data[item][0]]
                    return self.database.execute_query(Q['Global']["select_"+item+"_id_by_name"], name)[0][0]
        else:
            return None

    # Insert/update domain info in database
    def add_domain_in_database(self, domain_name, provider):
        self.database.execute_query(Q['Global']['insert_provider'], [provider])
        provider_id = self.database.execute_query(Q['Global']['select_provider_id_by_name'], [provider])[0][0]
        try:
            domain = who.whois(domain_name)
        except Exception as e:
            domain = "Error - " + str(e)

        print("Updating domain: " + domain_name)
        
        try:
            if isinstance(domain, str):
                raise Exception("Error with domain '" + domain_name + "'")
            parsed_data = Parser(provider, domain).get_structured_data()
            # parsed_data = parsed_data.get_structured_data()
            if parsed_data['domain'][0] == None:
                parsed_data['domain'][0] = "UNSUPORTED: " + domain_name
            # Return id if already inserted
            registrar_id = self.insert_("registrar", provider, parsed_data)
            registrant_id = self.insert_("registrant", provider, parsed_data)
            admin_id = self.insert_("admin", provider, parsed_data)
            tech_id = self.insert_("tech", provider, parsed_data)
            # print([registrar_id, registrant_id, admin_id, tech_id, domain_name])
            # Inserting domain
            self.database.execute_query(Q[provider]['insert_domain'], parsed_data['domain'])
            # Update Foreign Keys
            self.database.execute_query(Q['Global']['update_domain_keys'], [provider_id, registrar_id, registrant_id, admin_id, tech_id, parsed_data['domain'][0]])

        except Exception as e:
            if "Error" in domain:
                invalid_domain = "UNSUPORTED: " + domain_name
                self.database.execute_query(Q['Global']['insert_invalid_domain'], [invalid_domain, provider_id])
            elif hasattr(domain, 'text'):
                if domain.text == "Socket not responding" or "Error trying to connect" in domain.text:
                    error_domain = ["ERROR: " + domain_name]
                    self.database.execute_query(Q['Global']['insert_invalid_domain'], [error_domain, provider_id])
            print('Exception: ' + str(e) + ' (' + domain_name + ')')