# -*- coding: utf-8 -*-

MYSQL_AVAILABLE = False
try:
    import _mysql
    MYSQL_AVAILABLE = True
except ImportError, e:
    pass

def connect():
    if not MYSQL_AVAILABLE:
        return None
    try:
        db = _mysql.connect(host='127.0.0.1',
                            user='insdu',
                            passwd='insdpwd',
                            port=3306,
                            db='inservlet'
                            )
        return db
    except _mysql.exceptions.OperationalError:
        return None
    
def get_choices(db, id_field='',name_field='',table=''):
    query = "SELECT %s,%s FROM %s;" % (id_field,name_field,table)
    db.query(query)
    r = db.store_result()
    out = []
    while True:
        row = r.fetch_row()
        if not row:
            break
        element = row[0]
        out.append(element)
    return out
