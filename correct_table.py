import create_table as ct

commands = (
    #"""
    #ALTER TABLE ville
    #MODIFY nom TYPE varchar(50);
    #"""
    #,
    #"""
    #ALTER TABLE ville
    #ADD latitude float;
    #"""
    #,
    #"""
    #ALTER TABLE ville
    #ADD longitude float;
    #"""
    #,

    """
    ALTER TABLE intitule 
    ALTER nom TYPE varchar(51);
    """
    ,
    """
    ALTER TABLE offre
    ALTER titre TYPE varchar(100);
    """,

    """
    ALTER TABLE intitule 
    ALTER alias TYPE varchar(51);
    """)


with ct.connect() as conn:
    for req in commands:
        ct.query(conn,req)
    conn.commit()

