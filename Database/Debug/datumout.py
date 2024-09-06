from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from Database.Schema.schema import (
    Book, Song, Lyricist, SongWriter, Arranger,Artist,
    SongLyricistAssociation, SongWriterAssociation, 
    SongArrangerAssociation, SongArtistAssociation
)

# エンジンを作成
engine = create_engine('sqlite:///Database/ompooscores.db', echo=True)

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Bookテーブルのデータを取得
    books = session.query(Book).all()
    print("Books:")
    for book in books:
        print(f"ID: {book.id}, Name: {book.book_name}, Product Code: {book.product_code}")
    
    # Songテーブルのデータを取得
    songs = session.query(Song).all()
    print("\nSongs:")
    for song in songs:
        print(f"ID: {song.id}, Name: {song.song_name}, Book ID: {song.book_id},memo:{song.memo},grade:{song.grade}")
    
    # Artistテーブルのデータを取得
    artists = session.query(Artist).all()
    print("\nArtists:")
    for artist in artists:
        print(f"ID: {artist.id}, Name: {artist.Artist_name}")
    
    # Lyricistテーブルのデータを取得
    lyricists = session.query(Lyricist).all()
    print("\nLyricists:")
    for lyricist in lyricists:
        print(f"ID: {lyricist.id}, Name: {lyricist.lyricist_name}")
    
    # SongWriterテーブルのデータを取得
    song_writers = session.query(SongWriter).all()
    print("\nSong Writers:")
    for writer in song_writers:
        print(f"ID: {writer.id}, Name: {writer.song_writer_name}")
    
    # Arrangerテーブルのデータを取得
    arrangers = session.query(Arranger).all()
    print("\nArrangers:")
    for arranger in arrangers:
        print(f"ID: {arranger.id}, Name: {arranger.arranger_name}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # セッションをクローズしてリソースを解放
    session.close()
