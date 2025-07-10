from pymodm import MongoModel, fields
from zoneinfo import ZoneInfo
from datetime import datetime

class User(MongoModel):
    number = fields.CharField(required=True)
    exp = fields.IntegerField(required=True, min_value=0, default=0)
    ban = fields.BooleanField(default=False, required=True)
    reason = fields.CharField(default='None')
    banned_at = fields.DateTimeField()
    created_at = fields.DateTimeField(default=datetime.now(ZoneInfo("Asia/Kolkata")),required=True)
