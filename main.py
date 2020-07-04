# import main Flask class and request object
from flask import Flask, request, jsonify
import engine
from flask_cors import CORS

app = Flask(__name__)  # create the Flask app
CORS(app)


@app.route('/solve')
def api():
    truss = engine.defineTruss()
    result = engine.solve(truss)
    return jsonify(result)


@app.route('/truss', methods=['POST'])
def truss():

    beams = request.get_json()
    truss = engine.trussMaker(beams)
    result = engine.solve(truss)
    print(truss.nodes[5].rollingReaction)
    return jsonify(result)


print(__name__)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # run app in debug mode on port 4200
