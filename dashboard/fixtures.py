import os
import os.path
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .storage import NotebookSQL, Base


def add_fixtures(sqlalchemy_conn_string='sqlite:///tmp.db'):
    engine = create_engine(sqlalchemy_conn_string)
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', 'basics.ipynb')), 'r') as fp:
        notebook1 = fp.read()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', 'bqplot.ipynb')), 'r') as fp:
        notebook2 = fp.read()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', 'ipyvolume.ipynb')), 'r') as fp:
        notebook3 = fp.read()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', 'matplotlib.ipynb')), 'r') as fp:
        notebook4 = fp.read()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', 'perspective.ipynb')), 'r') as fp:
        notebook5 = fp.read()

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples', 'multigraph.ipynb')), 'r') as fp:
        notebook6 = fp.read()

    nbs = [NotebookSQL(name='My Notebook 1',
                       notebook=notebook1,
                       created=datetime.now(),
                       modified=datetime.now()),
           NotebookSQL(name='My Notebook 2',
                       notebook=notebook2,
                       created=datetime.now(),
                       modified=datetime.now()),
           NotebookSQL(name='My Notebook 3',
                       notebook=notebook3,
                       created=datetime.now(),
                       modified=datetime.now()),
           NotebookSQL(name='My Notebook 4',
                       notebook=notebook4,
                       created=datetime.now(),
                       modified=datetime.now()),
           NotebookSQL(name='My Notebook 5',
                       notebook=notebook5,
                       created=datetime.now(),
                       modified=datetime.now()),
           NotebookSQL(name='My Notebook 6',
                       notebook=notebook6,
                       created=datetime.now(),
                       modified=datetime.now())]

    for nb in nbs:
        session.add(nb)
    session.commit()


if __name__ == '__main__':
    add_fixtures()
