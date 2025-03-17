from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from config import Config
from projects.forms import MessageForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
@app.route('/message', methods=['GET', 'POST'])
@app.route('/message/', methods=['GET', 'POST'])
def message():
    name = ''
    email = ''
    text = ''
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        text = form.message.data
        print(name)
        print(email)
        print(text)
        print('\nData received. Now redirection...')
        return redirect(url_for('message'))

    return render_template(
        'index.html',
        form=form,
        name=name,
        email=email,
        text=text,
    )