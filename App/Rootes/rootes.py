from App.app_init_ import app,db,per_page
from App.app_init_ import Book, Song,Artist,Lyricist,SongWriter,Arranger
from flask import render_template, request, url_for,jsonify
from flask_sqlalchemy import pagination 
from sqlalchemy.orm import joinedload

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



@app.route("/advancedsearch", methods=["POST"])
def advancedsearch():
    # request.form から各データを取得
    artist = request.form.get('artist')
    lyricist = request.form.get('lyricist')
    song_writer = request.form.get('songWriter')
    arranger = request.form.get('arranger')
    grade = request.form.get('grade')
    memo = request.form.get('memo')

    # クエリの初期化
    query = db.session.query(Song).options(
        joinedload(Song.artists),
        joinedload(Song.lyricists),
        joinedload(Song.song_writers),
        joinedload(Song.arrangers)
    )
    
    # 各条件に応じてフィルタを適用
    if artist:
        query = query.join(Song.artists).filter(Artist.Artist_name.contains(artist))
    if lyricist:
        query = query.join(Song.lyricists).filter(Lyricist.lyricist_name.contains(lyricist))
    if song_writer:
        query = query.join(Song.song_writers).filter(SongWriter.song_writer_name.contains(song_writer))
    if arranger:
        query = query.join(Song.arrangers).filter(Arranger.arranger_name.contains(arranger))
    if grade:
        query = query.filter(Song.grade == grade)
    if memo:
        query = query.filter(Song.memo.like(f"%{memo}%"))  # memoを部分一致で検索

    # 結果を取得
    songs = query.all()

    # 結果がない場合の処理
    if not songs:
        return jsonify({"message": "No songs found matching the criteria."}), 404

    # 曲の情報をリストに変換
    result = []
    for song in songs:
        result.append({
            "id": song.id,
            "song_name": song.song_name,
            "grade": song.grade,
            "memo": song.memo,
            "created_at": song.created_at,
            "artists": [artist.Artist_name for artist in song.artists],
            "lyricists": [lyricist.lyricist_name for lyricist in song.lyricists],
            "song_writers": [song_writer.song_writer_name for song_writer in song.song_writers],
            "arrangers": [arranger.arranger_name for arranger in song.arrangers],
        })

    # 有効なデータをJSONで返す
    return jsonify(result), 200


@app.route("/book/<int:id>")
def bookinfo(id):
  bookid = id
  songs = db.session.query(Song).filter(Song.book_id == bookid).all()
  bookname = db.session.query(Book).get(bookid)
  return render_template('Pages/book.html',songs = songs,book = bookname)
