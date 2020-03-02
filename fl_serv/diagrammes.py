import psycopg2 as p2
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
from flask import url_for
import pygal
import numpy as np
from IPython.display import HTML, SVG
from pygal.maps.fr import aggregate_regions
from . import pygalRegDep as pg



def count_annonces():
    jour, total = 0 , 0
    try:
        conn = p2.connect('host=localhost dbname=job_dashboard user=job password=dashboard port=5432')
        cur = conn.cursor()

        sql = """
                SELECT COUNT(*) FROM offre;
            """
        sql_day = """
                    SELECT COUNT(*) FROM offre
                    WHERE date_publication BETWEEN now()  - interval '1 day' AND now();
                """
        cur.execute(sql)
        total = cur.fetchone()[0]

        cur.execute(sql_day)
        jour = cur.fetchone()[0]

    except p2.OperationalError as e:
        pass

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    return (jour,total)

def get_map_chart(zoom="r"):
    return '<p>Diagramme indisponible</p>'

def get_part_chart():
    camembert = ""
    with p2.connect('host=localhost dbname=job_dashboard user=job password=dashboard port=5432') as conn:
        cur = conn.cursor()

        sql = """
            SELECT i.nom as nom_intitule,
            COUNT(*) as nb_offre
            FROM offre o
            INNER JOIN offre_intitule oi ON oi.id_offre = o.id
            INNER JOIN intitule i ON oi.id_intitule = i.id
            WHERE o.Date_publication > current_timestamp - interval '7 day'
            GROUP BY nom_intitule;
        """

        if not sql == "" :
            cur.execute(sql)
            resultat = cur.fetchall()

            values = []
            if len(resultat) > 0:
                nbr = []
                for ligne in resultat:
                    values.append(ligne)
                    nbr.append(ligne[1])

                df = pd.DataFrame(values, columns=['nom_intitule', 'nb_offre'])

                camembert = pg.pie_chart(df,"7","r")
                

    return camembert


def get_volume_chart(unite="j"):
    
    balise = "<p>Diagramme indisponible</p>"
    sql = ""
    lib_unite = ""
    
    try:
        conn = p2.connect('host=localhost dbname=job_dashboard user=job password=dashboard port=5432')
        cur = conn.cursor()
        
        
        if unite == "j":
            sql = """SELECT date_trunc('day', Date_publication) as jour, COUNT(*) as nb
                    FROM offre
                    GROUP BY jour
                    ORDER BY jour;
                """
            lib_unite = "jour"

        elif unite == "m":
            sql = """SELECT date_trunc('month', Date_publication) as jour, COUNT(*) as nb
                    FROM offre
                    GROUP BY jour
                    ORDER BY jour;
                """
            lib_unite = "mois"
            
        if not sql == "" :
            cur.execute(sql)
            resultat = cur.fetchall()

            vals = []
            if len(resultat) > 0:
                nbo = []
                for ligne in resultat:
                    vals.append([ligne[1],str(ligne[0].day)+"-"+str(ligne[0].month)+"-"+str(ligne[0].year)])
                    nbo.append(ligne[1])
                
                df = pd.DataFrame(vals,columns=["nb",lib_unite])

                ax = sns.pointplot(df[lib_unite],df["nb"], color="blue")
                ax.set(ylim=plt.ylim(bottom=0,top=max(nbo)+5))
                plt.xticks(rotation=25)

                titre = f"volume-{lib_unite}-"+dt.today().isoformat().split("T")[0]
         
                try:
                    plt.savefig("fl_serv/static/image/"+titre+".png")
                except Exception:
                    pass

                #loc_image = url_for('static', filename='image/'+titre)
                #balise = f'<img src="{loc_image}" alt="Volume d\'annonces par {lib_unite}" />'
        
    except p2.OperationalError as e:
        pass
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    
    return titre, lib_unite
