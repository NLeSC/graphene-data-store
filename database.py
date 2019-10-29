from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///db.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import Department, User, Role, Dataset
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create the fixtures
    engineering = Department(name='Engineering')
    db_session.add(engineering)
    hr = Department(name='Human Resources')
    db_session.add(hr)

    manager = Role(name='manager')
    db_session.add(manager)
    engineer = Role(name='engineer')
    db_session.add(engineer)

    peter = User(name='Peter', department=engineering, role=engineer)
    db_session.add(peter)
    roy = User(name='Roy', department=engineering, role=engineer)
    db_session.add(roy)
    tracy = User(name='Tracy', department=hr, role=manager)
    db_session.add(tracy)

    # Dataset
    data = {"x": [1, 2, 3], "y": [4.2, 5.7, 6.3], "category": ['a', 'b', 'c']}
    test_data1 = Dataset(name='dataset1', description='First dataset', table_name='data1', is_active=True, raw=data)
    db_session.add(test_data1)
    data = {"x": [1.1, 2.3, 3], "y": [4, 5, 6]}    
    test_data2 = Dataset(name='dataset2', description='Second dataset', table_name='data2', is_active=False, raw=data)
    db_session.add(test_data2)


    db_session.commit()