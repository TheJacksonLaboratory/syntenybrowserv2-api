from src import ma
from ..model import Hello


class HelloSchema(ma.ModelSchema):
    class Meta:
        model = Hello
        strict = True
