from flask import Flask, abort, redirect, render_template, request

from model import db,EBook

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()
    

# Creating Library class with add_book,display_all_book,delete_book and search_book_by_title methods
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_all_books(self):
        l=[]
        for i in self.books:
            l.append(i)
        return l
    def delete_book(self,title):
        for i in self.books:
            if i.title == title:
                del i
                return "book deleted"

    def search_book_by_title(self, title):
        
        for book in self.books:
            if book.title == title:
                return book
        return {"message": "Book Not Found"}


library = Library()

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':



        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        file_format = request.form['file_format']

        book={
            "title":title,
            "author":author,
            "isbn":isbn,
            "file_format":file_format
            }
        library.add_book(book)
        print(library.display_all_books())
        
        students = EBook(
            title=title,
            author=author,
            isbn=isbn,
            file_format=file_format
        )
        db.session.add(students)
        db.session.commit()
        return redirect('/')
    

@app.route('/')
def RetrieveList():
    students = EBook.query.all()
    return render_template('datalist.html', students = students)


@app.route('/<int:id>')
def RetrieveStudent(id):
    students = EBook.query.filter_by(id=id).first()
    print(library.search_book_by_title(students.title))
    return render_template('data.html', students = students)
 

@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    students = EBook.query.filter_by(id=id).first()
    library.delete_book(students.title)
    if students:
        db.session.delete(students)
        db.session.commit()
        return redirect('/')
    abort(404)
    
 
@app.route('/<int:id>/edit',methods = ['GET','POST'])
def update(id):
    student = EBook.query.filter_by(id=id).first()
    print(id)

    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()  
        
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        file_format = request.form['file_format']
        
        student = EBook(
            title=title,
            author=author,
            isbn=isbn,
            file_format=file_format
            
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')
 
    return render_template('update.html', student = student)


if __name__=="__main__":
    app.run(debug=True)