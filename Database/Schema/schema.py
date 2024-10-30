from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint

# エンジンを作成
engine = create_engine("sqlite:///Database/ompooscores.db", echo=True)

# ベースクラスを定義
Base = declarative_base()


# テーブル定義
# 楽譜集
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, unique=True)
    book_name = Column(String)
    product_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    songs = relationship("Song", back_populates="parent_book")


# 曲名
class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, unique=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=True)
    song_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    grade = Column(String, nullable=True)
    memo = Column(String, nullable=True)

    parent_book = relationship("Book", back_populates="songs")
    artists = relationship(
        "Artist", secondary="song_artist_association", back_populates="songs"
    )
    lyricists = relationship(
        "Lyricist", secondary="song_lyricist_association", back_populates="songs"
    )
    song_writers = relationship(
        "SongWriter", secondary="song_writer_association", back_populates="songs"
    )
    arrangers = relationship(
        "Arranger", secondary="song_arranger_association", back_populates="songs"
    )


class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, unique=True)
    Artist_name = Column(String, nullable=False)

    songs = relationship(
        "Song", secondary="song_artist_association", back_populates="artists"
    )


# 作詞家
class Lyricist(Base):
    __tablename__ = "lyricists"
    id = Column(Integer, primary_key=True, unique=True)
    lyricist_name = Column(String, nullable=False)

    songs = relationship(
        "Song", secondary="song_lyricist_association", back_populates="lyricists"
    )


# 作曲家
class SongWriter(Base):
    __tablename__ = "songwriters"
    id = Column(Integer, primary_key=True, unique=True)
    song_writer_name = Column(String, nullable=False)

    songs = relationship(
        "Song", secondary="song_writer_association", back_populates="song_writers"
    )


# 編曲家
class Arranger(Base):
    __tablename__ = "arrangers"
    id = Column(Integer, primary_key=True, unique=True)
    arranger_name = Column(String, nullable=False)

    songs = relationship(
        "Song", secondary="song_arranger_association", back_populates="arrangers"
    )


# 中間テーブル for Song-Lyricist
class SongLyricistAssociation(Base):
    __tablename__ = "song_lyricist_association"
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    lyricist_id = Column(Integer, ForeignKey("lyricists.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("song_id", "lyricist_id"),)


# 中間テーブル for Song-Writer
class SongWriterAssociation(Base):
    __tablename__ = "song_writer_association"
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    song_writer_id = Column(Integer, ForeignKey("songwriters.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("song_id", "song_writer_id"),)


# 中間テーブル for Song-Arranger
class SongArrangerAssociation(Base):
    __tablename__ = "song_arranger_association"
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    arranger_id = Column(Integer, ForeignKey("arrangers.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("song_id", "arranger_id"),)


class SongArtistAssociation(Base):
    __tablename__ = "song_artist_association"
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("song_id", "artist_id"),)
