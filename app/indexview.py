from flask_appbuilder import IndexView, expose
from .models import MySkill
from . import db


class IndexView(IndexView):

    @expose('/')
    def index(self):
        mySkills=db.session.query(MySkill).all()
        
        self.update_redirect()
        return self.render_template(
            'index.html',
            appbuilder=self.appbuilder,
            skills=mySkills)
