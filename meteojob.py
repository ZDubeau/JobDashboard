from requests_html import HTMLSession
from time import sleep
import json


def get_from_meteojob(url):
    session = HTMLSession()

    headers = {
        "Host": "www.meteojob.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "ABTasty=uid%3D20012809565792105%26fst%3D1580201817549%26pst%3D1581517299643%26cst%3D1581598588773%26ns%3D3%26pvt%3D11%26pvis%3D1%26th%3D; _fbp=fb.1.1580201818340.973396398; _ga=GA1.2.1214576890.1580201818; cikneeto_uuid=id:811e2d38-8a86-4a72-9b53-d92cb2fb87a7; cto_bundle=Dye-hl9qTnpXZEpDNkh1dURJTHdLdE1zQ1c1NlNJaXJJMEJzb2pmY01yZWdXUyUyRkpDWVB2dmEyR0daSXRsWU9EdElsJTJGJTJCUTElMkZTQkZqOTNBSlVnVzRFMHBycVhyUXhWZnZUdDNueVJ5UjZ4Zk41eXBDTWRvSHZsVlM3bENzQUslMkZ4U3hsako5ajQwdk0xSWpaUm9jJTJCRUFMY1dqdFElM0QlM0Q; __gads=ID=f83e1fa8b3f0b798:T=1580201871:S=ALNI_MZiG2mYjCj0SCw_MdkWUT9HiMCATw; _gid=GA1.2.872070098.1581517301; _tac=false~self|not-available; _ta=fr~4~8d7faf049ef65861988a9f7855c1ca28; exit_modal_closed=true; cikneeto=date:1581598601434; autocomplete_history_job=[{%22type%22:%22JOB%22%2C%22id%22:11540%2C%22label%22:%22D%C3%A9veloppeur%20Big%20Data%20(H/F)%22%2C%22count%22:990%2C%22ambiguous%22:false}]; web_user_id=41a78692-e95a-4835-b086-610970bc4126; ABTastySession=sen%3D3__referrer%3D__landingPage%3Dhttps%3A//www.meteojob.com/candidat/offres/offre-d-emploi-data-scientist-h-f-brest-bretagne-cdi-12007746%3Fscroll%3DaW5kZXg9MTUmdG90YWw9NTkmd2hhdD1EJUMzJUE5dmVsb3BwZXVyK0JpZytEYXRhKyhIJTJGRikmcGFnZT0y; _tty=2083560087699625985; _tas=y8pte1n6i5i; _gat=1; _gat_raw=1",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
#    url = "https://www.meteojob.com/candidat/offres/offre-d-emploi-data-scientist-h-f-paris-ile-de-france-cdi-12341413?what=data"
    meteo = session.get(url,headers=headers)


    contenu = meteo.html.find(".mj-offer-details",first=True)
    annonce = {}
    annonce["Titre"] = contenu.find("h1",first=True).text
    annonce["Date_publication_txt"] = contenu.find(".publication-date",first=True).text
    cont_json = meteo.html.find(".mj-column-content script",first=True)
    if cont_json is not None and cont_json != "":
        cont_json=json.loads(cont_json.text)
        annonce["Date_publication"] = cont_json["datePosted"].split("T")[0]
    else:
        annonce["Date_publication"] = annonce["Date_publication_txt"]

    items = contenu.find(".matching-criterion-wrapper")
    criteres = []
    for bal in items:
        criteres.append(bal.text)


    for crit in criteres:
        if "(H/F)" in crit:
            annonce["intitule"] = crit
        elif crit.endswith(")"):
            lieu = crit.split(" ")
            annonce["ville"] = lieu[0]
            annonce["code_dep"] = lieu[1][1:-1]
        elif crit in ("CDI","CDI-C","CDD","Interim","Stage"):
            annonce["Type_contrat"] = crit
        elif crit.startswith("Expérience"):
            annonce["Exp"] = crit.split(" : ")[1]
        elif crit.startswith("Niveau"):
            annonce["Diplome"] = crit.split(" : ")[1]


    sections = contenu.find("section")
    corps = ""

    for sect in sections:
        if sect.attrs.get("class") and "offer-apply-form" not in sect.attrs.get("class"):
            corps += sect.text + "\n"
        if sect.attrs.get("class") and "company-description" in sect.attrs.get("class"):
            annonce["Entreprise"] = sect.find("h3 span",first=True).text
        elif not sect.attrs.get("class"):
            if sect.find("h3") and sect.find("h3",first=True).text == "Salaire et avantages":
                annonce["Salaire"] = sect.find("div",first=True).text

    annonce["corps"] = corps

    annonce["Lien"] = url
    
    return annonce


def get_all_meteojob():
    session = HTMLSession()

    headers = {
        "Host": "www.meteojob.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "ABTasty=uid%3D20012809565792105%26fst%3D1580201817549%26pst%3D1581517299643%26cst%3D1581598588773%26ns%3D3%26pvt%3D11%26pvis%3D1%26th%3D; _fbp=fb.1.1580201818340.973396398; _ga=GA1.2.1214576890.1580201818; cikneeto_uuid=id:811e2d38-8a86-4a72-9b53-d92cb2fb87a7; cto_bundle=Dye-hl9qTnpXZEpDNkh1dURJTHdLdE1zQ1c1NlNJaXJJMEJzb2pmY01yZWdXUyUyRkpDWVB2dmEyR0daSXRsWU9EdElsJTJGJTJCUTElMkZTQkZqOTNBSlVnVzRFMHBycVhyUXhWZnZUdDNueVJ5UjZ4Zk41eXBDTWRvSHZsVlM3bENzQUslMkZ4U3hsako5ajQwdk0xSWpaUm9jJTJCRUFMY1dqdFElM0QlM0Q; __gads=ID=f83e1fa8b3f0b798:T=1580201871:S=ALNI_MZiG2mYjCj0SCw_MdkWUT9HiMCATw; _gid=GA1.2.872070098.1581517301; _tac=false~self|not-available; _ta=fr~4~8d7faf049ef65861988a9f7855c1ca28; exit_modal_closed=true; cikneeto=date:1581598601434; autocomplete_history_job=[{%22type%22:%22JOB%22%2C%22id%22:11540%2C%22label%22:%22D%C3%A9veloppeur%20Big%20Data%20(H/F)%22%2C%22count%22:990%2C%22ambiguous%22:false}]; web_user_id=41a78692-e95a-4835-b086-610970bc4126; ABTastySession=sen%3D3__referrer%3D__landingPage%3Dhttps%3A//www.meteojob.com/candidat/offres/offre-d-emploi-data-scientist-h-f-brest-bretagne-cdi-12007746%3Fscroll%3DaW5kZXg9MTUmdG90YWw9NTkmd2hhdD1EJUMzJUE5dmVsb3BwZXVyK0JpZytEYXRhKyhIJTJGRikmcGFnZT0y; _tty=2083560087699625985; _tas=y8pte1n6i5i; _gat=1; _gat_raw=1",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    
    url0 = "https://www.meteojob.com/jobsearch/offers?what=data&sorting=DATE"

    annonces = []
    cont = True
    ipage = 0

    while cont:

        ipage += 1
        url2 = url0+"&page="+str(ipage)
        meteo = session.get(url2,headers=headers)
        contenu = meteo.html.find(".block-link")

        for elt in contenu:
            url3 = "https://www.meteojob.com" + elt.attrs["href"]
            curannonce = get_from_meteojob(url3)
            if curannonce["Date_publication_txt"] == "Hier":
                cont = False
                break
            annonces.append(curannonce)

            sleep(2)

    return annonces



if __name__ == "__main__":
    adresse = input("Entrez une URL : ")
    if adresse == "":
        retour = get_all_meteojob()
        print(len(retour),retour[0])
    else:
        print(get_from_meteojob(adresse))
