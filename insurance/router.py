class NewcalcRouter(object):
    """A router to control all database operations on models in
    the newcalc application"""

    def db_for_read(self, model, **hints):
        "Point all operations on newcalc models to 'remote'"
        if model._meta.app_label == 'newcalc':
            return 'remote'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on newcalc models to 'remote'"
        if model._meta.app_label == 'newcalc':
            return 'remote'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in newcalc is involved"
        if obj1._meta.app_label == 'newcalc' or obj2._meta.app_label == 'newcalc':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the newcalc app only appears on the 'remote' db"
        if db == 'remote':
            return model._meta.app_label == 'newcalc'
        elif model._meta.app_label == 'newcalc':
            return False
        return None
