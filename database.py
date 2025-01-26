from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    dni = Column(String(9), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    requested_capital = Column(Float, nullable=False)
    
    simulations = db.relationship('MortgageSimulation', backref='customer', lazy=True, cascade='all, delete-orphan')

class MortgageSimulation(db.Model):
    __tablename__ = 'mortgage_simulations'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, db.ForeignKey('customers.id'), nullable=False)
    apr = Column(Float, nullable=False)
    term_years = Column(Integer, nullable=False)
    monthly_installment = Column(Float, nullable=False)
    total_payback_amount = Column(Float, nullable=False)
    simulation_date = Column(DateTime, default=datetime.utcnow)
