from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from data.database import engine, User

Session = sessionmaker(bind=engine)

async def add_user(message, data):
    session = Session()

    new_user = User(user_id=str(message.from_user.id),
                    name=data["name"],
                    surname=data["surname"],
                    age=data["age"],
                    contacts=data["contacts"],
                    referrals=data["referrals"],
                    username="@" + message.from_user.username,
                    if_paid="n")
    session.add(new_user)
    session.commit()
    session.close()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

async def get_session(database):
    with Session.begin() as session:
        records = session.query(database).all()
        dict_of_entities = {}
        list_of_entities = []
        for record in records:
            user_data = object_as_dict(record)
            list_of_entities.append(user_data)
        for x in range(0, len(list_of_entities)):
            dict_of_entities[x] = list_of_entities[x]
            session.close()
        return dict_of_entities