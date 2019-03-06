import datetime as dt
from ..model import Session, Hello

def say_hello(name=None):
    Session.add(Hello(who=name, when=dt.datetime.now()))
    Session.commit()
    return {"message": "Hello {}!".format(name if name else "World")}

