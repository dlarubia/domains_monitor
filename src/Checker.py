# Realizar whois e checar informações do domínio, adicionando à Database
import whois as who
import json
import pandas as pd
import src.queries as queries


class Checker:
    # domains_all_fields = {
    #     'domain_name' : None,
    #     'registrar' : None,
    #     'whois_server' : None,
    #     'updated_date' : None,
    #     'creation_date' : None,
    #     'expiration_date' : None,
    #     'name_servers' : None,
    #     'status' : None,
    #     'emails' : None,
    #     'saci' : None,
    #     'org' : None,
    #     'address' : None,
    #     'city' : None,
    #     'state' : None,
    #     'zipcode' : None,
        
    # }
    
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
        try:
            for provider in self.domains:
                for domain_name in self.domains[provider]:
                    domain = self.domains[provider][domain_name]
                    registrar_id = self.database.execute_query(queries.select_registrar_id_where_name_equals_to, [domain['registrar']]) if 'registrar' in domain else None
                    registrant_id = self.database.execute_query(queries.select_registrant_id_where_name_equals_to, [domain['registrant']]) if 'registrant' in domain else None
                    admin_id = self.database.execute_query(queries.select_admin_id_where_name_equals_to, [domain['admin']]) if 'admin' in domain else None
                    tech_id = self.database.execute_query(queries.select_tech_id_where_name_equals_to, [domain['tech']]) if 'tech' in domain else None
                    parsed_data = [
                        domain_name,
                        registrar_id,
                        registrant_id,
                        admin_id,
                        tech_id,
                        domain['saci'] if 'saci' in domain else None,
                        domain['name_servers'] if 'name_servers' in domain else None,
                        domain['creation_date'] if 'creation_date' in domain else None,
                        domain['expiration_date'] if 'expiration_date' in domain else None,
                        domain['updated_date'] if 'updated_date' in domain else None
                    ]
                    print("Executando query")
                    self.database.execute_query(queries.insert_domain, parsed_data)
        except Exception as e:
            print(e)


    def insert_registrar(self):
        pass

    def insert_registrant(self):
        pass
    
    def insert_admin(self):
        pass

    def insert_tech(self):
        pass

    def insert_domain(self):
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