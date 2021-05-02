# https://static.mercdn.net/item/detail/orig/photos/m37136174729_1.jpg?1619894209
import requests

def save_image(filename, image):
        # ファイルをローカルに保存
        with open(filename, "wb") as file:
            file.write(image)

def download_image(url):
        # リクエストを投げる
        response = requests.get(url, timeout=100)
        # ステータスコードがエラー
        if response.status_code != 200:
            raise RuntimeError("取得失敗")
        content_type = response.headers["content-type"]
        # 画像ではない
        if 'image' not in content_type:
            raise RuntimeError("画像ではありません")
        return response.content

image = download_image("https://static.mercdn.net/item/detail/orig/photos/m37136174729_1.jpg?1619894209")
save_image("C:\\Users\\motoi\\Downloads\\test.jpg", image)