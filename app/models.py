from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Text


class MySkill(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    learning_level = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return str(self.id) + ": " + self.name

