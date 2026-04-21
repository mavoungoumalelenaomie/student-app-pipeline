from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Initialise l’exporter Prometheus
metrics = PrometheusMetrics(app)

@app.route('/')
def hello():
    return "Hello, DevOps!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

