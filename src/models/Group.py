from pymodm import MongoModel, fields


# 👥 Group Model
class Group(MongoModel):
    number = fields.CharField(required=True)
    events = fields.BooleanField(default=False, required=True)
    mod = fields.BooleanField(default=False, required=True)
