from flask import Blueprint, render_template, request

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/Dashboards')

@dashboard_bp.route('/')
def dashboard_handler():
    print("você foi redirecionado para dashboards")

    initial_page = request.args.get('page', 1, int)
    file = request.args.get('file', None)

    return render_template('dashboard.j2', file=file, page=initial_page)
