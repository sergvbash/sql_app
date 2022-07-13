from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://User:saraBarabu0@localhost/project_tracker')
Base = declarative_base(engine)

class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True)
    title = Column(String(50))

    def __repr__(self):
        return "<Project(project_id='{0}', title='{1}')".format(self.project_id, self.title)


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    # project_id = Column(Integer)
    description = Column(String(100))

    project = relationship('Project')

    def __repr__(self):
        return "<Task(task_id = '{0}', project_id='{1}', description='{2}')".format(self.task_id, self.project_id, self.description)

Base.metadata.create_all(engine, checkfirst=True)

def create_session():
    session=sessionmaker(bind=engine)
    return session()

if __name__=='__main__':
    session = create_session()
    pro = Project(title = 'Check mail for the reciept')
    try:
        session.add(pro)
        session.flush()
        print('Added', pro)
        taskone = Task(project_id=pro.project_id, description='go to elevator')
        session.add(taskone)
        session.flush()
        print('Added', taskone)
    except:
        print('Sth wrong!')
        session.rollback()
    session.commit()
    session.close()