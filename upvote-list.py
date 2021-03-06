from flask import Flask, request, redirect, render_template
from collections import defaultdict
import pickle

app = Flask(__name__)
app.debug = True

i = 0
items = defaultdict(dict)
users = defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html', 
                           items=items, 
                           users=users, 
                           user_id=request.remote_addr)

@app.route('/create/', methods=['POST'])
def create():
    global i
    items[i] = {
        'text': request.form['text'], 
        'votes': 0,
        'owner': request.remote_addr
    }
    id = i
    i += 1
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    if items[id]['owner'] != request.remote_addr:
        return "You can only delete your own posts."
    if id in items:
        del items[id]
    else:
        return 'Unknown ID.'
    return redirect('/')

@app.route('/vote/<int:id>/<type>')
def upvote(id, type):
    user_id = request.remote_addr
    if id not in items:
        return 'Unknown ID.'
    if type == 'up':
        if id in users[user_id]:
            return "You can't vote twice."
        items[id]['votes'] += 1
        users[user_id].append(id)
    elif type == 'down':
        if id not in users[user_id]:
            return "You can't downvote this topic."
        items[id]['votes'] -= 1
        users[user_id].remove(id)
    return redirect('/')

if __name__ == "__main__":
    app.run('0.0.0.0')