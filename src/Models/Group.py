from pymodm import MongoModel, fields


class Group(MongoModel):
    number = fields.CharField(required=True)
    events = fields.BooleanField(default=False)
    mod = fields.BooleanField(default=False)
