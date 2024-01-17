from flask import Flask, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle

@app.route('/items', methods=['GET'])
def get_items():
  items = list(db.items.find({}, {'_id': 0}))
  return jsonify(items)

if __name__ == '__main__':  
  app.run('0.0.0.0',port=5001,debug=True)
  


