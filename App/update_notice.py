# Database/Register/register_bytext.pyにて呼び出し
# githubactionで上記を実行

import json
def update(date, content, end_txt):
    json_open = open('Src/Static/notice.json',encoding="utf-8")
    notice_data = json.load(json_open)

    print(notice_data.pop())

    notice_data.insert(0,
        {
            "date": date,
            "content": content,
            "end_txt": end_txt
        }
    )
    print(notice_data)
    with open('Src/Static/notice.json', 'w', encoding="utf-8") as f:
        json.dump(notice_data, f, ensure_ascii=False, indent=4)
