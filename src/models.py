from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) 
    favorite_planet = db.relationship('Planet', lazy=True)
    favorite_character = db.relationship('Character', lazy=True)
   

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "favorite_planet": list(map(lambda x: x.serialize(), self.favorite_planet)),
            "favorite_character": list(map(lambda x: x.serialize(), self.favorite_character))
        }

    #Add user
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    #Add character
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    #Add planet
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet = db.Column(db.String(50), unique=True, nullable=False)
    character = db.Column(db.String(50), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Favorite %r>' % self.planet

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet,
            "character": self.character,
        }
        
    #Add favorite
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self