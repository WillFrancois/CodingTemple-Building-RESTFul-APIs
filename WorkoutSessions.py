from marshmallow import Schema, fields, validate

class WorkoutSession():
    def __init__(self, s_id, m_id, s_date, s_time, activity):
        self.s_id = s_id
        self.m_id = m_id
        self.s_date = s_date
        self.s_time = s_time
        self.activity = activity

class WorkoutSchema(Schema):
    s_id = fields.Integer(required=True, strict=True)
    m_id = fields.Integer(required=True, strict=True) #This is a foreign key that must connect with another table
    s_date = fields.Date()
    s_time = fields.Time(format="%H:%M")
    activity = fields.String(validate=validate.Length(max=255))

    class Meta:
        fields = ("s_id", "m_id", "s_date", "s_time", "activity")

class WorkoutUpdateSchema(Schema):
    s_date = fields.Date()
    s_time = fields.Time(format="%H:%M")
    activity = fields.String(validate=validate.Length(max=255))

    class Meta:
        fields = ("s_date", "s_time", "activity")
