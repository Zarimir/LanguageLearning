from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'study'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/study'

mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def hello_world():
    language = mongo.db.language
    output = []
    for obj in language.find():
        output.append(obj['language'])
    print(output)
    language.insert({'language':'dutch'})
    return 'Done!'


if __name__ == '__main__':
    app.run()
