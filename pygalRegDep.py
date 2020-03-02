import pygal
import psycopg2 # for database connection
import pandas as pd
import numpy as np
from datetime import datetime as dt
from IPython.display import HTML, SVG
from pygal.maps.fr import aggregate_regions

def region_offre(regions,profondeur):
    
    from pygal.maps.fr import aggregate_regions
    from pygal.style import Style
    
    custom_style=Style(background='#F0F8FF',colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'))
    fr_chart = pygal.maps.fr.Regions(style=custom_style, human_readable=True)
    #fr_chart.title = "le nombre d'offre par regions"
    regions_dict = dict(zip(regions.reg_code,regions.nb_offre))
    if profondeur =="1":
        duree = "1 jour"
    else:
        duree = profondeur + " jours"    
    fr_chart.add(duree, regions_dict)
    regions_to_display=fr_chart.render()
    fr_chart.render_to_file("Graphs/carte_region_"+profondeur+".svg")
    
def dep_offre(departements,profondeur):

    from pygal.maps.fr import aggregate_regions
    from pygal.style import Style
    
    custom_style=Style(background='#F0F8FF',colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'))
    fr_chart = pygal.maps.fr.Departments(style=custom_style, human_readable=True)
    #fr_chart.title = "le nombre d'offre par départements"
    departement_dict = dict(zip(departements.dep_code,departements.nb_offre))
    if profondeur =="1":
        duree = "1 jour"
    else:
        duree = profondeur + " jours"  
    fr_chart.add(duree, departement_dict)
    departements_to_display=fr_chart.render()
    #HTML(html_pygal.format(departements_to_display.decode("utf-8")))
    fr_chart.render_to_file("Graphs/carte_departement_"+profondeur+".svg")

def pie_chart(df,profondeur,unite):
    pie_chart = pygal.Pie()
    #if unite == "r":
        #pie_chart.title = "le pourcentage d'offre par regions"
    #elif unite == "d":
        #pie_chart.title = "le pourcentage d'offre par départements"
    total = 0
    for data in df.values:
        total += data[2]
    for data in df.values:
        percent = round(data[2]/total*100,1)
        pie_chart.add(data[0],percent)
    if unite == "r":
        pie_chart.render_to_file("Graphs/pie_chart_regions_"+profondeur+".svg")    
    elif unite == "d":
        pie_chart.render_to_file("Graphs/pie_chart_departement_"+profondeur+".svg")   
    
    
def get_infos(unite="r",profondeur="30"):
    
    balise = "<p>Carte indisponible</p>"
    sql = ""
    lib_unite = ""
    
    try:
        conn = psycopg2.connect('host=localhost dbname=job_dashboard user=job password=dashboard port=5432')
        cur = conn.cursor()
        if unite == "r":
            sql = """
                        SELECT region.nom as nom_region,
                        region.code_reg as reg_code,
                        count(*) as nb_offre
                        FROM offre
                        INNER JOIN ville ON ville.code_insee = offre.ville 
                        INNER JOIN region ON region.code_reg = offre.region
                        WHERE offre.Date_publication > current_timestamp - interval '""" + profondeur + """ day'
                        GROUP BY nom_region, reg_code
                        ORDER BY nb_offre DESC;
                    """
            lib_unite = "region"

        elif unite == "d":
            sql = """
                        SELECT departement.nom as nom_dep,
                        ville.code_dep as dep_code,
                        count(*) as nb_offre
                        FROM offre
                        INNER JOIN ville ON ville.code_insee = offre.ville 
                        INNER JOIN departement ON departement.code_dep = offre.departement
                        WHERE offre.Date_publication > current_timestamp - interval '""" + profondeur + """ day'
                        GROUP BY nom_dep, dep_code
                        ORDER BY nb_offre DESC;
                    """
            lib_unite = "departement"    
            
        if not sql == "" :
            cur.execute(sql)
            resultat = cur.fetchall()
        
            values = []
            if len(resultat) > 0:
                nbr = []
                for ligne in resultat:
                    values.append(ligne)
                    nbr.append(ligne[1])
                #print(values)
                if unite == "r":
                    df = pd.DataFrame(values, columns=['nom_region', 'reg_code', 'nb_offre'])
                    #df.pivot('nom_region', 'nom_ville', 'nb_offre', 'date_pub', 'lat', 'lng')
                    region_offre(df,profondeur)
                    
                elif unite == "d":
                    df = pd.DataFrame(values, columns=['nom_dep','dep_code', 'nb_offre'])
                    #df.pivot('nom_region', 'nom_ville', 'nb_offre', 'date_pub', 'lat', 'lng')
                    dep_offre(df,profondeur)
                
                pie_chart(df,profondeur,unite)
                #return df

    except psycopg2.OperationalError as error:
        pass
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    
get_infos("r","1")
get_infos("r","7")
get_infos("r","30")
get_infos("d","1")
get_infos("d","7")
get_infos("d","30")