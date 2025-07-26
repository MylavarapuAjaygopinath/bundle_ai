from flask import Flask, render_template, request, jsonify
import os
from bundle_ai import run_bundle_ai

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    file = request.files["dataset"]
    cost_limit = float(request.form["cost_limit"])
    weight_limit = float(request.form["weight_limit"])

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = run_bundle_ai(path, cost_limit, weight_limit)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
