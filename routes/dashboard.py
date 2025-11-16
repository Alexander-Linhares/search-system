from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/Dashboards')

@dashboard_bp.route('/')
def dashboard_handler():
    print("você foi redirecionado para dashboards")
    return render_template('dashboard.j2')
