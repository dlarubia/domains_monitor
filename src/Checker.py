# Realizar whois e checar informações do domínio, adicionando à Database
import whois as who
import json
import src.Database as Database
import pandas as pd

class Checker:
    
    def __init__(self, database = None, domains_txt = 'teste_dom.txt', first_time = False):
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
        pass

    def check_all_domains_and_update_db(self):
        self.whois()
        pass

        
# ch = Checker()
# ch.whois()
# f = open("new", 'w')
# f.write(str(ch.domains))

# # js = json.dumps(ch.domains)
# with open("domains.json", 'w') as json_file:
#     json.dump(ch.domains, json_file, default=str)