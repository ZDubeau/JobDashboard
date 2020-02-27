from bs4 import BeautifulSoup
import requests
import re
from time import sleep

liste_offre_emploi = []
URL  = 'https://offre-demploi.monster.fr/stage-r-d-génie-logiciel-pour-lia-intégration-et-tests-h-f-grenoble-isère-auvergne-rhône-alpes-fr-atos-se-société-européenne/ee1f8e4a-6dea-4a58-97aa-b64437fcd342'
URL = 'https://www.monster.fr/emploi/recherche/?q=D%C3%A9veloppeur+Python&where=Grenoble%2C+Auvergne-Rh%C3%B4ne-Alpes&intcid=&cy=fr&rad=20&client='
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
debut = False

for link in soup.find_all('a'):

    if debut:
        liste_offre_emploi.append(link.get('href'))
    if link.get('href') == "#list":
        debut = True

if debut:
    for url_emploi in liste_offre_emploi:
        # On va chercher le détail des différentes offres d'emploi
        page = requests.get(url_emploi)
        soup = BeautifulSoup(page.text, 'html.parser')
       # print(soup)
        results = soup.findAll('tr')

        my_dict = {}
        for result in results:
            text = result.get_text().strip()
            print(text)

            if '<div class="details-content is-preformated' in text:
                print(text)
        soup_string = str(soup)

        enregistrement_en_cours = False
        annonce_memorisee = ""
        for ligne_courante in soup_string:
       #     print(ligne_courante)
       #     print(ligne_courante.startswith('<div class="details-content is-preformated'))

            if ligne_courante is not None:
                #print(str(ligne_courante))
                if ligne_courante.startswith('<div class="details-content is-preformated'):
                    enregistrement_en_cours = True
                elif ligne_courante.startswith('<footer class="card-footer">'):
                    enregistrement_en_cours = False
               # print(enregistrement_en_cours)

                if enregistrement_en_cours:
                #    print(ligne_courante)
                    annonce_memorisee.append(ligne_courante)

        print(annonce_memorisee)

