from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Transaction
from datetime import datetime

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("/transactions", methods=["POST"])
@jwt_required()
def add_transaction():
    data = request.get_json()
    
    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description")
    date = data.get("date") or datetime.utcnow()

    if amount is None or category is None:
        return jsonify({"error": "Amount and category are required"}), 422

    user_id = get_jwt_identity()

    transaction = Transaction(
        amount=amount,
        category=category,
        description=description,
        date=date,
        user_id=user_id
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201

@transaction_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    result = []

    for t in transactions:
        result.append({
            "id": t.id,
            "amount": t.amount,
            "category": t.category,
            "description": t.description,
            "date": t.date.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(result), 200

@transaction_bp.route('/transactions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    user_id = get_jwt_identity()

    transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted successfully"}), 200

@transaction_bp.route('/summary', methods=['GET'])
@jwt_required()
def financial_summary():
    user_id = get_jwt_identity()

    transactions = Transaction.query.filter_by(user_id=user_id).all()

    total_income = 0
    total_expense = 0

    for t in transactions:
        if t.amount > 0:
            total_income += t.amount
        else:
            total_expense += abs(t.amount)

    balance = total_income - total_expense

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }), 200