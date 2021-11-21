from flask_login import current_user
from website.models import Transaction
from . import db, constant

def get_total_spending_for_category(c):
    list = db.session.query(Transaction).filter_by(user_id=current_user.id, category=c)
    return sum([x.price for x in list])

def get_highest_spending_category():
    maximum_spending = -3
    max_category = ''
    for c in constant.ACCEPTED_CATEGORIES:
        val = get_total_spending_for_category(c)
        if val > maximum_spending:
            max_category = c
            maximum_spending = val
    return max_category

