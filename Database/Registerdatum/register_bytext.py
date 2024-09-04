import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

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

        # 主題歌や追加情報を取得
        additional_info_element = track.select_one('.main')
        additional_info = ""
        for text in additional_info_element.stripped_strings:
            if text not in song_name:
                additional_info += text + " "
        additional_info = additional_info.strip()

        # 作詞者を取得
        lyricist_element = track.find(string="作詞：")
        lyricist = lyricist_element.find_next('a').text.strip() if lyricist_element else "N/A"

        # 作曲者を取得
        composer_element = track.find(string="作曲：")
        composer = composer_element.find_next('a').text.strip() if composer_element else "N/A"

        # 編曲者を取得
        arranger_element = track.find(string="編曲：")
        arranger = arranger_element.find_next(string=True).strip() if arranger_element else "N/A"

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
            '作詞者': lyricist,
            '作曲者': composer,
            '編曲者': arranger,
            'グレード': grade
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
        print(f"曲名: {track['曲名']}, メモ: {track['メモ']}, 作詞者: {track['作詞者']}, 作曲者: {track['作曲者']}, 編曲者: {track['編曲者']}, グレード: {track['グレード']}")

if __name__ == '__main__':
    main()
