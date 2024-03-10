from db import get_db
from models import Package

db = get_db()

def get_packages():
    packages = db.query(Package).all()
    db.close()
    return packages

def get_package_by_id(id):
    package = db.query(Package).filter_by(package_id=id).one()
    db.close()
    return package