# scoremanager5

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

## db-init
```
python -m Database.database_init_
```
## db-register
```
python -m Database.Register.register_bytext
```
Database/Register/datum/lists.textに記載されている商品コードに含まれる楽譜を登録します。
エラーが出る場合は手動登録。