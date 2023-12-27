from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name cannot be null")

        existing_author = self.query.filter(Author.name == name).first()
        if existing_author:
            raise ValueError("Duplicate name found")

        return name
 
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise ValueError("Author phone number must be exactly ten digits and contain only digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validate_content(self,key,content):
        if len(content)<250:
            raise ValueError("Content must be more than 250 characters")
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
                raise ValueError("Summary must be a maximum of 250 characters")
        return summary

    
    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category has to be either 'Fiction' or 'Non-Fiction'")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        inappropriate_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in inappropriate_words):
            raise ValueError("Post title must be sufficiently clickbait-y")
        return title


    
    




    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
