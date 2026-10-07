# необходимые библиотеки
import requests
import random
import time

# КОНСТАНТЫ
# 1) Отсюда получим список категорий (для выбора):
CATEGORIES_URL = "https://api.chucknorris.io/jokes/categories"
# 2) Отсюда получим случайную шутку выбранной категории, добавив после "=" значение категории
JOKE_SELECTED_BY_CATEGORY = "https://api.chucknorris.io/jokes/random?category="

class JokeCreateTesting():

    def category_select(self):  # Получаем список категорий шуток и выбираем одну категорию рандомно
        self.result = requests.get(CATEGORIES_URL)  # GET-запрос на получение списка категорий
        self.categories = self.result.json()  # весь ответ сервера
        print(f"Список категорий шуток получен с адреса {CATEGORIES_URL}:")
        # Из всего ответа сервера берем только значение категорий, преобразуем в строку и выводим, убрав лишние символы:
        print(str(self.categories).strip("[]").replace("'", ""))
        time.sleep(1)
        self.selected_category = random.choice(self.categories)  # категорию выбираем рандомно
        # это будет использовано для энд-пойнта с выбором категории
        print(f"Выбрана категория шутки: {self.selected_category}")

    def getting_the_joke(self):  # Запрос на получение рандомной шутки:
        self.current_url = f"{JOKE_SELECTED_BY_CATEGORY}{self.selected_category}"  # добавили к адресу выбранную категорию
        self.result = requests.get(self.current_url)  # весь ответ сервера на GET-запрос
        print(f"GET-запрос отправлен по адресу: {self.current_url}")
        print("Cтатус код ответа:",self.result.status_code)  # получаем статус-код из (весь ответ сервера)

        # Проверка на статус-код:
        assert self.result.status_code == 200, "Провал, статус код НЕверен!"  # Проверка условия ФР == ОР
        print("\033[32mУспех, статус код ответа сервера верен\033[0m")  # если ОР == ФР

        # Проверка на соответствие категории:
        fact_category = str(self.result.json().get('categories')).strip("'[]'") # получаем из ответа и убираем лишние символы
        assert fact_category == str(self.selected_category), "Провал, фактическая категория полученной шутки НЕ соответствует ожидаемой"
        print(f'32mУспех, фактическая категория полученной шутки ({fact_category}) соответствует ожидаемой\033[0m')

        # Проверка на содержании имени Chuck в теле шутки:
        joke_body = self.result.json().get("value","") # текст шутки в поле value,
        # если такое поле в ответе есть, поэтому и "", если поле value отсутствует
        # Проверяем вхождение слова Chuck в текст шутки:
        assert "Chuck" in joke_body, "Имя Chuck в теле полученной шутки НЕ содержится"
        print("\033[32mУспех, имя Chuck в теле полученной шутки содержится\033[0m")

        # Вывод на печать самой шутки:
        print(f"Текст полученной шутки:\n\033[36m{joke_body}\033[0m",sep='')

start = JokeCreateTesting()  # Создаём экземпляр класса
start.category_select()  # Получаем список категорий и выбираем одну категорию
start.getting_the_joke()  # Тестируем получение шутки выбранной категории