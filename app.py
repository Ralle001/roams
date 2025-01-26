from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from database import db, Customer, MortgageSimulation
from utils import validate_dni, validate_email, calculate_mortgage
from schemas import CustomerSchema, MortgageSimulationSchema
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mortgage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'title': 'Mortgage Simulation API',
    'uiversion': 3
}

db.init_app(app)
#swagger = Swagger(app)

# Swagger Configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger = Swagger(app, config=swagger_config)

customer_schema = CustomerSchema()
mortgage_schema = MortgageSimulationSchema()

@app.route('/customers', methods=['POST'])
def create_customer():
    """
    Create a new customer
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            dni:
              type: string
            email:
              type: string
            requested_capital:
              type: number
    responses:
      201:
        description: Customer created successfully
      400:
        description: Invalid input data
      409:
        description: Customer already exists
    """
    data = request.get_json()
    
    # Validate input
    errors = customer_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    if not validate_dni(data['dni']):
        return jsonify({"error": "Invalid DNI"}), 400
    
    if not validate_email(data['email']):
        return jsonify({"error": "Invalid email"}), 400
    
    # Check if customer already exists
    existing_customer = Customer.query.filter_by(dni=data['dni']).first()
    if existing_customer:
        return jsonify({"error": "Customer already exists"}), 409
    
    new_customer = Customer(**data)
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({"message": "Customer created", "customer_id": new_customer.id}), 201

@app.route('/customers/<dni>', methods=['GET'])
def get_customer(dni):
    """
    Get customer details by DNI
    ---
    parameters:
      - name: dni
        in: path
        type: string
        required: true
    responses:
      200:
        description: Customer details
      404:
        description: Customer not found
    """
    customer = Customer.query.filter_by(dni=dni).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    return jsonify({
        "name": customer.name,
        "dni": customer.dni,
        "email": customer.email,
        "requested_capital": customer.requested_capital
    })

@app.route('/customers/<dni>/simulate', methods=['POST'])
def simulate_mortgage(dni):
    """
    Simulate mortgage for a customer
    ---
    parameters:
      - name: dni
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            apr:
              type: number
            term_years:
              type: integer
    responses:
      200:
        description: Mortgage simulation result
      400:
        description: Invalid input data
      404:
        description: Customer not found
    """
    customer = Customer.query.filter_by(dni=dni).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    data = request.get_json()
    
    # Validate input
    errors = mortgage_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    simulation = calculate_mortgage(
        customer.requested_capital, 
        data['apr'], 
        data['term_years']
    )
    
    # Save simulation
    mortgage_sim = MortgageSimulation(
        customer_id=customer.id,
        apr=data['apr'],
        term_years=data['term_years'],
        monthly_installment=simulation['monthly_installment'],
        total_payback_amount=simulation['total_payback_amount']
    )
    
    db.session.add(mortgage_sim)
    db.session.commit()
    
    return jsonify(simulation)

@app.route('/customers/<dni>', methods=['PUT'])
def update_customer(dni):
    """
    Update customer details
    ---
    parameters:
      - name: dni
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
            requested_capital:
              type: number
    responses:
      200:
        description: Customer updated
      400:
        description: Invalid input data
      404:
        description: Customer not found
    """
    customer = Customer.query.filter_by(dni=dni).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        customer.name = data['name']
    
    if 'email' in data:
        if not validate_email(data['email']):
            return jsonify({"error": "Invalid email"}), 400
        customer.email = data['email']
    
    if 'requested_capital' in data:
        customer.requested_capital = data['requested_capital']
    
    db.session.commit()
    
    return jsonify({"message": "Customer updated"})

@app.route('/customers/<dni>', methods=['DELETE'])
def delete_customer(dni):
    """
    Delete a customer
    ---
    parameters:
      - name: dni
        in: path
        type: string
        required: true
    responses:
      200:
        description: Customer deleted
      404:
        description: Customer not found
    """
    customer = Customer.query.filter_by(dni=dni).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    
    return jsonify({"message": "Customer deleted"})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
