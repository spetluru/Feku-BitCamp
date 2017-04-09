from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask_restful import reqparse
import feku
from flask import make_response
from flask.ext.restful import fields, marshal
from flask import jsonify

app = Flask(__name__)
api = Api(app)
@app.route('/')
def api_root():
    return "Hello, World!"


@app.route('/api', methods=['GET','POST'])
def get_url():
    url = request.args.get('url')
    results = feku.get_indicators(url)
    fields = {
    'summary_similarity': results[0],
    'keyword_similarity': results[1],
    'opinion_score':results[2],
    'num_tones':results[3], 
    'tone_score':results[4],
    
    }
    return jsonify(fields)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

    
if __name__ == '__main__':
    app.run(debug=True)