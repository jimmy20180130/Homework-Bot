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
  

def keep_alive():
  server = Thread(target=run)
  server.start()


if __name__ == '__main__':
  keep_alive()