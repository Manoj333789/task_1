from flask_sqlalchemy import SQLAlchemy
 
db =SQLAlchemy()

 

    
# Creating Book class with display_info method to display book details
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn}
    
# Creating Ebook which override Book class and adding file_format variable
class EBook(Book,db.Model):
    __tablename__ = "data_1"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    isbn = db.Column(db.String())
    file_format = db.Column(db.String())
    def __init__(self, title, author, isbn, file_format):
        super().__init__(title, author, isbn)
        self.file_format = file_format

    def display_info(self):
        info = super().display_info()
        info["file_format"] = self.file_format
        return info
    