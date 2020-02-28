from flask import Flask, redirect, render_template, request, url_for
from . import diagrammes as dg


app = Flask(__name__)
#db.init_app(app)


@app.route("/", methods=["GET"])
def get_homepage():
    volume_unit = request.args.get("vol_unit", "j")

    hui = dg.dt.today()
    aujourdhui = ('0' if len(str(hui.day))==1 else "")+str(hui.day)+"-"+('0' if len(str(hui.month))==1 else "")+str(hui.month)+"-"+str(hui.year)
    nb_today, nb_total = dg.count_annonces()
    volume_mj,lib_unite = dg.get_volume_chart(volume_unit)
    carte = dg.get_map_chart()
    camembert = dg.get_part_chart()

    return render_template(
        "index.html",
        aujourdhui=aujourdhui,
        nb_today=nb_today,
        nb_total=nb_total,
        volume_mj=volume_mj,
        lib_unite=lib_unite,
        carte=carte,
        camembert=camembert)

