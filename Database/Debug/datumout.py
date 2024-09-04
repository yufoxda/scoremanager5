from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from Schema.schema import Book, Song, Author, PublishURL

# エンジンを作成
engine = create_engine('sqlite:///ompuscores.db')

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

try:
    # 書籍のクエリ例
    # books = session.query(Book).all()
    # for book in books:
    #     print(f"Book ID: {book.id}, Book Name: {book.book_name}")

    # 曲のクエリ例
    # songs = session.query(Song).all()
    # for song in songs:
    #     print(f"Song ID: {song.id}, Song Name: {song.song_name}, Book ID: {song.book_id}")

    # # 著者のクエリ例
    # authors = session.query(Author).all()
    # for author in authors:
    #     print(f"Author ID: {author.id}, Author Name: {author.author_name}, Song ID: {author.song_id}")

    # # 公開URLのクエリ例
    # publish_urls = session.query(PublishURL).all()
    # for publish_url in publish_urls:
    #     print(f"Publish URL ID: {publish_url.id}, URL: {publish_url.url}, Song ID: {publish_url.song_id}")

    books = session.query(Book).all()
    for i in books:
        try:
            print(i.product_code.strip())
        except:
            continue
        
except Exception as e:
    print(f"Error occurred: {e}")

finally:
    session.close()  # セッションをクローズしてリソースを解放
