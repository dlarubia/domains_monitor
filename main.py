# 1- Coletar domínios adquiridos via BHD
# 2- Checar constantemente os status dos domínios
# 3- Atualizar novas informações no banco de dados

from src.Checker import Checker
from src.Database import Database
from src.config.credentials import database as db

db = Database(user=db['user'], password=db['password'], host=db['host'], port=db['port'], db_name=db['name'], sql_script = db['sql_script'])
ch = Checker(database=db, first_time=True)
ch.whois()
ch.insert_domains_in_database()
# ch.export_domains_info_as_csv()

print('done')
pass