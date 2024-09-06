import requests
from bs4 import BeautifulSoup
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from ..Schema.schema import Book, Song, Lyricist, SongWriter, Arranger

from ..Schema.schema import SongLyricistAssociation,SongWriterAssociation,SongArrangerAssociation



engine = create_engine('sqlite:///Database/ompooscores.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def get_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def split_composer_data(data):
    # 複数の区切り文字に対応する関数
    delimiters = ['/', '、', 'と', '・']
    for delimiter in delimiters:
        if delimiter in data:
            return [name.strip() for name in data.split(delimiter)]
    return [data.strip()]

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    tracks = []

    # 収録曲数を取得
    num_tracks_element = soup.select_one('span[itemprop="numTracks"]')
    num_tracks = int(num_tracks_element.text.strip()) if num_tracks_element else 0

    # 各曲の情報を抽出
    for track in soup.select('tr[itemprop="track"]'):
        # 曲名を取得
        song_name = track.select_one('.main a span[itemprop="name"]').text.strip()
        artist = ""
        try:
            artist = (track.find('a', {'itemprop': 'byArtist'}).text.strip())
        except:
            artist = "none"
        # 主題歌や追加情報を取得
        additional_info_element = track.select_one('.main')
        print(list(additional_info_element.stripped_strings))
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
                lyricist = text
            elif(fase == 2):
                composer = text
            

        # グレードを取得
        grade_element = track.select_one('.sub')
        grade = "N/A"
        if grade_element:
            for text in grade_element.stripped_strings:
                if "グレード：" in text:
                    grade = text.split("グレード：")[1].strip()
                    break

        tracks.append({
            '曲名': song_name,
            'メモ': additional_info,
            'アーティスト':list(artist.split('/')),
            '作詞者': list(lyricist.split('/')),
            '作曲者': list(composer.split('/')),
            '編曲者': list(arranger.split('/')),
            'グレード': grade.replace("級","")
        })

    return num_tracks, tracks

def main():
    base_url = 'https://www.ymm.co.jp/p/detail.php?code=GTM01101878&dm=d&o='
    all_tracks = []
    page_offset = 0

    while True:
        url = f"{base_url}{page_offset}"
        print(f"Fetching page with offset {page_offset}...")
        html = get_page(url)
        num_tracks, new_tracks = parse_html(html)

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

    

if __name__ == '__main__':
    main()
