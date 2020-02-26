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

df = pd.DataFrame([annonce])  # Transformer Dict(Scraping) en DataFrame

def clean_salaire(df):
    
    ''' Nettoyer les données de la colonne "Salaire" et mettre dans 2 colonnes "min, max" '''
    
    list_salaire = []
    int_salaire = df['Salaire'].iloc[0]
    int_salaire = re.findall('(\d\s*\d\s*\d*)', int_salaire)  # Trouver les chiffres
    
    for v in int_salaire:
        list_salaire.append(v.replace('\xa0', ''))   # Supprimer certains lettres entre les chiffres
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

clean_salaire(df)

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

clean_exp(df)

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

clean_diplome(df)

def drop_column(df):
    
    ''' Supprimer toutes les colonnes qui ont séparer en min et max '''
    
    df.drop(columns =["Salaire"], inplace = True)
    df.drop(columns =["Exp"], inplace = True) 
    df.drop(columns =["Diplome"], inplace = True)
    
    return df

drop_column(df)

def clean_intitule(df):
    
    ''' Copier la valeur de colonne "Titre" dans la colonne "intitule" si elle est vide '''
    
    df['intitule'] = df['intitule'].fillna(df['Titre'])
    
    ''' Supprimer tous les suffixe de la colonne intitule si ça existe '''
    
    intitule = df['intitule'][0]
    intitule = intitule.replace(" (H/F) ","")
    intitule = intitule.replace(" (H/F)","")
    intitule = intitule.replace("(H/F)","")
    intitule = intitule.strip()
    df.loc[:, ('intitule')] = intitule
    
    ''' Separer plusieurs intitules en plusieures lignes s'il y a > 1 '''
    
    df = df.set_index(["Titre", "Date_publication", "ville",
                       "code_dep", "Type_contrat", "Exp_min","Exp_max",
                       "Diplome_min", "Diplome_max", "Entreprise", "Salaire_min",
                       "Salaire_max", "corps", "Lien"]).apply(lambda x: x.str.split(',').explode()).reset_index()
    
    return df

clean_intitule(df)

def pandas_func(dict_):
    
    ''' Appeler toutes les fonctions '''
    
    df = pd.DataFrame([dict_])  # Transformer DataFrame en Dict
    df = clean_salaire(df)
    df = clean_exp(df)
    df = clean_diplome(df)
    df = drop_column(df)
    df = clean_intitule(df)
    
    return df.to_dict()

pandas_func()