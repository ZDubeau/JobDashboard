import sys
import pytest

# Manip pour permettre l'import d'un module se trouvant dans le répertoire parent
sys.path.append("..")

import create_table as ct

import psycopg2

def test_connexion():
    assert ct.connect() is not None
    assert type(ct.connect()) is psycopg2.extensions.connection


def test_tables():
    with ct.connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM offre_brute")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM offre")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM intitule")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM ville")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM departement")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM region")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM secteur")
        assert cur.fetchall() == [(0,),]
        cur.execute("SELECT COUNT(*) FROM offre_secteur")
        assert cur.fetchall() == [(0,),]











