from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen, Request
import requests
from flask_cors import CORS
ssl._create_default_https_context = ssl._create_unverified_context

# SSLContext 생성하여 DH 키 크기 문제 해결
ctx = ssl.create_default_context()
ctx.set_ciphers("DEFAULT@SECLEVEL=1")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_number", methods=["POST"])
def get_number():
    #search = str(request.form["number"])
    search = request.get_json()["number"]
    print(search)
    url = 'https://www.yes24.com/Product/Search?domain=ALL&query=' + search.replace(' ', '%20')
    response = requests.get(url)
    html_data = response.text
    #response = urlopen(url, context=ctx)
    soup = BeautifulSoup(html_data, 'html.parser')
    item_info = soup.select('#yesSchList > li > div > div.item_img > div.img_canvas > span > span > a > em > img')
    p = str(item_info[0]).replace('"',',').split(',')
    print(p[1])
    print(p[7])
    prize_1 = soup.select('#yesSchList > li:nth-child(1) > div > div.item_info > div.info_row.info_price > strong > em')
    
    return jsonify({"result": p[7]})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
