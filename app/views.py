from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from app import appbuilder, app, db
from .models import MySkill

from flask_appbuilder.forms import DynamicForm

from wtforms import SelectField, TextAreaField, TextField, validators


"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

"""
    MySkill登録用のForm
"""
class MySkillForm(DynamicForm):
    MY_CHOICES = [
        ('5', 'Level5: その道では専門家と呼ばれてます'),
        ('4', 'Level4: 人に教えることができる程度'),
        ('3', 'Level3: 普通に使える程度'),
        ('2', 'Level2: ちょっと使ったことある程度'),
        ('1', 'Level1: ちょっと知っている程度'),
    ]
    learning_level = SelectField('習得レベル', [validators.required()], choices=MY_CHOICES)
    name = TextField('スキル名', [validators.required(), validators.length(max=50)], description='例：Python, 機械学習, 英語 など')
    description = TextAreaField('説明', [validators.required(), validators.length(max=200)], description='スキルの習熟度合いを200字以内で説明してください')

"""
    MySkill登録・編集用のModelView
"""
class MySkillModelView(ModelView):
    datamodel = SQLAInterface(MySkill)
    edit_form=MySkillForm
    add_form=MySkillForm
    list_columns=['learning_level', 'name', 'description']

appbuilder.add_view(MySkillModelView,
                    'Skills',
                    icon = 'fa-envelope',
                    category = 'My Skills')

db.create_all()

