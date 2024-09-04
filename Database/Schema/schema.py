from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# エンジンを作成
engine = create_engine('sqlite:///Database/ompuscores.db', echo=True)

# ベースクラスを定義
Base = declarative_base()

# テーブル定義
# 楽譜集
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, unique=True)
    book_name = Column(String)
    product_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    songs = relationship('Song', back_populates='parent_book')

# 曲名
class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, unique=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    song_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    grade = Column(String,  nullable=True)
    memo = Column(String,  nullable=True)

    parent_book = relationship('Book', back_populates='songs')
    lyricists = relationship('Lyricist', secondary='song_lyricist_association', back_populates='songs')
    song_writers = relationship('SongWriter', secondary='song_writer_association', back_populates='songs')
    arrangers = relationship('Arranger', secondary='song_arranger_association', back_populates='songs')

# 作詞家
class Lyricist(Base):
    __tablename__ = 'lyricists'
    id = Column(Integer, primary_key=True, unique=True)
    lyricist_name = Column(String, nullable=False)

    songs = relationship('Song', secondary='song_lyricist_association', back_populates='lyricists')

# 作曲家
class SongWriter(Base):
    __tablename__ = 'songwriters'
    id = Column(Integer, primary_key=True, unique=True)
    song_writer_name = Column(String, nullable=False)

    songs = relationship('Song', secondary='song_writer_association', back_populates='song_writers')

# 編曲家
class Arranger(Base):
    __tablename__ = 'arrangers'
    id = Column(Integer, primary_key=True, unique=True)
    arranger_name = Column(String, nullable=False)

    songs = relationship('Song', secondary='song_arranger_association', back_populates='arrangers')

# 中間テーブル
class SongLyricistAssociation(Base):
    __tablename__ = 'song_lyricist_association'
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    lyricist_id = Column(Integer, ForeignKey('lyricists.id'), primary_key=True)

class SongWriterAssociation(Base):
    __tablename__ = 'song_writer_association'
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    song_writer_id = Column(Integer, ForeignKey('songwriters.id'), primary_key=True)

class SongArrangerAssociation(Base):
    __tablename__ = 'song_arranger_association'
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    arranger_id = Column(Integer, ForeignKey('arrangers.id'), primary_key=True)
