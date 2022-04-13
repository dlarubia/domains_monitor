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
go_daddy_insert_domain = "INSERT INTO domains (name, did, name_servers, creation_date, expiration_date, updated_date, status) VALUES (%s, %s, %s, %s , %s, %s, %s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name, did = EXCLUDED.did, name_servers = EXCLUDED.name_servers, creation_date = EXCLUDED.creation_date, expiration_date = EXCLUDED.expiration_date, updated_date = EXCLUDED.updated_date, status = EXCLUDED.status"

go_daddy_insert_registrar = "INSERT INTO registrars (name, rid, url, whois_url, email, phone) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

go_daddy_insert_registrant = "INSERT INTO registrants (name, rid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

go_daddy_insert_admin = "INSERT INTO admins (name, aid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

go_daddy_insert_tech = "INSERT INTO techs (name, tid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

# ---------- UPDATE ---------- #
go_daddy_update_registrar_id_in_domain = 'UPDATE IN domains (registrar_id, registrant_id, admin_id, tech_id) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING'


# ---------- DELETE ---------- #


########## RegistroBR ##########

# ---------- INSERT ---------- #
registrobr_insert_domain = "INSERT INTO domains (name, saci, name_servers, creation_date, expiration_date, updated_date, status, email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name, saci = EXCLUDED.saci, name_servers = EXCLUDED.name_servers, creation_date = EXCLUDED.creation_date, expiration_date = EXCLUDED.expiration_date, updated_date = EXCLUDED.updated_date, status = EXCLUDED.status, email = EXCLUDED.email"

registrobr_insert_registrant = "INSERT INTO registrants (name, rid) VALUES (%s, %s) ON CONFLICT DO NOTHING"

# I'll put owner into admins
registrobr_insert_admin = "INSERT INTO admins (name) VALUES (%s) ON CONFLICT DO NOTHING"

registrobr_insert_tech = "INSERT INTO techs (name) VALUES (%s) ON CONFLICT DO NOTHING"



########## MarkMonitor ##########

# ---------- INSERT ---------- #
markmonitor_insert_domain = "INSERT INTO domains (name, name_servers, creation_date, expiration_date) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name, name_servers = EXCLUDED.name_servers, creation_date = EXCLUDED.creation_date, expiration_date = EXCLUDED.expiration_date"

markmonitor_insert_registrant = "INSERT INTO registrants (name, organization) VALUES (%s, %s) ON CONFLICT DO NOTHING"

markmonitor_insert_registrar = "INSERT INTO registrars (name, url) VALUES (%s, %s) ON CONFLICT DO NOTHING"



########## Global Queries ##########
update_domain_keys = "UPDATE domains SET provider_id = %s, registrar_id = %s, registrant_id = %s, admin_id = %s, tech_id = %s WHERE name = %s"

insert_provider = "INSERT INTO providers (name) VALUES (%s) ON CONFLICT DO NOTHING"

insert_invalid_domain = "INSERT INTO domains (name, provider_id) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name, provider_id = EXCLUDED.provider_id"

select_provider_id_by_name = "SELECT id FROM providers WHERE name = (%s)"

select_registrar_id_by_name = "SELECT id FROM registrars WHERE name = (%s)"

select_registrant_id_by_name = "SELECT id FROM registrants WHERE name = %s"

select_admin_id_by_name = "SELECT id FROM admins WHERE name = %s"

select_tech_id_by_name = "SELECT id FROM techs WHERE name = %s"

select_domains_with_provider = "select domains.name, providers.name from domains inner join providers on providers.id = domains.provider_id"

remove_domain = "DELETE FROM domains WHERE name LIKE '%%s'"

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
        "insert_provider" : insert_provider,
        "insert_invalid_domain" : insert_invalid_domain,
        "select_provider_id_by_name" : select_provider_id_by_name,
        "select_registrar_id_by_name" : select_registrar_id_by_name,
        "select_registrant_id_by_name" : select_registrant_id_by_name,
        "select_admin_id_by_name" : select_admin_id_by_name,
        "select_tech_id_by_name" : select_tech_id_by_name,
        "select_domains_with_provider" : select_domains_with_provider,
        "remove_domain" : remove_domain
    }
}