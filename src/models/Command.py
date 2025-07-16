from pymodm import MongoModel, fields


class Command(MongoModel):
    name = fields.CharField(required=True)
    enable = fields.BooleanField(required=True, default=True)
    reason = fields.CharField(default="")
    created_at = fields.DateTimeField()
