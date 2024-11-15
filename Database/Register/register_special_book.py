import requests
from bs4 import BeautifulSoup
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from ..Schema.schema import Book, Song, Lyricist, SongWriter, Arranger,Artist
from ..Schema.schema import SongLyricistAssociation,SongWriterAssociation,SongArtistAssociation



engine = create_engine('sqlite:///Database/ompooscores.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def addbook_first_song():
    new_book = Book(
        book_name="モーニング娘。", product_code="GTE643730", created_at=datetime.now()
    )
    session.add(new_book)
    session.flush()
    new_song = Song(
            book_id=new_book.id,
            song_name="モーニングコーヒー",
            grade="7",
            created_at=datetime.now()
        )
    
    sw = "つんく"
    ar = "渡部 薫"
    
    existing_artist = session.query(Artist).filter_by(Artist_name="モーニング娘。").first()
    if existing_artist:
        new_song.artists.append(existing_artist)
    else:
        new_artist = Artist(Artist_name="モーニング娘。")
        session.add(new_artist)  # セッションに追加
        new_song.artists.append(new_artist)

# 作詞家を曲に関連付け
    existing_lyricist = session.query(Lyricist).filter_by(lyricist_name=sw).first()
    if existing_lyricist:
        print("作詞家が存在します")
        new_song.lyricists.append(existing_lyricist)
    else:
        new_lyricist = Lyricist(lyricist_name=sw)
        session.add(new_lyricist)  # セッションに追加
        new_song.lyricists.append(new_lyricist)

        # 作曲家を曲に関連付け
 


    existing_writer = session.query(SongWriter).filter_by(song_writer_name=sw).first()
    if existing_writer:
        print("作曲家存在します")
        new_song.song_writers.append(existing_writer)
    else:
        new_writer = SongWriter(song_writer_name=sw)
        session.add(new_writer)  # セッションに追加
        new_song.song_writers.append(new_writer)

    # 編曲家を曲に関連付け
    existing_arranger = session.query(Arranger).filter_by(arranger_name=ar).first()
    if existing_arranger:
        print("編曲家が存在します")
        new_song.arrangers.append(existing_arranger)
    else:
        new_arranger = Arranger(arranger_name=ar)
        session.add(new_arranger)  # セッションに追加
        new_song.arrangers.append(new_arranger)


    # 曲をセッションに追加
    session.add(new_song)
    session.commit()
    add_song(new_book.id,"サマーナイトタウン",sw,"斉藤 純代","7")
    add_song(new_book.id,"Ｍｅｍｏｒｙ青春の光",sw,"松下 美千代","7")
    add_song(new_book.id,"真夏の光線",sw,"和鳴 敦子","6")
    add_song(new_book.id,"抱いてＨＯＬＤ ＯＮ ＭＥ！",sw,"上野 みゆき",6)
    add_song(new_book.id,"ＬＯＶＥマシーン",sw,"斉藤 純代","7")
    add_song(new_book.id,"恋のダンスサイト",sw,"杉本 豊之","6")
    return

def add_song(bookid,song,songw,arenge,grade):
    new_song = Song(
            book_id=bookid,
            song_name=song,
            grade=grade,
            created_at=datetime.now()
        )
    
    existing_artist = session.query(Artist).filter_by(Artist_name="モーニング娘。").first()
    if existing_artist:
        new_song.artists.append(existing_artist)
    else:
        new_artist = Artist(Artist_name="モーニング娘。")
        session.add(new_artist)  # セッションに追加
        new_song.artists.append(new_artist)

    existing_lyricist = session.query(Lyricist).filter_by(lyricist_name=songw).first()
    if existing_lyricist:
        print("作詞家が存在します")
        new_song.lyricists.append(existing_lyricist)
    else:
        new_lyricist = Lyricist(lyricist_name=songw)
        session.add(new_lyricist)  # セッションに追加
        new_song.lyricists.append(new_lyricist)

        # 作曲家を曲に関連付け
    existing_writer = session.query(SongWriter).filter_by(song_writer_name=songw).first()
    if existing_writer:
        print("作曲家が存在します")
        new_song.song_writers.append(existing_writer)
    else:
        new_writer = SongWriter(song_writer_name=songw)
        session.add(new_writer)  # セッションに追加
        new_song.song_writers.append(new_writer)

    # 編曲家を曲に関連付け
    existing_arranger = session.query(Arranger).filter_by(arranger_name=arenge).first()
    if existing_arranger:
        print("編曲家が存在します")
        new_song.arrangers.append(existing_arranger)
    else:
        new_arranger = Arranger(arranger_name=songw)
        session.add(new_arranger)  # セッションに追加
        new_song.arrangers.append(new_arranger)
    session.add(new_song)
    session.commit()
    

if __name__ == '__main__':
    addbook_first_song()