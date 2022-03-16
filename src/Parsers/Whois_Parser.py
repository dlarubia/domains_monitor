# Insert here the registrar and the structure returned in 'whois'
def get_godaddy_data(whois_obj):
    data = {
        "domain" : [ 
            whois_obj['domain_name'] if type(whois_obj['domain_name']) == type("str") else whois_obj['domain_name'][0].lower(),
            whois_obj['domain_id'] if 'domain_id' in whois_obj else None,
            whois_obj['name_servers'] if 'name_servers' in whois_obj else None,
            whois_obj['creation_date'] if 'creation_date' in whois_obj else None,
            whois_obj['expiration_date'] if 'expiration_date' in whois_obj else None,
            whois_obj['updated_date'] if 'updated_date' in whois_obj else None,
            whois_obj['status'] if 'status' in whois_obj else None,
        ],
        "registrar" : [
            whois_obj['registrar']  if 'registrar' in whois_obj else None,
            whois_obj['registrar_id'] if 'registrar_id' in whois_obj else None,
            whois_obj['registrar_url'] if 'registrar_url' in whois_obj else None,
            whois_obj['whois_server'] if 'whois_server' in whois_obj else None,
            whois_obj['registrar_email'] if 'registrar_email' in whois_obj else None,
            whois_obj['registrar_phone'] if 'registrar_phone' in whois_obj else None,
            ],
        "registrant" : [ 
            whois_obj['registrant_name'] if 'registrant_name' in whois_obj else None,
            whois_obj['registrant_id'] if 'registrant_id' in whois_obj else None,
            whois_obj['registrant_organization'] if 'registrant_organization' in whois_obj else None,
            whois_obj['registrant_street'] if 'registrant_street' in whois_obj else None,
            whois_obj['registrant_city'] if 'registrant_city' in whois_obj else None,
            whois_obj['registrant_state_province'] if 'registrant_state_province' in whois_obj else None,
            whois_obj['registrant_postal_code'] if 'registrant_postal_code' in whois_obj else None,
            whois_obj['registrant_country'] if 'registrant_country' in whois_obj else None,
            whois_obj['registrant_phone'] if 'registrant_phone' in whois_obj else None,
            whois_obj['registrant_email'] if 'registrant_email' in whois_obj else None,
            whois_obj['registrant_application_purpose'] if 'registrant_application_purpose' in whois_obj else None,
            whois_obj['registrant_nexus_category'] if 'registrant_nexus_category' in whois_obj else None
        ],
        "admin" : [ 
            whois_obj['admin'] if 'admin' in whois_obj else None,
            whois_obj['admin_id'] if 'admin_id' in whois_obj else None,
            whois_obj['admin_organization'] if 'admin_organization' in whois_obj else None,
            whois_obj['admin_street'] if 'admin_street' in whois_obj else None,
            whois_obj['admin_city'] if 'admin_city' in whois_obj else None,
            whois_obj['admin_state_province'] if 'admin_state_province' in whois_obj else None,
            whois_obj['admin_postal_code'] if 'admin_postal_code' in whois_obj else None,
            whois_obj['admin_country'] if 'admin_country' in whois_obj else None,
            whois_obj['admin_phone'] if 'admin_phone' in whois_obj else None,
            whois_obj['admin_email'] if 'admin_email' in whois_obj else None,
            whois_obj['admin_application_purpose'] if 'admin_application_purpose' in whois_obj else None,
            whois_obj['admin_nexus_category'] if 'admin_nexus_category' in whois_obj else None
        ],
        "tech" : [ 
            whois_obj['tech_name'] if 'tech_name' in whois_obj else None,
            whois_obj['tech_id'] if 'tech_id' in whois_obj else None,
            whois_obj['tech_organization'] if 'tech_organization' in whois_obj else None,
            whois_obj['tech_street'] if 'tech_street' in whois_obj else None,
            whois_obj['tech_city'] if 'tech_city' in whois_obj else None,
            whois_obj['tech_state_province'] if 'tech_state_province' in whois_obj else None,
            whois_obj['tech_postal_code'] if 'tech_postal_code' in whois_obj else None,
            whois_obj['tech_country'] if 'tech_country' in whois_obj else None,
            whois_obj['tech_phone'] if 'tech_phone' in whois_obj else None,
            whois_obj['tech_email'] if 'tech_email' in whois_obj else None,
            whois_obj['tech_application_purpose'] if 'tech_application_purpose' in whois_obj else None,
            whois_obj['tech_nexus_category'] if 'tech_nexus_category' in whois_obj else None
        ]
    }
    return data


def get_registroBR_data(whois_obj):
    data = {
        "domain" : [ 
            whois_obj['domain_name'],
            # whois_obj['country'],
            whois_obj['saci'],
            whois_obj['name_server'],
            whois_obj['creation_date'],
            whois_obj['expiration_date'],
            whois_obj['updated_date'],
            whois_obj['status'],
            # whois_obj['nic_hdl_br'],
            # whois_obj['person'], # TODO -> check
            whois_obj['email']
        ],
        'registrant' : [ 
            whois_obj['registrant_name'],
            whois_obj['registrant_id']
        ],

        "admin" : [ 
            whois_obj['owner_c']
            # whois_obj['admin_c'],

        ],

        "tech" : [
            whois_obj['tech_c']
        ]
    }
    return data
    

def get_MarkMonitor_data(whois_obj):
    data = {
        "domain" : [ 
            whois_obj['domain_name'] if 'domain_name' in whois_obj else None,
            whois_obj['name_servers'] if 'name_servers' in whois_obj else None,
            whois_obj['creation_date'] if 'creation_date' in whois_obj else None,
            whois_obj['expiration_date'] if 'expiration_date' in whois_obj else None
        ],
        'registrant' : [ 
            whois_obj['registrant_name'] if 'registrant_name' in whois_obj else None,
            whois_obj['registrant_organization'] if 'registrant_organization' in whois_obj else None
        ],
        'registrar' : [ 
            whois_obj['registrar'] if 'registrar' in whois_obj else None,
            whois_obj['registrar_url'] if 'registrar_url' in whois_obj else None
        ]
    }
    return data


whois_parser = {
    "GoDaddy" : get_godaddy_data,

    "RegistroBR" : get_registroBR_data,

    "MarkMonitor":  get_MarkMonitor_data
}