# Задача №2 Автотест API Яндекса

# Проверим правильность работы Яндекс.Диск REST API. Написать тесты, проверяющий создание папки на Диске.
# Используя библиотеку requests напишите unit-test на верный ответ и возможные отрицательные тесты на ответы с ошибкой

# Пример положительных тестов:

#     Код ответа соответствует 200.
#     Результат создания папки - папка появилась в списке файлов.




# БУдем использовать следующие проверки (asserts):

#     assertEqual(a, b) - проверка равенства a и b (например, статус-кода ответа)
#     assertIn(a, b)    - проверка, что a содержится в b (текст ошибки в описании)
#     assertRaises(Ex)  - проверка, что код вызывает исключение Ex (для сетевых ошибок)

#     subTest - позволяет параметризировать тесты без 
#               создания отдельных методов (то же что если бы мы использовали бы встроинную параметризацию )
# Перед выполнением тест нам нужно будет каждый раз проверять наличие тестовой папки
# на ЯндексДиске, ну и как мимнимум подчищать за собой следы после теста. 
# Так же тест запускаться будет тогда, 
# когда будет проведена валидность API-ключа, если API неверен или не введён 
# - то тест не будет запу3скаться. 
# За это отвечают методы:
#   setUpClass(cls) --	Классовый метод для однократной инициализации 
#                       (запрос токена) перед всеми тестами
#   setUp(self) 	--  Подготовка перед каждым тестом (удаление тестовой папки)
#   tearDown(self)  --	Очистка после каждого теста (удаление тестовой папки)
# Для параметризованных, разных наборов данных теста будем использовать декораторы 
# бибилиотеки   parameterized. Чтобы не создавать лишнего нагромождения, да и
# читать/воспринимать кортеж намного удобнее. 
# Вот таким образом:
# 
# @parameterized.expand([
#     ("empty_name", "", 400),
#     ("spaces_only", "   ", 400),
#     ...
#                       ])





# Импорт необходимых библиотек
import unittest  # Стандартный модуль для unit-тестирования
import requests  # Для выполнения HTTP-запросов к API
from unittest.mock import patch  # Для создания mock-объектов
from parameterized import parameterized  # Для параметризации тестов

