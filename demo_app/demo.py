from flask import Flask # Flaskモジュールをインポート

app = Flask(__name__) # Flaskアプリのインスタンス生成

@app.route("/")            # URLのパス
def hello():               # ”/” にアクセスされたときに実行される関数
    return "Hello World! "  # テキストを返却

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) # ビルドインサーバー起動


