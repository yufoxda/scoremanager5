import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.Schema.schema import (
    Book, Song, Lyricist, SongWriter, Arranger, Artist
)

# エンジンを作成 (既存の設定を維持)
engine = create_engine('sqlite:///Database/ompooscores.db', echo=True)

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

# データ格納用の辞書
data = {
    "books": [],
    "songs": [],
    "artists": [],
    "lyricists": [],
    "song_writers": [],
    "arrangers": []
}

try:
    # 1. Books
    books = session.query(Book).all()
    for book in books:
        data["books"].append({
            "id": book.id,
            "book_name": book.book_name,
            "product_code": book.product_code,
            # created_at は datetime オブジェクトなので文字列に変換
            "created_at": book.created_at.isoformat() if book.created_at else None
        })
    
    # 2. Artists
    artists = session.query(Artist).all()
    for artist in artists:
        data["artists"].append({
            "id": artist.id,
            "Artist_name": artist.Artist_name
        })

    # 3. Lyricists
    lyricists = session.query(Lyricist).all()
    for lyricist in lyricists:
        data["lyricists"].append({
            "id": lyricist.id,
            "lyricist_name": lyricist.lyricist_name
        })

    # 4. SongWriters
    song_writers = session.query(SongWriter).all()
    for writer in song_writers:
        data["song_writers"].append({
            "id": writer.id,
            "song_writer_name": writer.song_writer_name
        })

    # 5. Arrangers
    arrangers = session.query(Arranger).all()
    for arranger in arrangers:
        data["arrangers"].append({
            "id": arranger.id,
            "arranger_name": arranger.arranger_name
        })

    # 6. Songs (with relationships)
    songs = session.query(Song).all()
    for song in songs:
        data["songs"].append({
            "id": song.id,
            "song_name": song.song_name,
            "book_id": song.book_id,
            "grade": song.grade,
            "memo": song.memo,
            "created_at": song.created_at.isoformat() if song.created_at else None,
            # 多対多のリレーションシップIDを取得
            "artist_ids": [a.id for a in song.artists],
            "lyricist_ids": [l.id for l in song.lyricists],
            "song_writer_ids": [sw.id for sw in song.song_writers],
            "arranger_ids": [ar.id for ar in song.arrangers]
        })

    # JSONファイルとして出力
    output_path = "Database/Debug/output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"データの書き込みが完了しました: {output_path}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    session.close()