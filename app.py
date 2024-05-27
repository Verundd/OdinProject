from flask import Flask, render_template, request
import validators
import methods as m

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    text_url = request.args.get('text')
    if validators.url(text_url):
        time_url = m.time_session(text_url)
        dns = m.params_dns(text_url)
        ssl = m.ssl_search(text_url)
        pin = m.ping(text_url)
        ports = m.scan_ports(text_url)

        results_dict ={
            "Время загрузки страницы:": time_url,
            "Параметры DNS:": dns,
            "Проверка SSL-сертификата и дополнительных параметров:": ssl,
            "Выполнение ping:": pin,
            "Сканирование портов:": ports
        }

        return render_template('search.html', name=results_dict)
    else:
        return render_template('search.html', name={'Ошибка': 'Введен некорректный URL'})

if __name__ == '__main__':
    app.run(debug=True)