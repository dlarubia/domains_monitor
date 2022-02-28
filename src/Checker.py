# Realizar whois e checar informações do domínio, adicionando à Database
import whois as who
import json

class Checker:
    domains = {}
    #f = open('dominios.txt', 'r')
    f = open('teste_dom.txt', 'r')
    for line in f:
        if '[' and ']' in line:
            provider = line.strip().strip('[').strip(']')
            domains[provider] = {}
            continue
        elif line == "\n":
            continue
        domains[provider][line.strip()] = None
    
    def __init__(self, database=None):
        self.database = database
    
    def whois(self, domain=None):
        if not domain:
            for provider in self.domains:
                total = len(self.domains[provider])
                for i, domain in enumerate(self.domains[provider]):
                    try:
                        informations = who.whois(domain)
                        print("WhoIs (" + str(i+1) + "/" + str(total) + ") --> " + domain)
                        # print(informations)
                        self.domains[provider][domain] = informations
                    except Exception as e:
                        print(e)
                        self.domains[provider][domain] = "Error - " + str(e)

ch = Checker()
ch.whois()
f = open("new", 'w')
f.write(str(ch.domains))

# js = json.dumps(ch.domains)
with open("domains.json", 'w') as json_file:
    json.dump(ch.domains, json_file, default=str)