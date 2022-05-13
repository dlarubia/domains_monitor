from genericpath import isfile
from os.path import join
from os import listdir
import re


class Menu_Options:
    def __init__(self, domains_folder = 'domains'):
        self.options = [
            "Insert new domain",
            "Remove domain",
            "Update domains information",
            "Export csv of invalids and unsuported domains",
            "Exit" # needs to be the last one
        ]
        self.domains_folder = domains_folder

def insert_new_domain(self):
    
    pass

def remove_domain(domain_name):
    pass

def update_domains_info():
    pass

def export_csv_of_invalids_and_unsuported_domains(filename='invalid.csv'):
    pass
