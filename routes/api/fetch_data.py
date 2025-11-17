from flask import Blueprint, jsonify

dataset_rows_bp = Blueprint('dataset_rows', __name__, url_prefix='/dataset_rows')

@dataset_rows_bp.route('/', methods=['GET'])
def get_dataset_slice():
    some_fake_data = {
        'table_content': ['banana', 'maça', 'melão']
    }

    return jsonify(some_fake_data)