from pymodm import MongoModel, fields


class User(MongoModel):
    username = fields.CharField(default=None)
    icon = fields.URLField(default=None)
    bio = fields.URLField(default=None)
    jid = fields.CharField(required=True)
    exp = fields.IntegerField(required=True, min_value=0, default=0)
    ban = fields.BooleanField(default=False)
    reason = fields.CharField(default='')
    banned_at = fields.DateTimeField()
    created_at = fields.DateTimeField(required=True)
