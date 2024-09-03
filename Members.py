from marshmallow import Schema, fields, validate

class Member():
    def __init__(self, pk, name, age):
        self.pk = pk
        self.name = name
        self.age = age

#Used for creating new users
class MemberSchema(Schema):
    pk = fields.Integer(required=True, strict=True)
    name = fields.String(validate=validate.Length(max=255), required=True)
    age = fields.Integer(strict=True)

    class Meta:
        fields = ("pk", "name", "age")

#Used for updating existing users
class MemberUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(max=255), required=True)
    age = fields.Integer(strict=True)

    class Meta:
        fields = ("name", "age")
