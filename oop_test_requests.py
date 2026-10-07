# необходимые библиотеки
import requests
import random
import time


class JokeCreateTesting():
    def __init__(self):  # Создаем атрибуты экземпляра класса
    # 1) Адрес списка категорий (для выбора):
        self.categories_url = "https://api.chucknorris.io/jokes/categories"
    # 2) Адрес случайной шутки по выбранной категории без необходимого значения категории:
        self.joke_selected_by_category = "https://api.chucknorris.io/jokes/random?category="
    # 3) Переменная для выбранной категории:
        self.selected_category = ""

    def category_select(self):  # Получаем список категорий и выбираем одну рандомно
        result = requests.get(self.categories_url)  # ответ на GET-запрос
        categories = result.json()  # список категорий из ответа
        print(f"Список категорий шуток получен с адреса {self.categories_url}:")
        # Из всего ответа сервера берем только значение категорий,
        # преобразуем в строку и выводим, убрав лишние символы:
        print(str(categories).strip("[]").replace("'", ""))
        time.sleep(1)
        # Рандомно выбираем категорию, переводим строку, если надо
        self.selected_category = str(random.choice(categories))
        # это будет использовано для энд-пойнта с выбором категории
        print(f"Выбрана категория шутки: {self.selected_category}")

    def getting_the_joke(self):  # Тестируем получение рандомной шутки выбранной категории
        # Добавим к неполному адресу выбранную категорию:
        current_url = f"{self.joke_selected_by_category}{self.selected_category}"
        result = requests.get(current_url)  # весь ответ сервера на GET-запрос
        print(f"GET-запрос отправлен по адресу: {current_url}")
        # Выводим на экран статус-код из ответа сервера
        print("Cтатус код ответа:",result.status_code)

        # Проверка на статус-код: (Проверка условия ФР == ОР)
        assert result.status_code == 200, "Провал, статус код НЕверен!"
        print("\033[32mУспех, статус код ответа сервера верен\033[0m")  # если ОР == ФР

        # Проверка на соответствие категории полученной шутки.
        # Из ответа в формате JSON получаем списком категории (категорию) по ключу categories
        fact_categories_list = result.json().get("categories", [])
        # Проверяем, есть ли выбранная категория в списке из полученных категорий
        assert (self.selected_category in fact_categories_list), \
            "Провал, фактическая категория полученной шутки НЕ соответствует ожидаемой"
        print(f'\033[32mУспех, фактическая категория полученной шутки '
            f'({str(fact_categories_list).strip("[]").replace("'","")}) '
            f'соответствует ожидаемой ({self.selected_category})\033[0m')

        # Проверка на содержании имени Chuck в теле шутки:
        joke_body = result.json().get("value","") # текст шутки в поле value,
        # если такое поле в ответе есть, поэтому и "", если поле value отсутствует
        # Проверяем вхождение слова Chuck в текст шутки:
        assert "Chuck" in joke_body, "Имя Chuck в теле полученной шутки НЕ содержится"
        print("\033[32mУспех, имя Chuck в теле полученной шутки содержится\033[0m")

        # Вывод на печать самой шутки:
        print(f"Текст полученной шутки:\n\033[36m{joke_body}\033[0m",sep='')


start = JokeCreateTesting()  # Создаём экземпляр класса
start.category_select()  # Получаем список категорий и выбираем одну категорию (рандомно)
start.getting_the_joke()  # Тестируем получение рандомной шутки выбранной категории