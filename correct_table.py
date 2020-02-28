import create_table as ct

commands = (
    """
    UPDATE intitule
    SET nom = 'Big Data'
    WHERE alias LIKE '%Big Data%'
    AND nom IS NULL;
    """
    ,
    """
    UPDATE intitule
    SET nom = 'BI'
    WHERE (alias LIKE '%BI%'
    OR alias LIKE '%usiness%')
    AND nom IS NULL
    """,

    """
    UPDATE intitule
    SET nom = 'Data analyst'
    WHERE alias LIKE '%nalyst%'
    AND nom IS NULL;
    """
    ,
    """
    UPDATE intitule
    SET nom = 'Système'
    WHERE alias LIKE '%yst%'
    AND nom IS NULL;
    """
    ,
    """
    UPDATE intitule
    SET nom = 'Manager'
    WHERE alias LIKE '%anager%'
    AND nom IS NULL;
    """
    ,
    """
    UPDATE intitule
    SET nom = 'Data scientist'
    WHERE alias LIKE '%cientist%'
    AND nom IS NULL;
    """
    ,
    """
    UPDATE intitule
    SET nom = 'Développeur'
    WHERE alias LIKE '%velop%'
    AND nom IS NULL;
    """)


with ct.connect() as conn:
    for req in commands:
        ct.query(conn,req)
    conn.commit()

