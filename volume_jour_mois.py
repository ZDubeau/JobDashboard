import psycopg2 as p2
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt


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
            for ligne in resultat:
                vals.append([ligne[1],str(ligne[0].day)+"-"+str(ligne[0].month)+"-"+str(ligne[0].year)])

            df = pd.DataFrame(vals,columns=["nb","jour"])

            ax = sns.pointplot(df["jour"],df["nb"], color="purple")
            ax.set(ylim=plt.ylim(bottom=0))

            titre = f"volume-{lib_unite}-"+dt.today().isoformat().split("T")[0]
            plt.savefig("img/"+titre)

            balise = f'<img src="{titre}" alt="Volume d\'annonces par {lib_unite}" />'
        
    except p2.OperationalError as e:
        pass
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    
    return balise
