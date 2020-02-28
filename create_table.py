import psycopg2
import csv
import pandas as pd
import meteojob as mj
import traceback

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
    DROP TABLE offre_intitule CASCADE;
    """
    ,
    """
    DROP TABLE offre_secteur CASCADE;
    """
    ,
    """
    DROP TABLE intitule CASCADE;
    """
    ,
    """
    DROP TABLE secteur CASCADE;
    """
    ,
    """
    DROP TABLE ville CASCADE;
    """
    ,
    """
    DROP TABLE departement CASCADE;
    """
    ,
    """
    DROP TABLE region CASCADE;
    """
    ,
    """
    DROP TABLE offre CASCADE;
    """
    ,

    """
    CREATE TABLE IF NOT EXISTS offre_brute (
        id SERIAL PRIMARY KEY,
        ref VARCHAR(20),
        titre VARCHAR(100),
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
<<<<<<< HEAD
        nom VARCHAR(50),
        alias VARCHAR(50)
=======
        nom VARCHAR(30),
        alias VARCHAR(75)
>>>>>>> initialisation de la base
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
        nom VARCHAR(50),
        code_dep VARCHAR(3) REFERENCES departement (code_dep),
        latitude float,
        longitude float
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS offre (
        id SERIAL PRIMARY KEY,
        ref VARCHAR(20),
        titre VARCHAR(100),
        entreprise VARCHAR(50),
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
    CREATE TABLE IF NOT EXISTS offre_intitule (
        id_offre integer REFERENCES offre(id),
        id_intitule integer REFERENCES intitule(id),
        CONSTRAINT PK_o_i PRIMARY KEY(id_offre,id_intitule)
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

def query_params(conn,requete,params):
    cur = conn.cursor()
    cur.execute(requete,params)


def insert_villes(conn):
    with open("circos.csv","r") as floc:
        locreader = csv.DictReader(floc,delimiter=";")
        df = pd.DataFrame(locreader)

        dvf = df[['code_région', 'nom_région','numéro_département','nom_département',"code_insee","nom_commune","latitude","longitude"]]
        dvf = dvf.replace({"latitude":{"":"0.0"},"longitude":{"":"0.0"}})
        dvf = dvf.replace({"latitude":{"-":"0.0"},"longitude":{"-":"0.0"}})

        dvf = dvf.replace({"latitude":{r"^(-?\d{1,2}),(\d+)$":r"\1.\2"},"longitude":{r"^(-?\d{1,2}),(\d+)$":r"\1.\2"}},regex=True)

        dvf = dvf.astype({"latitude":"float32","longitude":"float32"},errors="ignore")        
        
        ddf = dvf.groupby(["numéro_département","nom_département","code_région"])
        departements = ddf.groups
        drf = dvf.groupby(["code_région","nom_région"])
        regions = drf.groups

        sql_reg = "INSERT INTO region (code_reg,nom) VALUES (%s,%s)"
        sql_dep = "INSERT INTO departement (code_dep, nom, code_reg) VALUES (%s,%s,%s)"
        sql_vil = "INSERT INTO ville (code_insee, nom, code_dep,latitude,longitude) VALUES (%s,%s,%s,%s,%s)"

        for reg in regions:
            query_params(conn,sql_reg,(reg[0],reg[1]))

        for dep in departements:
            query_params(conn,sql_dep,(dep[0],dep[1],dep[2]))

        communes = dvf.groupby(["code_insee","nom_commune","numéro_département","latitude","longitude"])
        villes = communes.groups

        insee = '0'
        for vil in villes:
            if insee != vil[0]:
                try:
                    if vil[0] == '97502' and not vil[1] == "BANDRABOUA" or not vil[0] == '97502':
                        query_params(conn,sql_vil,(vil[0],vil[1],vil[2],vil[3],vil[4]))
                except Exception as e:
                    print(e,vil[1])
                insee = vil[0]        



if __name__== "__main__":
    with connect() as conn:
        for command in commands:
            query(conn,command)
<<<<<<< HEAD
            conn.commit()

        try:
            insert_villes(conn)
            #mj.get_all_meteojob(True)
=======
        conn.commit() 
        try:
            insert_villes(conn)
            conn.commit()
            mj.get_all_meteojob(True)
>>>>>>> initialisation de la base
        except Exception as e:
            print(traceback.format_exc())
        finally:
            conn.commit()