class TestYandexDiskAPI(unittest.TestCase):
    """
    Класс тестов для API Яндекс.Диска.
    Наследуется от unittest.TestCase для интеграции с фреймворком unittest.
    """
    
    # Базовый URL API Яндекс.Диска для работы с ресурсами
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    
    # Имя тестовой папки (можно параметризировать при необходимости)
    FOLDER_NAME = "test_folder"
    
    # Максимально допустимая длина имени папки согласно документации API
    MAX_NAME_LENGTH = 255

    @classmethod
    def setUpClass(cls):
        """
        Метод класса, выполняемый один раз перед всеми тестами.
        Здесь выполняется инициализация: запрос токена и проверка его валидности.
        """
        print("\n=== Тестирование Яндекс.Диск API ===")
        print("Введите OAuth-токен (будет отображаться):")
        # Запрос токена у пользователя с отображением ввода
        cls.TOKEN = input("Токен: ").strip()
        
        # Если токен не введен, пропускаем все тесты
        if not cls.TOKEN:
            raise unittest.SkipTest("Токен не введен")
        
        # Формируем стандартные заголовки для запросов
        cls.headers = {
            "Authorization": f"OAuth {cls.TOKEN}",  # Авторизационный токен
            "Content-Type": "application/json",      # Тип содержимого
            "Accept-Language": "ru"                  # Язык ответов
        }
        
        # Проверка валидности токена
        try:
            # Тестовый запрос к корню диска
            test_response = requests.get(
                f"{cls.BASE_URL}?path=/", 
                headers=cls.headers,
                timeout=5  # Таймаут 5 секунд
            )
            # Если токен недействителен
            if test_response.status_code == 401:
                raise unittest.SkipTest("Неверный токен")
        except requests.exceptions.RequestException as e:
            # Обработка сетевых ошибок
            raise unittest.SkipTest(f"Ошибка подключения: {str(e)}")

    def setUp(self):
        """
        Метод, выполняемый перед каждым тестом.
        Очищает среду - удаляет тестовую папку, если она существует.
        """
        self._clean_test_folder()

    def tearDown(self):
        """
        Метод, выполняемый после каждого теста.
        Удаляет тестовую папку для очистки окружения.
        """
        self._clean_test_folder()

    def _clean_test_folder(self):
        """
        Вспомогательный метод для удаления тестовой папки.
        Используется в setUp и tearDown.
        """
        requests.delete(
            f"{self.BASE_URL}?path=/{self.FOLDER_NAME}",
            headers=self.headers,
            timeout=5
        )

    def test_create_folder_success(self):
        """
        Тест успешного создания папки.
        Проверяет:
        1. Код ответа при создании (201 Created)
        2. Фактическое наличие папки на диске (200 OK)
        """
        # Запрос на создание папки
        response = requests.put(
            f"{self.BASE_URL}?path=/{self.FOLDER_NAME}",
            headers=self.headers,
            timeout=5
        )
        # Проверка кода ответа
        self.assertEqual(response.status_code, 201)
        
        # Проверка существования папки
        check_response = requests.get(
            f"{self.BASE_URL}?path=/{self.FOLDER_NAME}",
            headers=self.headers,
            timeout=5
        )
        self.assertEqual(check_response.status_code, 200)

    def test_create_folder_already_exists(self):
        """
        Тест попытки создания уже существующей папки.
        Ожидаемый результат:
        - Код 409 Conflict
        - Сообщение об ошибке содержит указание на существование папки
        """
        # Создаем папку первый раз
        requests.put(
            f"{self.BASE_URL}?path=/{self.FOLDER_NAME}",
            headers=self.headers,
            timeout=5
        )
        
        # Пытаемся создать снова
        response = requests.put(
            f"{self.BASE_URL}?path=/{self.FOLDER_NAME}",
            headers=self.headers,
            timeout=5
        )
        
        # Проверка кода ответа
        self.assertEqual(response.status_code, 409)
        
        # Проверка текста ошибки (поддержка русского и английского)
        error_desc = response.json()["description"].lower()
        self.assertTrue(
            any(word in error_desc for word in ["exist", "уже существует"]),
            f"Неожиданное описание ошибки: {error_desc}"
        )

    @parameterized.expand([
        ("empty_name", "", 409),  # Пустое имя
        ("spaces_only", "   ", 409),  # Имя из пробелов
        ("invalid_char", "folder*name", 409),  # Запрещенные символы
        ("nested_path", "folder/name", 409),  # Вложенный путь
        ("too_long", "a" * (MAX_NAME_LENGTH + 1), 404),  # Слишком длинное имя
    ])
    def test_create_folder_invalid_name(self, name, folder_name, expected_code):
        """
        Параметризированный тест недопустимых имен папок.
        Проверяет различные варианты некорректных имен.
        Параметры:
        - name: описательное имя теста
        - folder_name: тестируемое имя папки
        - expected_code: ожидаемый код ответа
        """
        response = requests.put(
            f"{self.BASE_URL}?path=/{folder_name}",
            headers=self.headers,
            timeout=5
        )
        
        # Проверка кода ответа с подробным сообщением об ошибке
        self.assertEqual(
            response.status_code, 
            expected_code,
            f"Для имени '{folder_name}' получен код {response.status_code}, "
            f"ожидался {expected_code}. Описание: {response.json().get('description', '')}"
        )

    def test_create_nested_folder(self):
        """
        Тест создания вложенной папки.
        Ожидаемые коды:
        - 201 Created: если папка создана
        - 409 Conflict: если папка уже существует
        """
        nested_path = f"{self.FOLDER_NAME}/subfolder"
        response = requests.put(
            f"{self.BASE_URL}?path=/{nested_path}",
            headers=self.headers,
            timeout=5
        )
        self.assertIn(response.status_code, [201, 409])

    @patch('requests.put')
    def test_network_errors(self, mock_put):
        """
        Тест обработки сетевых ошибок.
        Использует mock для симуляции проблем с сетью.
        """
        # Настраиваем mock для выброса исключения
        mock_put.side_effect = requests.exceptions.ConnectionError("Ошибка подключения")
        
        # Проверяем, что исключение действительно возникает
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.put(
                f"{self.BASE_URL}?path=/{self.FOLDER_NAME}",
                headers=self.headers,
                timeout=5
            )

if __name__ == "__main__":
    # Точка входа для запуска тестов
    print("Запуск тестов Яндекс.Диск API...")
    unittest.main(verbosity=2)  # verbosity=2 для подробного вывода