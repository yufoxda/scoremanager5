from App.app_init_ import app,db,per_page
from App.app_init_ import Book, Song
from flask import render_template, request, url_for
from flask_sqlalchemy import pagination 
import os

@app.route("/")
def home():
  return render_template('Pages/home.html')

@app.route("/searchbook",methods = ["GET"])
def searchbook():
  page = request.args.get('page', 1, type=int)
  query = request.args.get('query')
  app.logger.info(query)
  books = db.session.query(Book).filter(Book.book_name.contains(query)).order_by(Book.book_name).paginate(page=page, per_page=30, error_out=False)

  return render_template('Pages/searched_book.html',books = books,que = query,page=page)

@app.route("/searchsong",methods = ["GET"])
def searchsong():
  page = request.args.get('page', 1, type=int)
  query = request.args.get('query')
  app.logger.info(query)
  songs = db.session.query(Song).filter(Song.song_name.contains(query)).order_by(Song.song_name).paginate(page=page, per_page=30, error_out=False)
  app.logger.info(songs)
  return render_template('Pages/searched_song.html',songs=songs,que = query,page=page)

@app.route("/book/<int:id>")
def bookinfo(id):
  bookid = id
  songs = db.session.query(Song).filter(Song.book_id == bookid).all()
  bookname = db.session.query(Book).get(bookid)
  return render_template('Pages/book.html',songs = songs,book = bookname)
