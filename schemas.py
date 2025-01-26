from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    dni = fields.Str(required=True)
    email = fields.Email(required=True)
    requested_capital = fields.Float(required=True, validate=validate.Range(min=0))

class MortgageSimulationSchema(Schema):
    apr = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    term_years = fields.Int(required=True, validate=validate.Range(min=1, max=40))
