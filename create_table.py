import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """

    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host = "localhost",
                                dbname = "job_dashboard",
                                user = "job",
                                password = "dashboard",
                                port = 5432)

    except:
            print("I am unable to connect to the database")
    
    return conn


commands = (
    """
    CREATE TABLE IF NOT EXISTS offre_brute (
        id SERIAL PRIMARY KEY,
        ref VARCHAR(20),
        titre VARCHAR(50),
        entreprise VARCHAR(30),
        ville VARCHAR(40),
        departement VARCHAR(30),
        region VARCHAR(30),
        date_publication VARCHAR(30),
        date_maj VARCHAR(30),
        experience VARCHAR(50),
        salaire VARCHAR(50),
        type_contrat VARCHAR(20),
        intitule VARCHAR(30),
        diplome TEXT,
        secteur TEXT,
        site_origine VARCHAR(20),
        lien_site TEXT,
        corps TEXT
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS intitule (
        id SERIAL PRIMARY KEY,
        nom VARCHAR(30),
        alias VARCHAR(30)
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS secteur (
        id SERIAL PRIMARY KEY,
        libelle VARCHAR(30)
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS region (
        code_reg VARCHAR(3) PRIMARY KEY,
        nom VARCHAR(30)
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS departement (
        code_dep VARCHAR(3) PRIMARY KEY,
        nom VARCHAR(30),
        code_reg VARCHAR(3) REFERENCES region (code_reg)
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS ville (
        code_insee VARCHAR(5) PRIMARY KEY,
        nom VARCHAR(40),
        code_dep VARCHAR(3) REFERENCES departement (code_dep)
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS offre (
        id SERIAL PRIMARY KEY,
        ref VARCHAR(20),
        titre VARCHAR(50),
        entreprise VARCHAR(30),
        ville VARCHAR(5) REFERENCES ville (code_insee),
        departement VARCHAR(3) REFERENCES departement (code_dep),
        region VARCHAR(3) REFERENCES region (code_reg),
        date_publication DATE,
        date_maj DATE,
        exp_min INTEGER,
        exp_max INTEGER,
        salaire_min INTEGER,
        salaire_max INTEGER,
        type_contrat VARCHAR(20),
        intitule INTEGER REFERENCES intitule (id),
        diplome_min VARCHAR(30),
        diplome_max VARCHAR(30),
        site_origine VARCHAR(20),
        lien_site TEXT,
        corps TEXT
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS offre_secteur (
        id_secteur INTEGER REFERENCES secteur (id),
        id_offre INTEGER REFERENCES offre (id),
        CONSTRAINT PK_of_sec PRIMARY KEY (id_secteur, id_offre)
    )
    """
)


def query(conn,requete):
    """ Curseur """
    cur = conn.cursor()
    cur.execute(requete)


if __name__== "__main__":
    with connect() as conn:
        for command in commands:
            query(conn,command)

            conn.commit()
