'''
GLOBAL FIELDS
1- table 'domains': (name, registrar_id, registrant_id, admin_id, tech_id, saci, name_servers, creation_date, expiration_date, updated_date, status)
2- table 'registrars': (name, id, url, whois_url, email, phone)
3- table 'registrants': (name, id, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category)
4- table 'admins': (name, id, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category)
5- table 'techs': (name, id, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category)


'''
########## GoDaddy ##########

# ---------- INSERT ---------- #
go_daddy_insert_domain = "INSERT INTO domains (name, did, name_servers, creation_date, expiration_date, updated_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"

go_daddy_insert_registrar = "INSERT INTO registrars (name, rid, url, whois_url, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"

go_daddy_insert_registrant = "INSERT INTO registrants (name, rid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

go_daddy_insert_admin = "INSERT INTO admins (name, aid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

go_daddy_insert_tech = "INSERT INTO techs (name, tid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# ---------- UPDATE ---------- #
go_daddy_update_registrar_id_in_domain = 'UPDATE IN domains (registrar_id, registrant_id, admin_id, tech_id) VALUES (%s, %s, %s, %s)'


# ---------- DELETE ---------- #


########## RegistroBR ##########

# ---------- INSERT ---------- #
registrobr_insert_domain = "INSERT INTO domains (name, saci, name_servers, creation_date, expiration_date, updated_date, status, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

registrobr_insert_registrant = "INSERT INTO registrants (name, rid) VALUES (%s, %s)"

# I'll put owner into admins
registrobr_insert_admin = "INSERT INTO admins (name) VALUES (%s)"

registrobr_insert_tech = "INSERT INTO techs (name) VALUES (%s)"



########## MarkMonitor ##########

# ---------- INSERT ---------- #
markmonitor_insert_domain = "INSERT INTO domains (name, name_servers, creation_date, expiration_date) VALUES (%s, %s, %s, %s)"

markmonitor_insert_registrant = "INSERT INTO registrants (name, organization) VALUES (%s, %s) ON CONFLICT DO NOTHING"

markmonitor_insert_registrar = "INSERT INTO registrars (name, url) VALUES (%s, %s) ON CONFLICT DO NOTHING"



########## Global Queries ##########
update_domain_keys = "UPDATE domains SET registrar_id = %s, registrant_id = %s, admin_id = %s, tech_id = %s WHERE name = %s"

insert_invalid_domain = "INSERT INTO domains (name) VALUES (%s)"

select_registrar_id_by_name = "SELECT id FROM registrars WHERE name = %s"

select_registrant_id_by_name = "SELECT id FROM registrants WHERE name = %s"

select_admin_id_by_name = "SELECT id FROM admins WHERE name = %s"

select_tech_id_by_name = "SELECT id FROM techs WHERE name = %s"


## -------- GLOBAL DICTIONARY -------- #
# TODO -> Review registrars names
queries = {
    "GoDaddy" : {
        "insert_domain" : go_daddy_insert_domain,
        "insert_registrar" : go_daddy_insert_registrar,
        "insert_registrant" : go_daddy_insert_registrant,
        "insert_admin" : go_daddy_insert_admin,
        "insert_tech" : go_daddy_insert_tech
    },

    "RegistroBR" : {
        "insert_domain" : registrobr_insert_domain,
        "insert_registrant" : registrobr_insert_registrant,
        "insert_admin" : registrobr_insert_admin,
        "insert_tech" : registrobr_insert_tech
    },

    "MarkMonitor" : {
        "insert_domain" : markmonitor_insert_domain,
        "insert_registrar" : markmonitor_insert_registrar,
        "insert_registrant" : markmonitor_insert_registrant
    },

    "Global" : {
        "update_domain_keys" : update_domain_keys,
        "insert_invalid_domain" : insert_invalid_domain,
        "select_registrar_id_by_name" : select_registrar_id_by_name,
        "select_registrant_id_by_name" : select_registrant_id_by_name,
        "select_admin_id_by_name" : select_admin_id_by_name,
        "select_tech_id_by_name" : select_tech_id_by_name
    }
}