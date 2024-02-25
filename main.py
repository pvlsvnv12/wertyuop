from flask import Flask, jsonify
from flask_restful import reqparse
from ml.main import prediction
from collect_data import open_database
from collect_data import close_database
from collect_data import insert_item_to_companies_table
from collect_data import get_id_from_data
from collect_data import get_data_from_table_with_id
from collect_data import calculate_spent_budget
from collect_data import insert_item_to_history_table
from collect_data import get_history_dict


app = Flask(__name__)


@app.route('/api/partners', methods=['POST'])  # pyright: ignore
def add_company():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('budget', type=float)
    args = parser.parse_args()

    connection, cur = open_database()

    insert_item_to_companies_table(cur, args['name'], args['budget'], False)

    id_of_company = get_id_from_data(cur, args['name'], args['budget'])
    fresh_data_to_return = [id_of_company, args['name'], args['budget'], 0]
    all_params = ['id', 'name', 'budget', 'spent_budget']
    return_data = {all_params[i]: fresh_data_to_return[i] for i in range(len(all_params))}

    close_database(connection)
    return jsonify(return_data)


@app.route('/api/partners/<int:id>', methods=['GET'])  # pyright: ignore
def get_company(id):
    connection, cur = open_database()

    name, budget, is_stopped = get_data_from_table_with_id(cur, id)
    spent_budget = calculate_spent_budget(cur, id)
    fresh_data_to_return = [id, name, budget, spent_budget, is_stopped]
    all_params = ['id', 'name', 'budget', 'spent_budget', 'is_stopped']
    return_data = {all_params[ind]: fresh_data_to_return[ind] for ind in range(len(all_params))}

    close_database(connection)
    return jsonify(return_data)


@app.route('/api/partners/<int:id>/cashback', methods=['PUT'])  # pyright: ignore
def update_company(id):
    parser = reqparse.RequestParser()
    parser.add_argument('date', type=str)
    parser.add_argument('cashback', type=float)
    args = parser.parse_args()

    connection, cur = open_database()
    name, budget, is_stopped = get_data_from_table_with_id(cur, id)

    is_stopped = prediction(name, get_history_dict(cur, id),
                            calculate_spent_budget(cur, id), budget)
    insert_item_to_history_table(cur, id, args['date'], args['cashback'], is_stopped)

    close_database(connection)
    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
