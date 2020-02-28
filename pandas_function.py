from urllib.request import urlopen
from requests_html import HTMLSession
from time import sleep
import json
import re
import pandas as pd
from pandas import DataFrame
from pandas import isnull
import numpy as np
from collections import defaultdict
import psycopg2 as p2
import traceback


#df = pd.DataFrame([annonce])  # Transformer Dict(Scraping) en DataFrame

def clean_salaire(df):
    
    ''' Nettoyer les données de la colonne "Salaire" et mettre dans 2 colonnes "min, max" '''
    
    list_salaire = []
    int_salaire = df['Salaire'].iloc[0]
    int_salaire = re.findall('(\d\s*\d\s*\d*)', int_salaire)  # Trouver les chiffres
    
    for v in int_salaire:
        list_salaire.append(v.replace('\xa0', '').replace(" ",""))   # Supprimer certains lettres entre les chiffres
        list_salaire = [int(i) for i in list_salaire]
        
    if len(list_salaire) == 0:
        df["Salaire_min"] = 'NaN'
        df["Salaire_max"] = 'NaN'
        
    elif len(list_salaire) == 1:
        df["Salaire_min"] = list_salaire[0]
        df["Salaire_max"] = 'NaN'
        
    else:
        df["Salaire_min"]= list_salaire[0] 
        df["Salaire_max"]= list_salaire[1]
    
    return df

#clean_salaire(df)

def clean_exp(df):
    
    ''' Nettoyer les données de la colonne "Experience" et mettre dans 2 colonnes "min, max" '''
    
    list_exp = []
    int_expr = df['Exp'].iloc[0]
    int_exp = re.findall(r'[0-9]+', int_expr)  # Trouver seulement les chiffres
    
    list_exp = [int(i) for i in int_exp]
    
    if len(list_exp) == 0:
        df["Exp_min"] = 'NaN'
        df["Exp_max"] = 'NaN'
        
    elif len(list_exp) == 1:
        df["Exp_min"] = list_exp[0]
        df["Exp_max"] = 'NaN'
        
    elif len(list_exp) == 2:
        df["Exp_min"] = list_exp[0]
        df["Exp_max"] = list_exp[1]
        
    else:
        df["Exp_min"]= list_exp[0] 
        df["Exp_max"]= list_exp[-1]
    
    return df

#clean_exp(df)

def clean_diplome(df):
    
    ''' Définir une foction qui execute et modifie la colonne "Diplome" spour le site "METEOJOB" '''
                  
    for index, row in df.iterrows(): 
        diplome = [str(i).strip() for i in row['Diplome'].split(",")]
    
        dict_diplome = {'Bac':['Bac', 'BAC', 'Bac. Général'],
                        'Bac+2': ['BAC+2', 'Bac+2', 'DUES', 'type DEUG', 'DUT', 'BTS'],
                        'Bac+3': ['BAC+3', 'Bac+3', 'Licence générale', 'Licence professionnelle'],
                        'Bac+4': ['Bac+4', 'BAC+4', 'Master 1', 'MIAGE', 'Maîtrise', 'type DEA - DESS'],
                        'Bac+5': ['Bac+7', '> BAC+5', 'Bac+5', 'Master - Magistère', 'BAC+5','Master',
                                  "Diplôme de grande école d'ingénieur", 'Diplôme de grande école de commerce']}
        
        list_cles = list(dict_diplome.keys())  # list de clés du dictionaire
        
        list_diplome  = []
        for value in diplome:
            for key in list_cles:
                if value in dict_diplome[key]:
                    list_diplome .append(key)
                    
    list_diplome = (list(set(list_diplome )))  # Supprimer les doublons de la list

    if len(list_diplome) == 0:
        df["Diplome_min"] = 'NaN'
        df["Diplome_max"] = 'NaN'

    elif len(list_diplome) == 1:
        df["Diplome_min"] = list_diplome[0]
        df["Diplome_max"] = 'NaN'

    else:
        df["Diplome_min"]= list_diplome[0] 
        df["Diplome_max"]= list_diplome[1]
        
    return df

#clean_diplome(df)

def drop_column(df):
    
    ''' Supprimer toutes les colonnes qui ont séparer en min et max '''
    
    df.drop(columns =["Salaire"], inplace = True)
    df.drop(columns =["Exp"], inplace = True) 
    df.drop(columns =["Diplome"], inplace = True)
    
    return df

#drop_column(df)

