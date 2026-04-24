from flask import Flask, jsonify, request, render_template_string
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

students = [
    {"id": 1, "nom": "Mvounga", "prenom": "Jean", "note": 15.5},
    {"id": 2, "nom": "Obame", "prenom": "Marie", "note": 12.0},
    {"id": 3, "nom": "Ndong", "prenom": "Paul", "note": 18.0},
    {"id": 4, "nom": "Ondo", "prenom": "Sophie", "note": 9.5},
    {"id": 5, "nom": "Mba", "prenom": "Pierre", "note": 14.0},
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Gestion des Étudiants</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a0533 0%, #3d0066 50%, #6a0080 100%);
            padding: 40px 20px;
        }
        h1 {
            text-align: center;
            color: white;
            font-size: 2.2em;
            margin-bottom: 30px;
            text-shadow: 0 0 20px #ff69b4;
            letter-spacing: 2px;
        }
        .container { max-width: 950px; margin: 0 auto; }
        #message {
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            display: none;
            text-align: center;
            font-weight: bold;
        }
        .success { background: rgba(255, 105, 180, 0.3); color: #ff69b4; border: 1px solid #ff69b4; }
        .error { background: rgba(255, 0, 0, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }

        .form-container {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 105, 180, 0.3);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 25px;
        }
        .form-container h3 {
            color: #ff69b4;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .form-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
        input[type="text"], input[type="number"] {
            padding: 10px 15px;
            border: 1px solid rgba(255, 105, 180, 0.5);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 14px;
            outline: none;
            transition: border 0.3s;
        }
        input::placeholder { color: rgba(255, 255, 255, 0.5); }
        input:focus { border-color: #ff69b4; box-shadow: 0 0 10px rgba(255, 105, 180, 0.4); }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }

        .btn-save {
            background: linear-gradient(135deg, #ff69b4, #9b30ff);
            color: white;
        }
        .btn-reset {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .btn-edit {
            background: linear-gradient(135deg, #a855f7, #7c3aed);
            color: white;
            padding: 6px 12px;
            font-size: 12px;
        }
        .btn-delete {
            background: linear-gradient(135deg, #ff69b4, #e91e8c);
            color: white;
            padding: 6px 12px;
            font-size: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 105, 180, 0.2);
        }
        th {
            background: linear-gradient(135deg, #9b30ff, #ff69b4);
            color: white;
            padding: 14px;
            text-align: left;
            font-size: 14px;
            letter-spacing: 1px;
        }
        td {
            padding: 12px 14px;
            color: rgba(255, 255, 255, 0.9);
            border-bottom: 1px solid rgba(255, 105, 180, 0.1);
            font-size: 14px;
        }
        tr:hover td { background: rgba(255, 105, 180, 0.1); }

        .note-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
        }
        .note-high { background: rgba(100, 255, 150, 0.2); color: #64ff96; }
        .note-mid { background: rgba(255, 200, 0, 0.2); color: #ffc800; }
        .note-low { background: rgba(255, 100, 100, 0.2); color: #ff6464; }
    </style>
</head>
<body>
<div class="container">
    <h1>🎓 Gestion des Étudiants — INPTIC</h1>
    <div id="message"></div>

    <div class="form-container">
        <h3>✨ Ajouter / Modifier un étudiant</h3>
        <input type="hidden" id="student-id">
        <div class="form-row">
            <input type="text" id="nom" placeholder="Nom">
            <input type="text" id="prenom" placeholder="Prénom">
            <input type="number" id="note" placeholder="Note /20" step="0.5" min="0" max="20">
            <button class="btn-save" onclick="saveStudent()">💾 Sauvegarder</button>
            <button class="btn-reset" onclick="resetForm()">🔄 Réinitialiser</button>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Prénom</th>
                <th>Note</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="students-table"></tbody>
    </table>
</div>

<script>
    function showMessage(msg, type) {
        const el = document.getElementById('message');
        el.textContent = msg;
        el.className = type;
        el.style.display = 'block';
        setTimeout(() => el.style.display = 'none', 3000);
    }

    function getNoteClass(note) {
        if (note >= 14) return 'note-high';
        if (note >= 10) return 'note-mid';
        return 'note-low';
    }

    function loadStudents() {
        fetch('/students')
            .then(r => r.json())
            .then(data => {
                const tbody = document.getElementById('students-table');
                tbody.innerHTML = '';
                data.students.forEach(s => {
                    tbody.innerHTML += `
                        <tr>
                            <td>${s.id}</td>
                            <td>${s.nom}</td>
                            <td>${s.prenom}</td>
                            <td><span class="note-badge ${getNoteClass(s.note)}">${s.note}/20</span></td>
                            <td>
                                <button class="btn-edit" onclick="editStudent(${s.id}, '${s.nom}', '${s.prenom}', ${s.note})">✏️ Modifier</button>
                                <button class="btn-delete" onclick="deleteStudent(${s.id})">🗑️ Supprimer</button>
                            </td>
                        </tr>`;
                });
            });
    }

    function saveStudent() {
        const id = document.getElementById('student-id').value;
        const nom = document.getElementById('nom').value;
        const prenom = document.getElementById('prenom').value;
        const note = parseFloat(document.getElementById('note').value);

        if (!nom || !prenom || isNaN(note)) {
            showMessage('⚠️ Remplissez tous les champs !', 'error');
            return;
        }

        const method = id ? 'PUT' : 'POST';
        const url = id ? `/students/${id}` : '/students';

        fetch(url, {
            method: method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({nom, prenom, note})
        })
        .then(r => r.json())
        .then(() => {
            showMessage(id ? '✅ Étudiant modifié !' : '✅ Étudiant ajouté !', 'success');
            resetForm();
            loadStudents();
        });
    }

    function editStudent(id, nom, prenom, note) {
        document.getElementById('student-id').value = id;
        document.getElementById('nom').value = nom;
        document.getElementById('prenom').value = prenom;
        document.getElementById('note').value = note;
    }

    function deleteStudent(id) {
        if (!confirm('Supprimer cet étudiant ?')) return;
        fetch(`/students/${id}`, {method: 'DELETE'})
            .then(() => {
                showMessage('🗑️ Étudiant supprimé !', 'success');
                loadStudents();
            });
    }

    function resetForm() {
        document.getElementById('student-id').value = '';
        document.getElementById('nom').value = '';
        document.getElementById('prenom').value = '';
        document.getElementById('note').value = '';
    }

    loadStudents();
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"total": len(students), "students": students})

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Étudiant non trouvé"}), 404

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or not all(k in data for k in ["nom", "prenom", "note"]):
        return jsonify({"error": "Champs requis: nom, prenom, note"}), 400
    new_id = max(s["id"] for s in students) + 1 if students else 1
    new_student = {"id": new_id, "nom": data["nom"], "prenom": data["prenom"], "note": data["note"]}
    students.append(new_student)
    return jsonify(new_student), 201

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
