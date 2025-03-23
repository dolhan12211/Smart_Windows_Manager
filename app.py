# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/window/status', methods=['POST'])
def window_status():
    data = request.get_json()
    print(f"Otrzymane dane: {data}")
    # Tutaj dodaj logikę decyzyjną dotyczącą otwierania/zamykania okna
    return jsonify({"success": True, "message": "Dane zostały otrzymane"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)