def clean_intitule(df):
    
    ''' Copier la valeur de colonne "Titre" dans la colonne "intitule" si elle est vide '''
    
    df['intitule'] = df['intitule'].fillna(df['Titre'])
    
    ''' Supprimer tous les suffixe de la colonne intitule si ça existe '''
    
    #intitule = df['intitule'][0]
    #intitule = intitule.replace(" (H/F) ","")
    #intitule = intitule.replace(" (H/F)","")
    #intitule = intitule.replace("(H/F)","")
    #intitule = intitule.strip()
    #df['intitule'][0] = intitule
    
    def intitule_clean(intitule):
    
        intitule = intitule.replace(" (H/F) ","")
        intitule = intitule.replace(" (H/F)","")
        intitule = intitule.replace("(H/F)","")
        return intitule.strip()

    df['intitule'][0] = intitule_clean(df['intitule'][0])

    ''' Separer plusieurs intitules en plusieures lignes s'il y a > 1 '''
    
    df = df.set_index(['Titre', 'Date_publication',  'ville', 'code_dep',
       'Type_contrat', 'Entreprise', 'corps', 'Lien', 'Date_publication_txt',
       'Salaire_min', 'Salaire_max', 'Exp_min', 'Exp_max', 'Diplome_min',
       'Diplome_max','Reference','Site_origine']).apply(lambda x: x.str.split(',').explode()).reset_index()

    print("in funct : ", df["intitule"]) 

    return df

#clean_intitule(df)

def pandas_func(dict_):
    
    ''' Appeler toutes les fonctions '''
    
    df = pd.DataFrame([dict_])  # Transformer DataFrame en Dict
    print(df.columns)
    df = clean_salaire(df)
    print(1)
    df = clean_exp(df)
    print(2)
    df = clean_diplome(df)
    print(3)
    df = drop_column(df)
    print(4)
    try:
        df = clean_intitule(df)
    except Exception:
        print(df.columns,df["intitule"])
        raise ValueError()
    
    return df.to_dict()

#pandas_func()


def insertion(annonces):
    con_params = """
                  host=localhost
                  dbname=job_dashboard
                  user=job
                  password=dashboard
                  port=5432
                  """
    with p2.connect(con_params) as conn:
        cur = conn.cursor()

        clean = pandas_func(annonces)
        
        
        if clean["ville"].get(0):
            print(clean["ville"])
            if clean["code_dep"].get(0):
                print(clean["code_dep"])
                sql = "SELECT code_insee, code_dep FROM ville WHERE nom = %s AND code_dep = %s"
                params = (clean["ville"][0].strip(),clean["code_dep"][0])
                try:
                    cur.execute(sql,params)
                    print("arg")
                except Exception as e:
                    print(traceback.format_exc())
                    

            else:
                print("no code dep")
                sql = "SELECT code_insee, code_dep FROM ville WHERE nom = %s"
                cur.execute(sql,(clean["ville"][0].strip(),))

            rinsee = cur.fetchall()

            if len(rinsee) == 1:
                insee = rinsee[0][0]
                code_dep = rinsee[0][1]
            else:
                insee = None
                code_dep = clean["code_dep"].get(0)
        
        if code_dep:
            sql = "SELECT code_reg FROM departement WHERE code_dep = %s"
            cur.execute(sql,(code_dep,))
            region = cur.fetchall()
            if len(region) == 1:
                region = region[0][0]
            else:
                region = None
        
        if clean["intitule"].get(0):
            intitules = []
            #print(clean["intitule"])
            for k,tit in clean["intitule"].items():
                tit = tit.strip()
                sql = "SELECT id FROM intitule WHERE alias = %s"
                cur.execute(sql,(tit,))
                exists = cur.fetchall()
                if len(exists)>0:
                    intitules.append(exists[0][0])
                else:
                    sql = """
                            INSERT INTO intitule (alias) 
                            VALUES (%s)
                            RETURNING id;
                        """
                    cur.execute(sql,(tit,))
                    exists = cur.fetchall()
                    if len(exists)>0:
                        intitules.append(exists[0][0])

        sql = """
                INSERT INTO offre (titre, date_publication, type_contrat, exp_min, exp_max,
                diplome_min, diplome_max, entreprise, salaire_min, salaire_max, corps, lien_site,
                ref, site_origine, ville, departement, region)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """
        to_check = [
            clean["Titre"].get(0),
            clean["Date_publication"].get(0),
            clean["Type_contrat"].get(0),
            clean["Exp_min"].get(0),
            clean["Exp_max"].get(0),
            clean["Diplome_min"].get(0),
            clean["Diplome_max"].get(0),
            clean["Entreprise"].get(0),
            clean["Salaire_min"].get(0),
            clean["Salaire_max"].get(0),
            clean["corps"].get(0),
            clean["Lien"].get(0),
            clean["Reference"].get(0),
            clean["Site_origine"].get(0),
            insee,
            code_dep,
            region
        ]

        to_insert = []
        for elt in to_check:
            if elt == "NaN":
                to_insert.append(None)
            else:
                to_insert.append(elt)

        to_insert = tuple(to_insert)
        print(to_insert)
        cur.execute(sql,to_insert)
        id_offre = cur.fetchall()
        if len(id_offre):
            id_offre = id_offre[0][0]
        else:
            id_offre = None

        if id_offre and len(intitules):
            sql = "INSERT INTO offre_intitule (id_offre, id_intitule) VALUES (%s, %s)"
            for intitule in intitules:
                cur.execute(sql,(id_offre,intitule))

        conn.commit()
