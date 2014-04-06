from flask import Flask, request
from random import choice
import string
import dbm

app = Flask(__name__)

@app.route('/')
def hello_world():
    response = """
<form method="POST" action="/generate">
<input type=text name=title placeholder="Your link" /> <br>
<input type=submit value=submit />
</form>
"""
    return response

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        link = request.form['title']
    else:
        return "error"
    allowed_letters = string.ascii_letters + string.digits

    db = dbm.open("links.db",'c')
    new_link = ""
    while True:
        for i in range(8):
            new_link = new_link + choice(allowed_letters)
        if new_link not in db.keys():
            break
    db[new_link] = link

    return ("Your old link: {0} <br>New link: {1}").format(link,new_link)

@app.route('/<link>')
def redirect(link):
    db = dbm.open("links.db", 'r')
    try:
        site = db[link]
    except:
        return "Error! No long links"
    return '<meta http-equiv="refresh" content="0; url={}">'.format(site)

if __name__ == '__main__':
    app.run()
