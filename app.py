from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Données étudiants
students = [
    {"id": 1, "nom": "Mvounga", "prenom": "Jean", "note": 15.5},
    {"id": 2, "nom": "Obame", "prenom": "Marie", "note": 12.0},
    {"id": 3, "nom": "Ndong", "prenom": "Paul", "note": 18.0},
    {"id": 4, "nom": "Ondo", "prenom": "Sophie", "note": 9.5},
    {"id": 5, "nom": "Mba", "prenom": "Pierre", "note": 14.0},
]

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur l'API de gestion des étudiants",
        "endpoints": ["/students", "/students/<id>", "/metrics"]
    })

@app.route('/students')
def get_students():
    return jsonify({
        "total": len(students),
        "students": students
    })

@app.route('/students/<int:student_id>')
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Étudiant non trouvé"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
