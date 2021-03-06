from flask import Blueprint, render_template, request, redirect, url_for, flash
from book_inventory.models import User, db, Book, BookHistory
from book_inventory.forms import AddBookForm
# import json
import requests
# import urllib
from book_inventory.hidden import credentials
import re

from flask_login import current_user, login_required

catalog = Blueprint('catalog', __name__, template_folder='catalog_templates')

@catalog.route('/books')
def books():
    """Retrieves and returns all books in catalog."""
    books = Book.query.all()
    history = BookHistory.query.all()
    return render_template('books.html', books = books, history = history)

@catalog.route('/addbook', methods = ['GET', 'POST'])
@login_required
def addbook():
    """Adds book to catalog."""
    form = AddBookForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            author = form.author.data
            title = form.title.data
            user_id = current_user.id

            try:
                # Access API using form data
                response = requests.get(
                    f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}&key={credentials.API_KEY}'
                    ).json()

                publisher = response['items'][0]['volumeInfo']['publisher']
                description = response['items'][0]['volumeInfo']['description']
                genre = response['items'][0]['volumeInfo']['categories']
                image = response['items'][0]['volumeInfo']['imageLinks']['thumbnail']
                pub_date = response['items'][0]['volumeInfo']['publishedDate']
                more_info = response['items'][0]['volumeInfo']['infoLink']

                if len(description) > 500:
                    description = description[:497] + '...'
                genre = str(genre)
                genre = re.sub(r"[\([{})\]]", '', genre)

                book = Book(
                    author,  
                    title, 
                    publisher, 
                    description, 
                    genre,
                    image,
                    pub_date,
                    more_info,
                    user_id
                    )

                db.session.add(book)
                db.session.commit()

                flash(f'Thank you! A record for *{title}* has been added to the catalog.', 'user-created')
                return redirect(url_for('catalog.books'))

            except:

                publisher = ''
                description = ''
                genre = ''
                image = ''
                pub_date = ''
                more_info = ''

                book = Book(
                    author,
                    title,
                    publisher,
                    description,
                    genre,
                    image,
                    pub_date,
                    more_info,
                    user_id
                )

                db.session.add(book)
                db.session.commit()

                flash(f'Thank you for adding *{title}* to the catalog. Metadata about this title could not be found in the API, but you can edit the record below if you wish.', 'user-created')
                return redirect(url_for('site.profile'))

    except:
        flash(f"That didn't work. Please try again.")
        return redirect(url_for('catalog.books'))
        
    return render_template('addbook.html', form = form)

@catalog.route('/deletebook', methods = ['GET', 'POST'])
@login_required
def deletebook():
    """Removes book from catalog and adds it to history."""
    id = request.args.get('id', None)
    title = request.args.get('title', None)

    # Retrieve db info for title and add to BookHistory table
    book = Book.query.filter_by(id=id).first()
    author = book.author
    title = book.title
    publisher = book.publisher
    description = book.description
    genre = book.genre
    image = book.image
    pub_date = book.pub_date
    more_info = book.more_info
    user_id = book.user_id

    hist_add = BookHistory(
        author,
        title,
        publisher,
        description,
        genre,
        image,
        pub_date,
        more_info,
        user_id
    )

    db.session.add(hist_add)
    db.session.commit()

    # Remove book from Book table
    Book.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Thank you! *{title}* has been removed from the catalog.', 'user-created')
    return redirect(url_for('catalog.books'))