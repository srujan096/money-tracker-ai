from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Expense, Budget

main_bp = Blueprint('main', __name__)

# ---------- DASHBOARD ---------- #
from datetime import datetime

@main_bp.route('/')
@login_required
def index():
    
    today = datetime.today()
    month, year = today.month, today.year

    # Fetch current user's expenses for current month/year
    expenses = Expense.query.filter_by(user_id=current_user.id)\
        .filter(db.extract('month', Expense.date) == month)\
        .filter(db.extract('year', Expense.date) == year)\
        .all()

    # ✅ Fetch all budgets for current user (no strict filter)
    budgets = Budget.query.filter_by(user_id=current_user.id).all()

    total_spent = sum(e.amount for e in expenses)
    total_budget = sum(b.limit_amount for b in budgets)

    categories = [e.category for e in expenses]
    amounts = [e.amount for e in expenses]

    return render_template(
        'dashboard.html',
        expenses=expenses,
        budgets=budgets,
        total_spent=total_spent,
        total_budget=total_budget,
        month=month,
        year=year,
        categories=categories,
        amounts=amounts
    )



# ---------- ADD EXPENSE ---------- #
from datetime import datetime

@main_bp.route('/add-expense', methods=['POST'])
@login_required
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    note = request.form.get('note', '')
    date_str = request.form.get('date')

    # ✅ Convert string to Python date
    if date_str:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            date = datetime.today().date()
    else:
        date = datetime.today().date()

    new_expense = Expense(
        amount=amount,
        category=category,
        note=note,
        date=date,
        user_id=current_user.id
    )

    db.session.add(new_expense)
    db.session.commit()
    flash('Expense added!', 'success')
    return redirect(url_for('main.index'))


# ---------- DELETE EXPENSE ---------- #
@main_bp.route('/delete-expense/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.index'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'info')
    return redirect(url_for('main.index'))

# ---------- ADD BUDGET ---------- #
@main_bp.route('/add-budget', methods=['POST'])
@login_required
def add_budget():
    category = request.form['category']
    limit_amount = float(request.form['limit_amount'])
    month = int(request.form['month'])
    year = int(request.form['year'])

    budget = Budget(
        category=category,
        limit_amount=limit_amount,
        month=month,
        year=year,
        user_id=current_user.id
    )

    db.session.add(budget)
    db.session.commit()
    flash('Budget added!', 'success')
    return redirect(url_for('main.index'))


@main_bp.route('/')
@login_required
def home():
    return redirect(url_for('main.dashboard'))


@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Default to current month/year
    today = datetime.today()
    month = request.args.get('month', type=int, default=today.month)
    year = request.args.get('year', type=int, default=today.year)

    # Fetch data for selected month/year
    expenses = Expense.query.filter_by(user_id=current_user.id)\
        .filter(db.extract('month', Expense.date) == month)\
        .filter(db.extract('year', Expense.date) == year)\
        .all()

    budgets = Budget.query.filter_by(user_id=current_user.id, month=month, year=year).all()

    total_spent = sum(e.amount for e in expenses)
    total_budget = sum(b.limit_amount for b in budgets)

    categories = [e.category for e in expenses]
    amounts = [e.amount for e in expenses]

    return render_template(
        'dashboard.html',
        expenses=expenses,
        budgets=budgets,
        total_spent=total_spent,
        total_budget=total_budget,
        month=month,
        year=year,
        categories=categories,
        amounts=amounts
    )

from app.ml_logic import predict_category
from app import csrf  # add this import at the top of routes.py

@csrf.exempt

@main_bp.route('/predict-category', methods=['POST'])
@login_required
def predict_category_route():
    note = request.json.get('note', '')
    if not note.strip():
        return jsonify({'category': ''})
    predicted = predict_category(note)
    return jsonify({'category': predicted})

from app import csrf
import os
from flask import jsonify
from flask_login import login_required, current_user

@csrf.exempt
@main_bp.route('/retrain-model', methods=['POST'])
@login_required
def retrain_model_route():
    # Optional: only admin can trigger retraining
    if current_user.email != "test123@gmail.com":
        return jsonify({'error': 'Unauthorized'}), 403

    os.system("python train_model.py")
    return jsonify({'status': 'Model retrained successfully'})
