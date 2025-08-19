# ### Задача №3. Дополнительная (не обязательная)

# Применив selenium, напишите unit-test для авторизации на Яндексе 
# по url: https://passport.yandex.ru/auth/




# !!!! ВЫ БЛИН ВООООООООБЩЕ ПОНИМАЕТЕ ЧТО НЕ НУЖНО ДЕЛАТЬ ЗААДАНИЯ НА ОТРЕЧЕСТВЕННЫЕ САЙТЫ,
# ТАК КАК ОНИ ОТ КАЖДОЙ СЕСИИ ПРЕДЛАГАЮТ РАЗНЫЕ СЦЕНАРИИ АУТЕНТИФИКАЦИИ???? ГОСПОДА КУРАТОРЫ
# ПЕРЕСТАНЬТЕ ИЗДЕВАТЬСЯ ТАКИМИ ЗАДАНИЯМИ, ПУСТЬ ЛУЧШЕ УЧАЩИЕСЯ ПИШУТ ТЕСТЫ НА КАКИЕ_НИБУДЬ НЕ ЗАУРЯДНЫЕ САТЫ БЕЗ 
# ВСЯЧЕСКИХ ДИБИЛЬНЫХ РЕДИРЕКТОВ!!!!!

# !!!ЕСЛИ ЭТОТ КОД С ВЕТВЛЕНИЕМ СЦЕНАРИЯ НЕ ПОДОЙДЁТ, ТО В ТОПКУ...!!!! ТЕМ БОЛЕЕ ЗАДАНИЕ ЭТО 
# НЕ ОБЯЗАТЕЛЬНОЕ, НО УБИТО НА ЕГО НАПИСАНИЕ 3 ДНЯ и 18 ЧАСОВ ВРЕМЕНИ!!!!

# !!!!ТЕСТ ДАЁТ ОШИБКУ, ПОТОМУК ЧТО Я НЕ МОГУ ДОЙТИ ДО ТОГО ПОЧЕМУ У МЕНЯ ЗАНОВО НАЧИНАЕТ ВОСПРОИЗВОДИТЬСЯ СЦЕНАРИЙ
#  КОТОРЫЙ ИЩЕТ КНОПКУ ПОДТВЕРЖДЕНИЯ КОДА ИЗ СМС!!!!




# Импорт модуля для создания и запуска unit-тестов.
import unittest
# Импорт модуля для безопасного ввода конфиденциальных данных (например, пароля).
import getpass
# Импорт модуля для работы со временем (используется для пауз).
import time
# Импорт основного модуля Selenium WebDriver для автоматизации браузера.
from selenium import webdriver
# Импорт класса By для указания способов поиска элементов (по ID, CSS и т.д.).
from selenium.webdriver.common.by import By
# Импорт класса WebDriverWait для реализации "умных" ожиданий в Selenium.
from selenium.webdriver.support.ui import WebDriverWait
# Импорт набора предопределенных условий для ожиданий (например, элемент кликабелен).
from selenium.webdriver.support import expected_conditions as EC
# Импорт конкретного исключения, которое возникает при истечении времени ожидания.
from selenium.common.exceptions import TimeoutException

