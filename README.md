gmail_sender
====

gmailアカウントからメールを送信します。
送信先のリストを参照して、個別にメールを作成します。

## 必要環境
- 本リポジトリ
    インストールというかダウンロードしていただければよいです。
    `Clone　or　Download`　から　`Download　ZIP`　でダウンロードしてください。
    お好みの場所で展開すればOKです。

- python
    インストールされていない場合は入れてください。
    なにそれ？と思った場合はおそらく入ってないです。
    linux使ってる人には説明は不要ですね。

    インストールはこちら↓  
    [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

    - windows(64bit)の場合  
    "Download Windows x86-64 executable installer"

    - windows(32bit)の場合  
    "Download Windows x86 executable installer"

    をダウンロードして、インストールしてくださいね。

## 使い方
1. mailsettings.txt に 宛先等を記入してください。
    bccなど、使用しない場合は空欄にしてください。
    行番号が変わらないようにご注意ください。

1. mailbody.txt に メール本文を記入してください。
    本文は４行目以降に記入してください。
    宛先は ##TO_NAME## と記入することで、
    sendlist.csv に記載された名前に置換されます。

1. attachment.txt に 添付ファイルの場所を記入してください。
    添付しない場合は"none"と記入してください。

1. sendlist.csv に 送信先情報を記入してください。
    ただし次の点に注意してください。

    - １行目は見出し。送付先リストは２行目以降。
    - １列目に送付先名。これはメール冒頭のに 「〇〇様」 に使用されます。
    - ２列目に送付先メールアドレス。
    - ３列目に送信"する"または"しない"を記入してください。
        ”する"以外が記入されている場合は送信処理がスキップされます。

1. gmail_sender.py を実行してください。
    gmailのパスワードを聞かれるので、入力してください。
    認証が通ればメールが送信されます。
    送信の成否が log.csv に出力されます。

## License

MIT License

## Author

[shka86](https://github.com/shka86)
