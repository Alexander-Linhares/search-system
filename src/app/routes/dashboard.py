from flask import Blueprint, render_template, request, current_app
from app.functions import match_files

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/Dashboards')

@dashboard_bp.route('/')
def dashboard_handler():
    print("você foi redirecionado para dashboards")

    initial_page = request.args.get('page', 1, int)
    file_name = request.args.get('file', None)
    if file_name:
        db_node = current_app.config.get('DATABASE', None)
        file = match_files(db_node, file_name)
        print(file)

    return render_template('dashboard.j2', file=file, page=initial_page)
