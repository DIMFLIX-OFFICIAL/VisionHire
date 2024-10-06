from sqladmin import ModelView

from .models import User, Hierarchy, Candidate, Vacancy, Task, Interview


class UsersView(ModelView, model=User):
    column_list = [column.name for column in User.__table__.columns]

class HierarchyView(ModelView, model=Hierarchy):
    column_list = [column.name for column in Hierarchy.__table__.columns]

class CandidateView(ModelView, model=Candidate):
    column_list = [column.name for column in Candidate.__table__.columns]

class VacancyView(ModelView, model=Vacancy):
    column_list = [column.name for column in Vacancy.__table__.columns]

class TaskView(ModelView, model=Task):
    column_list = [column.name for column in Task.__table__.columns]

class InterviewView(ModelView, model=Interview):
    column_list = [column.name for column in Interview.__table__.columns]


all_views = [UsersView, HierarchyView, CandidateView, VacancyView, TaskView, InterviewView]
