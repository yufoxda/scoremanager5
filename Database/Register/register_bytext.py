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

ignoresplitlist = ["DISH//"]

def get_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def splitartist(texts):
    thistext = texts
    retrunlists = []
    for edgename in ignoresplitlist:
        if edgename in thistext:
            retrunlists.append(edgename)
            thistext = thistext.replace(edgename,"")
            
    if(not thistext == ""):
        retrunlists += list(thistext.split('/'))
    return retrunlists


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    tracks = []

    # 収録曲数を取得
    num_tracks_element = soup.select_one('span[itemprop="numTracks"]')
    num_tracks = int(num_tracks_element.text.strip()) if num_tracks_element else 0
    
    name = soup.find('span',itemprop="name")
    bookname = re.sub(r"\s", "", name.get_text())
    print(bookname)
    # 各曲の情報を抽出
    for track in soup.select('tr[itemprop="track"]'):
        # 曲名を取得
        song_name = track.select_one('.main a span[itemprop="name"]').text.strip()
        artist = ""
        try:
            artist = (track.find('a', {'itemprop': 'byArtist'}).text.strip())
        except BaseException:
            artist = "none"
        # 主題歌や追加情報を取得
        additional_info_element = track.select_one('.main')
        #print(list(additional_info_element.stripped_strings))
        additional_info = []
        lyricist= "none"
        composer = "none"
        arranger= "none"
        
        fase = 0
        for text in additional_info_element.stripped_strings:
            if text in song_name or (fase == 0 and text in artist) :
                continue
            if(text == '作詞：'):
                fase = 1
                continue
            if(text == '作曲：'):
                fase = 2
                continue
            if(not text.find('編曲：') == -1):
                arranger = text.replace('編曲：','')
            elif(fase == 0):
                additional_info.append(text)
            elif(fase == 1):
                lyricist = text.strip()
            elif(fase == 2):
                composer = text.strip()
            

        # グレードを取得
        grade_element = track.select_one('.sub')
        grade = "none"
        if grade_element:
            for text in grade_element.stripped_strings:
                if "グレード：" in text:
                    grade = text.split("グレード：")[1].strip()
                    break
        
        

        tracks.append({
            '曲名': song_name,
            'メモ': additional_info,
            'アーティスト':splitartist(artist),
            '作詞者': list(lyricist.split('/')),
            '作曲者': list(composer.split('/')),
            '編曲者': list(arranger.split('/')),
            'グレード': grade.replace("級","")
        })

    return num_tracks, tracks,bookname

def main(code):

    existcode = session.query(Book).filter_by(product_code = code).first()
    if existcode:
        return

    base_url = 'https://www.ymm.co.jp/p/detail.php?code='+code+'&dm=d&o='
    all_tracks = []
    page_offset = 0

    while True:
        url = f"{base_url}{page_offset}"
        print(f"Fetching page with offset {page_offset}...")
        html = get_page(url)
        num_tracks, new_tracks,bookname = parse_html(html)

        if not new_tracks:
            break

        all_tracks.extend(new_tracks)
        page_offset += 10

        # 最後のページで「次へ」ボタンが非表示の場合にループを終了
        if len(new_tracks) < 10:
            break

    # 総収録曲数を表示
    print(f"総収録曲数: {num_tracks}曲")
    
    

    # 抽出した曲の情報を表示
    for track in all_tracks:
        print(track['曲名'],track['メモ'],track['アーティスト'], track['作詞者'], track['作曲者'], track['編曲者'],track['グレード'])

    print("------------")
    # 楽譜集を作成
    new_book = Book(book_name=bookname, product_code=code, created_at=datetime.now())
    session.add(new_book)
    session.flush()

    for track in all_tracks:
        memos = ""
        for i in track['メモ']:
            memos += (" " + i)

        # 新しい曲を作成
        new_song = Song(
            book_id=new_book.id,
            song_name=track['曲名'],
            grade=track['グレード'],
            memo=memos,
            created_at=datetime.now()
        )

        if track['アーティスト'] is not None:
            # アーティストを曲に関連付け
            for i in track['アーティスト']:
                existing_artist = session.query(Artist).filter_by(Artist_name=i.strip()).first()
                if existing_artist:
                    print(f"アーティスト '{i}' が存在します")
                    new_song.artists.append(existing_artist)
                else:
                    new_artist = Artist(Artist_name=i.strip())
                    session.add(new_artist)  # セッションに追加
                    new_song.artists.append(new_artist)

        # 作詞家を曲に関連付け
        for i in track['作詞者']:
            existing_lyricist = session.query(Lyricist).filter_by(lyricist_name=i.strip()).first()
            if existing_lyricist:
                print(f"作詞家 '{i}' が存在します")
                new_song.lyricists.append(existing_lyricist)
            else:
                new_lyricist = Lyricist(lyricist_name=i.strip())
                session.add(new_lyricist)  # セッションに追加
                new_song.lyricists.append(new_lyricist)

        # 作曲家を曲に関連付け
        for i in track['作曲者']:
            existing_writer = session.query(SongWriter).filter_by(song_writer_name=i.strip()).first()
            if existing_writer:
                print(f"作曲家 '{i}' が存在します")
                new_song.song_writers.append(existing_writer)
            else:
                new_writer = SongWriter(song_writer_name=i.strip())
                session.add(new_writer)  # セッションに追加
                new_song.song_writers.append(new_writer)

        # 編曲家を曲に関連付け
        for i in track['編曲者']:
            existing_arranger = session.query(Arranger).filter_by(arranger_name=i.strip()).first()
            if existing_arranger:
                print(f"編曲家 '{i}' が存在します")
                new_song.arrangers.append(existing_arranger)
            else:
                new_arranger = Arranger(arranger_name=i.strip())
                session.add(new_arranger)  # セッションに追加
                new_song.arrangers.append(new_arranger)


        # 曲をセッションに追加
        session.add(new_song)

    # セッションをコミットしてデータベースに保存
    session.commit()

    print("データベースに楽譜集と曲を保存しました。")

    

if __name__ == '__main__':
    filename = "Database/Register/datum/lists.text"
    f = open(filename, 'r')

    datalist = f.readlines()
    for i in datalist:
        print(i)
        main(i.strip())
