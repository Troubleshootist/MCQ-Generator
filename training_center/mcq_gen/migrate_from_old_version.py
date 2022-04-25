import simplejson
import models
import old_models

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()
engine = create_engine('sqlite:///mcq_old_base.db', echo=False)
Sess = sessionmaker(autoflush=False)
session = Sess(bind=engine)

def questions_migrate(json_file):
    file = open(json_file, 'r')
    obj = simplejson.load(file)
    for item in obj:
        question = models.Question()


if __name__ == '__main__':
    questions_migrate('/Users/dmitriy/Desktop/question.json')