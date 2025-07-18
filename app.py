from flask import Flask, render_template, request, session
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'любая_секретная_строка'

API_KEY = '9e3de4b9d0789e52a3c1f3494b4e11b2'

# Список городов Украины
cities_ukraine = [
    "Киев", "Харьков", "Одесса", "Днепр", "Донецк", "Львов", "Запорожье", "Кривой Рог", 
    "Николаев", "Мариуполь", "Луганск", "Винница", "Макеевка", "Полтава", "Херсон", 
    "Симферополь", "Севастополь", "Горловка", "Чернигов", "Хмельницкий", "Черкассы", 
    "Черновцы", "Житомир", "Сумы", "Ровно", "Ивано-Франковск", "Каменское", "Тернополь", 
    "Кропивницкий", "Луцк", "Кременчуг", "Белая Церковь", "Керчь", "Мелитополь", 
    "Краматорск", "Ужгород", "Бровары", "Евпатория", "Бердянск", "Алчевск", "Никополь", 
    "Славянск", "Павлоград", "Северодонецк", "Каменец-Подольский", "Лисичанск", 
    "Красный Луч (Хрустальный)", "Енакиево", "Александрия", "Стаханов (Кадиевка)", 
    "Константиновка"
]

# Список часов, которые мы хотим отобразить
selected_hours = [6, 9, 10, 12, 15, 18, 21]  # 06:00, 09:00, 10:00, 12:00, 15:00, 18:00, 21:00

@app.route("/", methods=["GET", "POST"])
def index():
    weather = {}
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        city = request.form['city']
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Текущая погода
            current_weather = {
                'город': data['city']['name'],
                'температура': data['list'][0]['main']['temp'],
                'описание': data['list'][0]['weather'][0]['description'],
                'иконка': data['list'][0]['weather'][0]['icon']
            }
            weather['current'] = current_weather

            # Прогноз на определенные часы (06:00, 09:00, 10:00, 12:00, ...)
            forecast = []
            for day in data['list']:
                # Извлекаем время
                dt = datetime.utcfromtimestamp(day['dt'])
                hour = dt.hour
                # Если час в списке selected_hours, добавляем в прогноз
                if hour in selected_hours:
                    forecast.append({
                        'день': dt.strftime('%d-%m-%Y'),  # День в формате день-месяц-год
                        'время': dt.strftime('%H:%M'),  # Время в формате 06:00, 09:00 и т.д.
                        'температура': day['main']['temp'],
                        'описание': day['weather'][0]['description'],
                        'иконка': day['weather'][0]['icon']
                    })
            weather['forecast'] = forecast

            session['history'] = ([weather['current']['город']] + session['history'])[:5]
        else:
            weather['ошибка'] = "Город не найден"

    return render_template("index.html", weather=weather, history=session['history'], cities=cities_ukraine)

if __name__ == "__main__":
    app.run(debug=True)
