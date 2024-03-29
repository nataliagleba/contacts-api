from app import ma


class EmailSchema(ma.Schema):
    class Meta:
        fields = ('address', 'contact_id')


class ContactSchema(ma.Schema):
    emails = ma.Nested(EmailSchema, many=True)

    class Meta:
        fields = ('username', 'last_name', 'username', 'emails')


emails_schema = EmailSchema(many=True)

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
