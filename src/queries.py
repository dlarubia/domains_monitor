# ---------- INSERT ---------- #

insert_domain = "INSERT INTO domains (name, registrar_id, registrant_id, admin_c, tech_c, owner_c, billing_c, nic_hdl_br, saci, name_servers, creation_date, expiration_date, updated_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

insert_admin = "INSERT INTO admins (name, rid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category, created, changed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

insert_registrant = "INSERT INTO registrants (name, rid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

insert_registrar = "INSERT INTO registrars (name, url, whois_url, email, phone) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"

insert_tech = "INSERT INTO techs (name, rid, organization, street, city, state_province, postal_code, country, phone, email, application_purpose, nexus_category, created, changed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


# ---------- SELECT ---------- #
select_all_domains = "SELECT * FROM domains"

select_domain_where_name_equals_to = "SELECT * FROM domains WHERE name = %s"

select_registrar_id_where_name_equals_to = "SELECT id FROM registrars WHERE name = %s"

select_registrant_id_where_name_equals_to = "SELECT id FROM registrants WHERE name = %s"

select_admin_id_where_name_equals_to = "SELECT id FROM admins WHERE name = %s"

select_tech_id_where_name_equals_to = "SELECT id FROM tech WHERE name = %s"