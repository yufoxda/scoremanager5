import requests
from bs4 import BeautifulSoup
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from ..Schema.schema import Book, Song, Lyricist, SongWriter, Arranger,Artist
from ..Schema.schema import SongLyricistAssociation,SongWriterAssociation,SongArtistAssociation

import csv


engine = create_engine('sqlite:///Database/ompooscores.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


f =  open('./Database/Register/datum/songs.csv',encoding='utf-8')
# readerでCSVファイルとして呼び出す
reader = csv.reader(f)
bookname = ""
booknum = ""
# reader: 2次元配列
for row in reader:
    if(row[0] != '' ):
        bookname = row[0]
        new_book = Book(
            book_name=bookname, product_code=row[1] if(row[1]) else "none", created_at=datetime.now()
        )
        session.add(new_book)
        session.flush()
        booknum = new_book.id
        continue
    new_song = Song(
        book_id=booknum,
        song_name=row[1],
        memo= row[2] if row[2] else '',
        grade=row[5],
        created_at=datetime.now()
    )

    songwriters = list(row[2].split(","))
    for sw in songwriters:
        existing_writer = session.query(SongWriter).filter_by(song_writer_name=sw).first()
        if existing_writer:
            print("作曲家存在します")
            new_song.song_writers.append(existing_writer)
        else:
            new_writer = SongWriter(song_writer_name=sw)
            session.add(new_writer)  # セッションに追加
            new_song.song_writers.append(new_writer)

    # 編曲家を曲に関連付け
    arenger = row[4]
    existing_arranger = session.query(Arranger).filter_by(arranger_name=arenger).first()
    if existing_arranger:
        print("編曲家が存在します")
        new_song.arrangers.append(existing_arranger)
    else:
        new_arranger = Arranger(arranger_name=arenger)
        session.add(new_arranger)  # セッションに追加
        new_song.arrangers.append(new_arranger)
    session.commit()
    
    