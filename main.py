from flask import Flask, render_template, request, url_for, send_file
from werkzeug.utils import redirect
import io
import json
from datetime import datetime

from config import Config
from projects.forms import MessageForm

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Замените на свой секретный ключ


def save_to_json(name, email, text):
    try:
        # Читаем существующие данные
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Если файл не существует, создаем новую структуру
        data = {"messages": []}
    
    # Добавляем новое сообщение с временной меткой
    new_message = {
        "name": name,
        "email": email,
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    data["messages"].append(new_message)
    
    # Сохраняем обновленные данные
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


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
        print('\nData received. Now saving to JSON...')
        
        # Сохраняем данные в JSON
        save_to_json(name, email, text)
        
        return redirect(url_for('message'))

    return render_template(
        'index.html',
        form=form,
        name=name,
        email=email,
        text=text,
    )

@app.route('/zhopa')
def zhopa():
    return render_template('zhopa.html')

@app.route('/download')
def download():
    content = "ЖОПА"
    doc_content = content.encode('utf-8-sig')
    return send_file(
        io.BytesIO(doc_content),
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='document.docx'
    )

if __name__ == '__main__':
    app.run(debug=True)