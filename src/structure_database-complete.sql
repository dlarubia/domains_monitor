CREATE TABLE IF NOT EXISTS registrars (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
--  rid VARCHAR(100),
    url VARCHAR(255),
    whois_url VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS registrants (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(255),
    rid VARCHAR(100), -- CPF ou CPNJ ou Código estrangeiro
    organization VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(255),
    state_province VARCHAR(255),
    postal_code VARCHAR(50),
    country VARCHAR(20),
    phone VARCHAR(255),
    email VARCHAR(255),
    application_purpose VARCHAR(255),
    nexus_category VARCHAR(255)
    );
    
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(255),
    rid VARCHAR(100), -- CPF ou CPNJ ou Código estrangeiro
    organization VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(255),
    state_province VARCHAR(255),
    postal_code VARCHAR(50),
    country VARCHAR(20),
    phone VARCHAR(255),
    email VARCHAR(255),
    application_purpose VARCHAR(255),
    nexus_category VARCHAR(255),
    created VARCHAR(100),
    changed VARCHAR(100)
    );

    
CREATE TABLE IF NOT EXISTS techs (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(255),
    rid VARCHAR(100), -- CPF ou CPNJ ou Código estrangeiro
    organization VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(255),
    state_province VARCHAR(255),
    postal_code VARCHAR(50),
    country VARCHAR(20),
    phone VARCHAR(255),
    email VARCHAR(255),
    application_purpose VARCHAR(255),
    nexus_category VARCHAR(255),
    created VARCHAR(100),
    changed VARCHAR(100)
    );
   
        
CREATE TABLE IF NOT EXISTS domains (
    id SERIAL,
    name VARCHAR(255) PRIMARY KEY,
    
    registrar_id INT,
        FOREIGN KEY (registrar_id)
            REFERENCES registrars(id),
    registrant_id INT,
        FOREIGN KEY (registrant_id)
            REFERENCES registrants(id),
    admin_id INT,
        FOREIGN KEY (admin_id)
            REFERENCES admins(id),
    tech_id INT,
        FOREIGN KEY (tech_id)
            REFERENCES techs(id),
    
    saci BOOLEAN,
    name_servers TEXT,
    creation_date VARCHAR(255),
    expiration_date VARCHAR(255),
    updated_date TEXT --changed
    status TEXT
);


CREATE TABLE IF NOT EXISTS domains_history (
    id SERIAL PRIMARY KEY,
    change_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
    operation VARCHAR(20),

    name VARCHAR(255),
    
    registrar_id INT,
        FOREIGN KEY (registrar_id)
            REFERENCES registrars(id),
    registrant_id INT,
        FOREIGN KEY (registrant_id)
            REFERENCES registrants(id),
    admin_id INT,
        FOREIGN KEY (admin_id)
            REFERENCES admins(id),
    tech_id INT,
        FOREIGN KEY (tech_id)
            REFERENCES techs(id),
    
    saci BOOLEAN,
    name_servers TEXT,
    creation_date VARCHAR(255),
    expiration_date VARCHAR(255),
    updated_date TEXT --changed
);

CREATE OR REPLACE FUNCTION copy_domain_info() RETURNS trigger AS 
    $$
        BEGIN
            INSERT INTO domains_history
                (operation, id, name, registrar_id, registrant_id, admin_id, tech_id, saci,
                name_servers, creation_date, expiration_date, updated_date)
            VALUES
                ('UPDATE', OLD.id, OLD.name, OLD.registrar_id, OLD.registrant_id, OLD.admin_id, OLD.tech_id, OLD.saci,
                OLD.name_servers, OLD.creation_date, OLD.expiration_date, OLD.updated_date);
            RETURN OLD;
        END;
    $$
    LANGUAGE plpgsql;

CREATE TRIGGER trigger_domains_history AFTER UPDATE ON domains
    FOR EACH ROW
    EXECUTE PROCEDURE copy_domain_info();