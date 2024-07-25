from pymodm import MongoModel, fields


class Group(MongoModel):
    jid = fields.CharField(required=True)
    events = fields.BooleanField(min_value=False)
    mod = fields.BooleanField(min_value=False)
