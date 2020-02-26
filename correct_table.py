import create_table as ct

commands = (
    """
    ALTER TABLE ville
    MODIFY nom TYPE varchar(50);
    """
    ,
    """
    ALTER TABLE ville
    ADD latitude float;
    """
    ,
    """
    ALTER TABLE ville
    ADD longitude float;
    """
    )

with ct.connect() as conn:
    for req in commands:
        ct.query(conn,req)
    conn.commit()

