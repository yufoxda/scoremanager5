from App.app_init_ import app,db,ppage
from App.app_init_ import Book, Song,Artist,Lyricist,SongWriter,Arranger
from flask import render_template, request, url_for,jsonify
from flask_sqlalchemy import pagination 
from sqlalchemy.orm import joinedload , contains_eager

import random
import os

@app.route("/")
def home():
  num = db.session.query(Book).count()
  random_ids = random.sample(range(1, num), 4)
  picup = db.session.query(Book).filter(Book.id.in_(random_ids)).all()
  return render_template('Pages/home.html',picup = picup)


@app.route("/searchbook",methods = ["GET"])
def searchbook():
  page = request.args.get('page', 1, type=int)
  query = request.args.get('query')
  app.logger.info(query)
  books = db.session.query(Book).filter(Book.book_name.contains(query)).order_by(Book.book_name).paginate(page=page, per_page=ppage, error_out=False)

  return render_template('Pages/searched_book.html',books = books,que = query,page=page)

@app.route("/searchsong",methods = ["GET"])
def searchsong():
  page = request.args.get('page', 1, type=int)
  query = request.args.get('query')
  app.logger.info(query)
  songs = db.session.query(Song).filter(Song.song_name.contains(query)).order_by(Song.song_name).paginate(page=page, per_page=ppage, error_out=False)
  app.logger.info(songs)
  return render_template('Pages/searched_song.html',songs=songs,que = query,page=page)



@app.route("/advancedsearch", methods=["GET"])
def advancedsearch():
    search_params = {
        'book': request.args.get('book'),
        'song': request.args.get('song'),
        'artist': request.args.get('artist'),
        'lyricist': request.args.get('lyricist'),
        'song_writer': request.args.get('songWriter'),
        'arranger': request.args.get('arranger'),
        'grade': request.args.get('grade'),
        'memo': request.args.get('memo'),
        'page': request.args.get('page', 1, type=int)
    }

    query = db.session.query(Song)

    # 動的にフィルタを追加
    if search_params['song']:
        query = query.filter(Song.song_name.contains(search_params['song']))
        
    if search_params['book']:
        query = query.join(Book).filter(Book.book_name.contains(search_params['book'])).options(contains_eager(Song.parent_book))
    if search_params['artist']:
        query = query.join(Song.artists).filter(Artist.Artist_name.contains(search_params['artist'])).options(contains_eager(Song.artists))
    if search_params['lyricist']:
        query = query.join(Song.lyricists).filter(Lyricist.lyricist_name.contains(search_params['lyricist'])).options(contains_eager(Song.lyricists))
    if search_params['song_writer']:
        query = query.join(Song.song_writers).filter(SongWriter.song_writer_name.contains(search_params['song_writer'])).options(contains_eager(Song.song_writers))
    if search_params['arranger']:
        query = query.join(Song.arrangers).filter(Arranger.arranger_name.contains(search_params['arranger'])).options(contains_eager(Song.arrangers))
    if search_params['grade']:
        query = query.filter(Song.grade == search_params['grade'])
    if search_params['memo']:
        query = query.filter(Song.memo.like(f"%{search_params['memo']}%"))

    # クエリの結果を取得
    results = query.order_by(Song.song_name).paginate(page=search_params['page'], per_page=ppage, error_out=False)

    return render_template('Pages/searched_song_advanced.html',songs = results,que = search_params,page=search_params['page'])


@app.route("/book/<int:id>")
def bookinfo(id):
  bookid = id
  songs = db.session.query(Song).filter(Song.book_id == bookid).all()
  bookname = db.session.query(Book).get(bookid)
  return render_template('Pages/book.html',songs = songs,book = bookname)
