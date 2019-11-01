import sys
sys.path.insert(0, 'wsi_api')

from factory import db

class Parameter(db.Model):

    __table_name__='parameter'

    VariableId = db.Column(db.Integer, primary_key=True)
    Year = db.Column(db.Integer, primary_key=True)
    AreaId = db.Column(db.Integer, primary_key=True)
    VariableName = db.Column(db.Text, index=False, unique=False, nullable=True)
    Value = db.Column(db.Integer, index=False, unique=False, nullable=True)
    Area = db.Column(db.Text, index=False, unique=False, nullable=True)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'year': self.Year,
           'areaid': self.AreaId,
           'value': self.Value,
           'area': self.Area,
           'variablename': self.VariableName
       }