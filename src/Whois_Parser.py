# Insert here the registrar and the structure returned in 'whois'
def get_godaddy_data(whois_obj):
    data = {
        "domain" : [ 
            whois_obj['domain_name'][0].lower(),
            whois_obj['domain_id'],
            whois_obj['whois_server'],
            whois_obj['name_servers'],
            whois_obj['creation_date'],
            whois_obj['expiration_date'],
            whois_obj['updated_date'],
            whois_obj['status'],
        ],
        "registrar" : [
            whois_obj['registrar'],
            whois_obj['registrar_id'],
            whois_obj['registrar_url'],
            whois_obj['registrar_email'],
            whois_obj['registrar_phone'],],
        "registrant" : [ 
            whois_obj['registrant_id'],
            whois_obj['registrant_name'],
            whois_obj['registrant_organization'],
            whois_obj['registrant_street'],
            whois_obj['registrant_city'],
            whois_obj['registrant_state_province'],
            whois_obj['registrant_postal_code'],
            whois_obj['registrant_country'],
            whois_obj['registrant_phone'],
            whois_obj['registrant_email'],
            whois_obj['registrant_application_purpose'],
            whois_obj['registrant_nexus_category'],
        ],
        "admin" : [ 
            whois_obj['admin_id'],
            whois_obj['admin'],
            whois_obj['admin_organization'],
            whois_obj['admin_street'],
            whois_obj['admin_city'],
            whois_obj['admin_state_province'],
            whois_obj['admin_postal_code'],
            whois_obj['admin_country'],
            whois_obj['admin_phone'],
            whois_obj['admin_email'],
            whois_obj['admin_application_purpose'],
            whois_obj['admin_nexus_category'],
        ],
        "tech" : [ 
            whois_obj['tech_id'],
            whois_obj['tech_name'],
            whois_obj['tech_organization'],
            whois_obj['tech_street'],
            whois_obj['tech_city'],
            whois_obj['tech_state_province'],
            whois_obj['tech_postal_code'],
            whois_obj['tech_country'],
            whois_obj['tech_phone'],
            whois_obj['tech_email'],
            whois_obj['tech_application_purpose'],
        ]
    }
    return data


def get_registroBR_data(whois_obj):
    data = {
        "domain" : [ 
            whois_obj['domain'],
            whois_obj['country'],
            whois_obj['owner_c'],
            whois_obj['admin_c'],
            whois_obj['tech_c'],
            whois_obj['billing_c'],
            whois_obj['name_server'],
            whois_obj['saci'],
            whois_obj['creation_date'],
            whois_obj['updated_date'],
            whois_obj['expiration_date'],
            whois_obj['status'],
            whois_obj['nic_hdl_br'],
            whois_obj['person'], # TODO -> check
            whois_obj['email'],
        ],
        'registrant' : [ 
            whois_obj['registrant_name'],
            whois_obj['registrant_id'],
        ]
    }
    return data
    

def get_MarkMonitor_data(whois_obj):
    data = {
        "domain" : [ 
            whois_obj['domain'],
            whois_obj['creation_date'],
            whois_obj['expiration_date'],
            whois_obj['name_servers'],
        ],
        'registrant' : [ 
            whois_obj['registrant_name'],
            whois_obj['registrant_organization'],
        ],
        'registrar' : [ 
            whois_obj['registrar'],
            whois_obj['registrar_url'],
        ]
    }
    return data




registrars = {
    "GoDaddy" : get_godaddy_data,

    "RegistroBR" : get_registroBR_data,

    "MarkMonitor":  get_MarkMonitor_data
}