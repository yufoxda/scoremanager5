from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database.Schema.schema import Song

# エンジンを作成
engine = create_engine('sqlite:///Database/ompooscores.db', echo=True)

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Songテーブルのすべてのデータを取得
    songs = session.query(Song).all()

    for song in songs:
        if song.memo:  # memoがNoneでないことを確認
            # 空白を削除して更新
            new_memo = song.memo.replace(" ", "")  # 空白を削除
            if new_memo != song.memo:  # 変更があった場合
                song.memo = new_memo
                print(f"Updated song ID: {song.id}, New memo: {new_memo}")

    # 変更をコミット
    session.commit()

except Exception as e:
    print(f"Error occurred: {e}")
    session.rollback()  # エラー発生時はロールバック

finally:
    # セッションをクローズしてリソースを解放
    session.close()
