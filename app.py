from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# In-memory database
posts = []
post_id_counter = 1

# Resource for single post
class PostResource(Resource):
    def get(self, post_id):
        for post in posts:
            if post["id"] == post_id:
                return post, 200
        return {"message": "Post not found"}, 404

    def put(self, post_id):
        data = request.get_json()
        if "title" not in data or "content" not in data:
            return {"error": "Title and content are required"}, 400

        for post in posts:
            if post["id"] == post_id:
                post["title"] = data["title"]
                post["content"] = data["content"]
                post["author"] = data.get("author", post["author"])
                return post, 200
        return {"message": "Post not found"}, 404

    def delete(self, post_id):
        global posts
        posts = [p for p in posts if p["id"] != post_id]
        return {"message": "Post deleted"}, 200

# Resource for list of posts
class PostListResource(Resource):
    def get(self):
        return posts, 200

    def post(self):
        global post_id_counter
        data = request.get_json()
        if "title" not in data or "content" not in data:
            return {"error": "Title and content are required"}, 400

        new_post = {
            "id": post_id_counter,
            "title": data["title"],
            "content": data["content"],
            "author": data.get("author", "Anonymous")
        }
        posts.append(new_post)
        post_id_counter += 1
        return new_post, 201

# Routes
api.add_resource(PostListResource, "/posts")
api.add_resource(PostResource, "/posts/<int:post_id>")

if __name__ == "__main__":
    app.run(debug=True)
