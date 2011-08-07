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
                             db=settings.SERVLET_DB
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
    marks = get_marks(db)
    models = get_models(db)
    years = get_model_years(db)
    mym = get_mym(db)
    # Fill 'models' field of the marks dict
    for model_id,model_d in models.items():
        marks[model_d['mark']]['models'].append(model_id)
    # Fill 'years' field of the models dict
    for _,model_id,year_id in mym:
        models[model_id]['years'].append(year_id)
    return (marks,models,years)

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
    query = "SELECT model_year_year FROM model_year WHERE model_year_id="+id+";"
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
    query = "SELECT power_name FROM power WHERE power_id="+id+";"
    db.query(query)
    r = db.store_result()
    out = r.fetch_row()[0][0]
    return out
    


