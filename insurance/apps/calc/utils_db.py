# -*- coding: utf-8 -*-
"""
Функции для получения данных о моделях и годах выпуска из
базы данных и упаковки их в json
"""
from insurance import settings
import json

MYSQL_AVAILABLE = False
try:
    import MySQLdb
    MYSQL_AVAILABLE = True
except ImportError, e:
    pass

def connect():
    if not MYSQL_AVAILABLE:
        return None
    try:
        db = MySQLdb.connect(host=settings.SERVLET_DB_HOST,
                             user=settings.SERVLET_DB_USER,
                             passwd=settings.SERVLET_DB_PASS,
                             port=settings.SERVLET_DB_PORT,
                             db=settings.SERVLET_DB,
                             charset='utf8',
                             )
        return db
    except MySQLdb.OperationalError, e:
        print "ERROR CONNECTING: ", e
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
        st = u''
        st = row[0][1]
        import sys
        out.append(element)
    return out

def get_marks(db):
    """
    Получить словарь словарей марок.
    {id:{'name':mark_name,models:[model_id,model_id....]}
    }
    массив model_id пустой, будет заполнен позже
    """
    query = "SELECT mark_id,mark_name FROM mark;"
    db.query(query)
    r = db.store_result()
    out = {}
    while True:
        row = r.fetch_row()
        if not row:
            break
        element = {'name':row[0][1],'models':[]}
        out[int(row[0][0])] = element
    return out

def get_models(db):
    """
    Получить словарь словарей моделей.
    {id:{'name':model_name,years:[year_id,year_id....]}
    }
    массив years пустой, будет заполнен позже
    """
    query = "SELECT model_id,model_name,model_mark FROM model;"
    db.query(query)
    r = db.store_result()
    out = {}
    while True:
        row = r.fetch_row()
        if not row:
            break
        element = {'name':row[0][1],
                   'mark':int(row[0][2]),
                   'years':[]}
        out[int(row[0][0])] = element
    return out

def get_model_years(db):
    """
    Получить словарь годов выпуска
    {id:year}
    """
    query = "SELECT model_year_id,model_year_year FROM model_year;"
    db.query(query)
    r = db.store_result()
    out = {}
    while True:
        row = r.fetch_row()
        if not row:
            break
        out[int(row[0][0])] = int(row[0][1])
    return out

def get_mym(db):
    """
    Получить словарь массивов связей [(id,model,year),...]
    """
    query = "SELECT mym_id,mym_m,mym_y FROM mym;"
    db.query(query)
    r = db.store_result()
    out = []
    while True:
        row = r.fetch_row()
        if not row:
            break
        element = (int(row[0][0]),int(row[0][1]),int(row[0][2]))
        out.append(element)
    return out

def get_mark_model_year_data(db):
    import sys
    marks = get_marks(db)
    models = get_models(db)
    years = get_model_years(db)
    mym = get_mym(db)
    # Fill 'models' field of the marks dict
    for model_id,model_d in models.items():
        marks[model_d['mark']]['models'].append(model_id)
    # Fill 'years' field of the models dict В качестве индекса для
    # года выпуска испольуем индекс связи модель-год из таблицы mym
    years_d = {}
    for mym_id,model_id,year_id in mym:
        years_d[mym_id] = years[year_id]
        models[model_id]['years'].append(mym_id)
    # Отсортировать года в словарях моделей, иначе в формах будут
    # выпадать вперемешку
    for model_id,model_d in models.items():
        model_d['years'].sort()
    return (marks,models,years_d)

def get_mark_model_year_json():
    """
    Запаковывает и возврачает данные о марке, модели и годах
    выпуска в json
    """
    db = connect()
    marks,models,years = get_mark_model_year_data(db)
    marks_json = json.dumps(marks)
    models_json = json.dumps(models)
    years_json = json.dumps(years)
    return (marks_json,models_json,years_json)

def get_mark_by_id(db,id):
    query = "SELECT mark_name FROM mark WHERE mark_id="+id+";"
    db.query(query)
    r = db.store_result()
    out = r.fetch_row()[0][0]
    return out

def get_model_by_id(db,id):
    query = "SELECT model_name FROM model WHERE model_id="+id+";"
    db.query(query)
    r = db.store_result()
    out = r.fetch_row()[0][0]
    return out

def get_model_year_by_id(db,id):
    if not id:
        return ""
    query = 'SELECT model_year.model_year_year FROM model_year,mym WHERE mym.mym_id='+id+' AND model_year.model_year_id=mym.mym_y;'
    db.query(query)
    r = db.store_result()
    out = r.fetch_row()[0][0]
    return out

def get_city_by_id(db,id):
    query = "SELECT city_name FROM city WHERE city_id="+id+";"
    db.query(query)
    r = db.store_result()
    out = r.fetch_row()[0][0]
    return out

def get_power_by_id(db,id):
    import sys
    print "id =", id
    query = "SELECT power_name FROM power WHERE power_id="+id+";"
    db.query(query)
    r = db.store_result()
    out = r.fetch_row()[0][0]
    return out

def get_power_by_model_and_year(mym_id):
    db = connect()
    # query = 'SELECT power_id,power_name,power_mym FROM power WHERE power_mym='+str(mym_id)+' ORDER BY power_id'
    query = 'SELECT power_id,power_name,power_mym FROM power WHERE power_mym=1 ORDER BY power_id'
    db.query(query)
    r = db.store_result()
    out = []
    while True:
        row = r.fetch_row()
        if not row:
            break
        out.append((row[0][0],row[0][1]))
    return out

def get_price_by_model_and_power(price_mym,price_power):
    import sys
    print >> sys.stderr, "get_price_by_model_and_power(price_mym,price_power)"
    db = connect()
    # Заглушка, пока не заполнена база данных, принимаем price_mym=1
    price_mym = 1
    query = 'SELECT price_min,price_max FROM price WHERE price_mym='+str(price_mym)+' AND price_power='+str(price_power)+';'
    print >> sys.stderr, "query =", query
    db.query(query)
    r = db.store_result()
    out = []
    row = r.fetch_row()
    print >> sys.stderr, "row =", row
    # [price_min,price_max]
    out.append((row[0][0],row[0][1]))
    return out
    
    
