from flask import jsonify

def handle_validtion_error(e):
    print("Invalid form data")
    return jsonify({'error': 'Invalid form data', 'datails': e.errors()[0]["type"]}), 400
