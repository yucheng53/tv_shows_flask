from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

class Show():
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def save_show(cls, data):
        query = "INSERT INTO shows (title, network, release_date, description, created_at, updated_at, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW(), %(user_id)s )"
        return connectToMySQL('tv_shows_schema').query_db( query, data )

    @classmethod
    def get_all_shows(cls,data):
        query = "SELECT * FROM shows WHERE user_id = %(id)s;"
        results = connectToMySQL('tv_shows_schema').query_db(query,data)
        shows = []
        for show in results:
            shows.append( cls(show) )
        return shows

    @classmethod
    def one_show(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL("tv_shows_schema").query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s, updated_at = NOW() WHERE id=%(id)s; "
        return connectToMySQL('tv_shows_schema').query_db( query, data )
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM shows WHERE id=%(id)s; "
        return connectToMySQL('tv_shows_schema').query_db( query, data )
    
    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (user_id, show_id) VALUES (%(user_id)s, %(show_id)s, NOW(), NOW() )"
        return connectToMySQL('tv_shows_schema').query_db( query, data )
    
    @classmethod
    def num_like(cls,data):
        query = "SELECT COUNT(user_id) AS num FROM likes WHERE show_id=%(id)s;"
        results = connectToMySQL("tv_shows_schema").query_db(query, data)
        print(results)
        return results[0]['num']

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show["title"]) < 3:
            flash("Title must be at least 3 characters.", "error")
            is_valid = False
        if len(show["network"]) < 3:
            flash("Network must be at least 3 characters.", "error")
            is_valid = False
        if not show["release_date"]:
            flash("All fields must be filled out.", "error")
            is_valid = False
        if len(show["description"]) < 3:
            flash("Description must be at least 3 characters.", "error")
            is_valid = False
        return is_valid
    
