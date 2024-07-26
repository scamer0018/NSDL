from pymodm import MongoModel, fields


class Group(MongoModel):
    jid = fields.CharField(required=True)
    events = fields.BooleanField(default=False)
    mod = fields.BooleanField(default=False)
