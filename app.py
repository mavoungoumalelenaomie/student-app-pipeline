from flask import Flask, jsonify, request
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
        "message": "API Gestion des étudiants",
        "endpoints": {
            "GET": ["/students", "/students/<id>"],
            "POST": "/students",
            "PUT": "/students/<id>",
            "DELETE": "/students/<id>"
        }
    })

# READ - Tous les étudiants
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"total": len(students), "students": students})

# READ - Un étudiant
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Étudiant non trouvé"}), 404

# CREATE - Ajouter un étudiant
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or not all(k in data for k in ["nom", "prenom", "note"]):
        return jsonify({"error": "Champs requis: nom, prenom, note"}), 400
    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {
        "id": new_id,
        "nom": data["nom"],
        "prenom": data["prenom"],
        "note": data["note"]
    }
    students.append(new_student)
    return jsonify(new_student), 201

# UPDATE - Modifier un étudiant
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    data = request.get_json()
    student.update({
        "nom": data.get("nom", student["nom"]),
        "prenom": data.get("prenom", student["prenom"]),
        "note": data.get("note", student["note"])
    })
    return jsonify(student)

# DELETE - Supprimer un étudiant
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": f"Étudiant {student_id} supprimé"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