# Объявление тестового класса, который наследуется от unittest.TestCase.
# Это стандартный способ организации тестов в unittest.
class YandexAuthTest(unittest.TestCase):

    # Декоратор @classmethod указывает, что это метод класса.
    # Метод setUpClass выполняется ОДИН РАЗ перед запуском всех тестов в этом классе.
    # Он используется для настройки общих ресурсов для всех тестов.
    @classmethod
    def setUpClass(cls):
        """Инициализация теста"""  # Строка документации (docstring) для метода.
        # Вывод заголовка в консоль для улучшения читаемости логов.
        print("\n=== Тест авторизации Яндекс ===")
        # Запрос ввода логина у пользователя. .strip() удаляет лишние пробелы.
        # Введенное значение сохраняется в переменную КЛАССА cls.login.
        cls.login = input("Введите логин (example@yandex.ru): ").strip()

        # Условная проверка: если строка логина пуста после удаления пробелов...
        if not cls.login:
            # ...то вызывается специальное исключение,SkipTest,
            # которое пропускает все тесты в классе с указанием причины.
            raise unittest.SkipTest("Логин не введен")

        # Часть настройки браузера: создается объект опций для Chrome.
        options = webdriver.ChromeOptions()
        # Ключевая опция. Отключает функции Blink, которые позволяют сайтам
        # обнаруживать автоматизацию. Помогает обойти защиту от ботов.
        options.add_argument("--disable-blink-features=AutomationControlled")
        # Опция для отключения GPU-ускорения, иногда необходима для стабильности в headless-режиме или на серверах.
        options.add_argument("--disable-gpu")
        # Опция для запуска браузера без sandbox (песочницы). Часто требуется для работы
        # внутри Docker-контейнеров или под определенными правами.
        options.add_argument("--no-sandbox")
        # Инициализация самого драйвера браузера Chrome.
        # В конструктор передается созданный объект опций.
        # Созданный экземпляр WebDriver сохраняется в переменную КЛАССА cls.driver.
        cls.driver = webdriver.Chrome(options=options)
        # Команда браузеру открыться на весь экран.
        cls.driver.maximize_window()

        # Сохранение URL страницы логина Яндекс в переменную КЛАССА.
        # Это делается здесь, чтобы не хардкодить URL в самом тесте.
        cls.login_url = "https://passport.yandex.ru/auth/add/login"

    # Основной метод теста. Любой метод, имя которого начинается с 'test_',
    # автоматически распознается unittest как тест для запуска.
    def test_auth_flow(self):
        """Полный процесс авторизации"""  # Docstring для тестового метода.
        # Информационный вывод для логирования хода выполнения теста.
        print("\n1. Открытие страницы ввода логина...")
        # Команда драйверу перейти по URL, сохраненному в setUpClass.
        self.driver.get(self.login_url)

        # Ввод логина:
        # Создается объект ожидания WebDriverWait с таймаутом 20 секунд.
        # Он ожидает, пока условие (EC.element_to_be_clickable) не будет выполнено.
        # Условие ищет элемент с ID "passp-field-login" и ждет, пока он станет кликабельным.
        # Как только элемент найден и готов, он возвращается и присваивается в login_field.
        login_field = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "passp-field-login"))
        )
        # Метод .send_keys() имитирует ввод с клавиатуры, передавая в поле ввода логин.
        login_field.send_keys(self.login)
        # Подтверждение ввода логина в консоль.
        print(f"✓ Введен логин: {self.login}")

        # Поиск кнопки "Войти" по её ID и последующий клик по ней.
        # Здесь используется простой find_element, так как мы уверены, что кнопка уже есть на странице.
        self.driver.find_element(By.ID, "passp:sign-in").click()

        # Ожидание любого перехода
        # Явная пауза (ожидание) на 3 секунды. Это АНТИПАТТЕРН.
        # Используется потому, что после клика может произойти сложная JS-анимация
        # или редирект, которые трудно отследить стандартными ожиданиями Selenium.
        # Лучше заменить на ожидание изменения URL или появления элемента на новой странице.
        print("Ожидание перехода на следующую страницу...")
        time.sleep(3)

        # Получение текущего URL браузера после ожидания и потенциального перехода.
        current_url = self.driver.current_url
        # Вывод текущего URL для отладки и понимания, на какой странице мы оказались.
        print(f"Текущий URL: {current_url}")

        # Логика ветвления: в зависимости от того, какой фрагмент содержится в URL,
        # вызывается соответствующий метод-обработчик для этой страницы.
        if "auth/image" in current_url:
            print("✓ Переход на страницу с каптчей (image)")
            self._handle_captcha_page()  # Вызов метода для обработки каптчи.
        elif "auth/welcome" in current_url:
            print("✓ Переход на страницу выбора способа входа (welcome)")
            self._handle_welcome_page()  # Вызов метода для страницы выбора.
        elif "auth/challenge" in current_url:
            print("✓ Переход на страницу подтверждения (challenge)")
            self._handle_challenge_page()  # Вызов метода для страницы подтверждения (например, код из SMS).
        elif "auth/push-code" in current_url:
            print("✓ Переход на страницу ввода push-кода (push-code)")
            self._handle_push_code_page()  # Вызов метода для Push-кода.
        elif "auth/magic" in current_url:
            print("✓ Переход на страницу magic-ссылки (magic)")
            self._handle_magic_page()  # Вызов метода для страницы с "волшебной" ссылкой.
        else:
            # Если URL не соответствует ни одному известному шаблону,
            # делается скриншот для последующего анализа.
            self.driver.save_screenshot("unknown_page.png")
            # Тест принудительно помечается как проваленный с сообщением.
            self.fail(f"Неизвестная страница: {current_url}")

    # Приватный метод (соглашение об именовании _имя) для обработки страницы с "magic"-ссылкой.
    def _handle_magic_page(self):
        """Обработка страницы с magic-ссылкой и переход к вводу пароля"""
        print("\n2. Обнаружена страница с magic-ссылкой, ищем кнопку 'Войти с паролем'...")

        # Блок try/except для перехвата исключения TimeoutException,
        # которое может выбросить WebDriverWait.
        try:
            # Список кортежей. Каждый кортеж содержит способ поиска (By) и селектор.
            # Это надежная практика: если один селектор не сработает (например, из-за изменения верстки),
            # код попробует следующий.
            password_button_selectors = [
                (By.CSS_SELECTOR, "button.PasswordButton"), # По CSS-классу
                (By.CSS_SELECTOR, "button[class*='PasswordButton']"), # По классу, содержащему подстроку
                (By.CSS_SELECTOR, "button[data-t='button:pseudo']"), # По data-атрибуту
                (By.CSS_SELECTOR, "button[aria-label*='паролем']"), # По атрибуту aria-label
                (By.CSS_SELECTOR, "button:contains('Войти с паролем')"), # Псевдо-селектор по тексту (не работает в Selenium)
                (By.XPATH, "//button[contains(text(), 'Войти с паролем')]"), # По XPath, ищущему текст кнопки
                (By.XPATH, "//button[contains(., 'паролем')]") # По XPath, ищущему текст кнопки (более широкий)
            ]

            # Инициализация переменной для найденной кнопки.
            password_button = None
            # Цикл по всем селекторам из списка.
            for by, selector in password_button_selectors:
                try:
                    # Для каждой пары (by, selector) пытаемся найти элемент.
                    # Ожидание всего 5 секунд, так как селекторов много.
                    password_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    # Если элемент найден, сообщаем об этом и прерываем цикл break.
                    print(f"✓ Кнопка 'Войти с паролем' найдена по: {by} = {selector}")
                    break
                except TimeoutException:
                    # Если текущий селектор не сработал, переходим к следующему.
                    continue

            # Проверка: если после перебора всех селекторов кнопка так и не найдена...
            if not password_button:
                # ...делаем скриншот для анализа...
                self.driver.save_screenshot("magic_password_button_not_found.png")
                # ...и проваливаем тест с сообщением.
                self.fail("Не найдена кнопка 'Войти с паролем' на странице magic")

            # Клик по найденной кнопке.
            password_button.click()
            print("✓ Нажата кнопка 'Войти с паролем'")

            # Еще одна явная пауза после клика, чтобы дать время на анимацию/редирект.
            time.sleep(2)

            # Получение текущего URL после действия.
            current_url = self.driver.current_url
            print(f"URL после нажатия кнопки: {current_url}")

            # Проверка: если мы все еще на странице аутентификации (URL содержит 'auth')...
            if "auth" in current_url:
                # ...значит, нас перенаправило на страницу ввода пароля, вызываем соответствующий метод.
                self._handle_password_input()
            else:
                # ...иначе считаем, что авторизация прошла успешно, и идем на проверку.
                self._check_successful_auth()

        # Перехват исключения, если ни один селектор не сработал за отведенное время.
        except TimeoutException as e:
            self.driver.save_screenshot("magic_error.png")
            self.fail(f"Ошибка на странице magic: {str(e)}")

    # Метод для обработки страницы с каптчей. Логика очень похожа на _handle_magic_page.
    def _handle_captcha_page(self):
        """Обработка страницы с каптчей и переход к вводу пароля"""
        print("\n2. Обнаружена каптча, нажимаем 'Войти с паролем'...")

        try:
            # Ожидание появления кнопки "Войти с паролем". Пробуются два CSS-селектора.
            password_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.PasswordButton, button[class*='PasswordButton']"))
            )
            password_button.click()
            print("✓ Нажата кнопка 'Войти с паролем'")

            time.sleep(2)

            current_url = self.driver.current_url
            print(f"URL после нажатия кнопки: {current_url}")

            if "auth" in current_url:
                self._handle_password_input()
            else:
                self._check_successful_auth()

        except TimeoutException as e:
            self.driver.save_screenshot("captcha_error.png")
            self.fail(f"Ошибка на странице с каптчей: {str(e)}")

    # Основной метод для ввода пароля. Вызывается с разных страниц.
    def _handle_password_input(self):
        """Обработка ввода пароля после каптчи или magic-страницы"""
        print("3. Ввод пароля...")

        try:
            # Список селекторов для поиска поля ввода пароля.
            password_selectors = [
                (By.ID, "passp-field-passwd"), # Предпочтительный способ, по ID
                (By.NAME, "passwd"), # По атрибуту name
                (By.CSS_SELECTOR, "input[type='password']"), # По типу поля
                (By.CSS_SELECTOR, "input[name='passwd']"), # По имени
                (By.CSS_SELECTOR, "input[data-t='field:input-passwd']") # По data-атрибуту
            ]

            password_field = None
            # Цикл по селекторам, аналогичный тому, что используется для поиска кнопки.
            for by, selector in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"✓ Поле пароля найдено по: {by} = {selector}")
                    break
                except TimeoutException:
                    continue

            if not password_field:
                self.driver.save_screenshot("password_field_not_found.png")
                self.fail("Не найдено поле для ввода пароля")

            # Безопасный запрос пароля у пользователя. Текст не отображается в консоли.
            password = getpass.getpass("Введите пароль: ").strip()
            # Проверка, что пароль был введен.
            if not password:
                self.fail("Пароль не введен")

            # Очистка поля (на всякий случай) и ввод пароля.
            password_field.clear()
            password_field.send_keys(password)
            print("✓ Пароль введен") # В логах сам пароль не отображается.

            # Поиск кнопки подтверждения (Войти) после ввода пароля.
            submit_selectors = [
                (By.ID, "passp:sign-in"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "button[data-t='button:action']"),
                (By.CSS_SELECTOR, "button.Button2_view_action")
            ]

            submit_button = None
            for by, selector in submit_selectors:
                try:
                    submit_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    print(f"✓ Кнопка входа найдена по: {by} = {selector}")
                    break
                except TimeoutException:
                    continue

            if submit_button:
                submit_button.click()
                print("✓ Форма пароля отправлена")

                time.sleep(3)
                current_url = self.driver.current_url
                print(f"Текущий URL после ввода пароля: {current_url}")

                # После ввода пароля также возможны разные сценарии (MFA, успех).
                # Анализируем URL и передаем управление дальше.
                if "auth/challenge" in current_url:
                    self._handle_challenge_page()
                elif "auth/push-code" in current_url:
                    self._handle_push_code_page()
                elif "auth/image" in current_url:
                    self._handle_captcha_page() # Может потребоваться новая каптча.
                elif "auth/magic" in current_url:
                    self._handle_magic_page()
                else:
                    # Если не на странице аутентификации, проверяем успешный вход.
                    self._check_successful_auth()
            else:
                self.fail("Не найдена кнопка подтверждения пароля")

        except TimeoutException as e:
            self.driver.save_screenshot("password_error.png")
            self.fail(f"Ошибка при вводе пароля: {str(e)}")

    # Метод для обработки сценария с SMS. В текущем потоке теста не вызывается напрямую.
    def _handle_sms_scenario(self):
        """Обработка сценария с вводом SMS-кода"""
        print("\n4. Ввод SMS-кода...")

        try:
            # Ожидание появления поля для ввода кода из SMS.
            code_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, "passp-field-phoneCode"))
            )
            print("✓ Поле для SMS-кода найдено")
        except TimeoutException:
            self.driver.save_screenshot("sms_field_not_found.png")
            self.fail("Не найдено поле для SMS-кода")
        # Вызов общего метода для ввода и отправки кода.
        self._input_and_submit_code(code_field)

    # Метод для обработки страницы ввода Push-кода.
    def _handle_push_code_page(self):
        """Обработка страницы ввода push-кода"""
        print("\n4. Ввод кода на странице push-code...")

        try:
            # Ожидание поля для Push-кода по ID.
            code_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, "passp-field-pushCode"))
            )
            print("✓ Поле для push-кода найдено")
        except TimeoutException:
            # Если не нашли по ID, пробуем альтернативный селектор по имени.
            try:
                code_field = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pushCode']"))
                )
                print("✓ Поле для push-кода найдено (по имени)")
            except TimeoutException:
                self.driver.save_screenshot("push_code_field_not_found.png")
                self.fail("Не найдено поле для кода на странице push-code")
        # Вызов общего метода для ввода и отправки кода.
        self._input_and_submit_code(code_field)

    # Метод для обработки страницы выбора способа входа (например, пароль или SMS).
    def _handle_welcome_page(self):
        """Обработка страницы выбора способа входа"""
        print("\n2. Страница выбора способа входа")

        try:
            # Ожидание и клик по кнопке входа через SMS.
            sms_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-t='button:default:auth-by-sms']"))
            )
            sms_button.click()
            print("✓ Выбран вход через SMS")

            time.sleep(2)
            current_url = self.driver.current_url
            # Анализ, куда нас перенаправило после выбора SMS.
            if "push-code" in current_url:
                self._handle_push_code_page()
            elif "image" in current_url:
                self._handle_sms_scenario() # Вероятно, опечатка? Должен быть вызов обработки SMS.
            else:
                self._handle_sms_scenario() # Стандартный сценарий SMS.
        except TimeoutException:
            self.fail("Не найдена кнопка входа через SMS")

    # Универсальный метод для страницы подтверждения (challenge).
    def _handle_challenge_page(self):
        """Обработка страницы подтверждения"""
        print("\n4. Страница подтверждения")

        try:
            # Пытаемся найти поле для кода (подходит и для SMS, и для Push).
            # Используется CSS-селектор, который ищет элемент по одному из возможных ID или name.
            code_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#passp-field-phoneCode, #passp-field-pushCode, input[name='phoneCode'], input[name='pushCode']"))
            )
            print("✓ Найдено поле для кода подтверждения")
            self._input_and_submit_code(code_field)
        except TimeoutException:
            self.fail("Не найдено поле для кода на странице подтверждения")

    # Общий метод для ввода 6-значного кода и его отправки.
    def _input_and_submit_code(self, code_field):
        """Общий метод для ввода и отправки кода"""
        print("На ваш телефон, привязанный к аккаунту, будет отправлен код")
        # Запрос кода у пользователя через стандартный input.
        sms_code = input("Введите 6-значный код: ").strip()

        # Валидация введенного кода: должен быть ровно 6 символов и только цифры.
        if not sms_code or len(sms_code) != 6 or not sms_code.isdigit():
            self.fail("Неверный формат кода (требуется 6 цифр)")

        # Очистка поля и ввод кода.
        code_field.clear()
        code_field.send_keys(sms_code)
        print(f"✓ Введен код: {sms_code}") # Код логируется, что может быть небезопасно.

        # Поиск и нажатие кнопки подтверждения (Войти).
        try:
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], #passp\\:sign-in"))
            )
            submit_button.click()
        except TimeoutException:
            self.fail("Не найдена кнопка подтверждения")

        # Финальная проверка успешной авторизации.
        self._check_successful_auth()

    # Метод для финальной проверки, что авторизация прошла успешно.
    def _check_successful_auth(self):
        """Проверка успешной авторизации"""
        try:
            # Ожидание с помощью пользовательского условия (lambda).
            # Условие ждет, пока текущий URL НЕ будет содержать 'auth' и 'passport'.
            # Это означает, что браузер покинул сайт аутентификации и перешел на целевую страницу (почта, диск и т.д.).
            WebDriverWait(self.driver, 20).until(
                lambda d: "auth" not in d.current_url and "passport" not in d.current_url
            )
            # Если условие выполнено, авторизация считается успешной.
            print(f"✓ Авторизация успешна! Текущая страница: {self.driver.current_url}")
        except TimeoutException:
            # Если в течение 20 секунд URL не изменился должным образом, тест падает.
            self.driver.save_screenshot("auth_failed.png")
            self.fail("Не удалось подтвердить авторизацию")

    # Метод класса, выполняемый ОДИН РАЗ после всех тестов.
    # Используется для очистки ресурсов.
    @classmethod
    def tearDownClass(cls):
        """Завершение теста"""
        # Проверка, что драйвер был создан и существует, перед тем как его закрыть.
        if hasattr(cls, 'driver') and cls.driver:
            # Команда браузеру полностью завершить работу и закрыть все окна.
            cls.driver.quit()
        # Информационное сообщение о завершении.
        print("\n=== Тестирование завершено ===")

# Стандартная конструкция для запуска тестового набора, если файл выполняется напрямую.
if __name__ == "__main__":
    unittest.main()