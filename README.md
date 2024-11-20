# scoremanager
TUAT electoneサークル用　楽譜マネージャー：楽譜館\
部室所蔵の楽譜が載っている本の検索と、そこに掲載されている楽譜が検索できます。

# stack
flamework flask\
css tailwind\
db sqlite

## tailwind
```
npm install -D tailwindcss
npx tailwindcss init
npx tailwindcss -i ./Src/Static/input.css -o ./Src/Static/output.css --watch
```
## flask
```
flask run --debug 
```

## db
スキーマ
```./Database/Schema/schema.py```

初回登録
```
python -m Database.database_init_
python -m Database.Register.register_bytext
```
Database/Register/datum/lists.textに記載されている商品コードに含まれる楽譜を登録します。
エラーが出る場合は手動登録。
```./Database/Register/register_bycsv.py```、```./Database/Register/register_special_book.py```を参考に適宜変更して登録。


## debug 
全出力
```
python -m Database.Debug.printput
```
