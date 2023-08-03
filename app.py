from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
import pymongo

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Initialize Flask-Swagger
swagger = Swagger(app)

client = pymongo.MongoClient("<mongodb_uri>")
db = client["mydatabase"]  # Replace "mydatabase" with your database name
articles_collection = db["articles"]
comments_collection = db["comments"]

# ...

@app.route('/api/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    new_article = {
        'title': title,
        'content': content,
        'likes': 0
    }
    result = articles_collection.insert_one(new_article)
    new_article['_id'] = result.inserted_id

    return jsonify(new_article), 201


@app.route('/api/articles/<string:article_id>', methods=['GET'])
def get_article(article_id):
    article = articles_collection.find_one({'_id': pymongo.ObjectId(article_id)})
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    comments_list = list(comments_collection.find({'article_id': pymongo.ObjectId(article_id)}))
    article['comments'] = comments_list
    article['likes'] = like_counts.get(article_id, 0)

    return jsonify(article), 200


@app.route('/api/articles/<string:article_id>/comments', methods=['POST'])
def add_comment(article_id):
    data = request.get_json()
    author = data.get('author')
    content = data.get('content')

    article = articles_collection.find_one({'_id': pymongo.ObjectId(article_id)})
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    new_comment = {
        'article_id': pymongo.ObjectId(article_id),
        'author': author,
        'content': content
    }
    result = comments_collection.insert_one(new_comment)
    new_comment['_id'] = result.inserted_id

    return jsonify(new_comment), 201

# ...

if __name__ == '__main__':
    app.run(debug=True)
