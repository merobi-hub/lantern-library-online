from flask import Blueprint, render_template, request, redirect, url_for, flash
from book_inventory.models import User, db, Book
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
    books = Book.query.all()
    return render_template('books.html', books = books)

@catalog.route('/addbook', methods = ['GET', 'POST'])
@login_required
def addbook():
    form = AddBookForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            author = form.author.data
            title = form.title.data
            user_id = current_user.id

            try:
                # Access API using form data
                response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}&key={credentials.API_KEY}').json()

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
            
                print(response.keys())
                print(response['items'][0]['selfLink']) #works for url
                print(response['items'][0]['volumeInfo']) #works for mucho info!

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
    id = request.args.get('id', None)
    title = request.args.get('title', None)
    Book.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'Thank you! *{title}* has been removed from the catalog.', 'user-created')
    return redirect(url_for('catalog.books'))