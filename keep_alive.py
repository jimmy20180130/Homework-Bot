from flask import Flask, request, send_file
from threading import Thread
import requests
import time
import base64
from io import BytesIO

app = Flask('')


@app.route('/')
def main():
  return 'Bot is aLive!'

def run():
  app.run(host="0.0.0.0", port=8080)


def send_request():
  while True:
    url = 'https://alivesrfewsdfcdrwerfdwe.jimmy20180130.repl.co'
    # 发送GET请求到指定的URL
    response = requests.get(url)

    # 打印响应内容和状态码
    print(f"網站 {url} : {response.status_code}")

    # 等待60秒再次发送请求
    time.sleep(60)


def keep_alive():
  server = Thread(target=run)
  request_thread = Thread(target=send_request)
  server.start()
  request_thread.start()


if __name__ == '__main__':
  keep_alive()