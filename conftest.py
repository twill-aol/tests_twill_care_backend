# import pytest
# import time

# def pytest_addoption(parser):
#     parser.addoption('--browser_name', action='store', default='firefox',
#                      help="Choose browser: chrome or firefox")


# @pytest.fixture(scope="function")
# def browser(request):
#     browser_name = request.config.getoption("browser_name")
#     browser = None
#     if browser_name == "chrome":
#         print("\nstart chrome browser for test..")
#         browser = webdriver.Chrome()
#     elif browser_name == "firefox":
#         print("\nstart firefox browser for test..")
#         browser = webdriver.Firefox()
#     # else:
#     #     raise pytest.UsageError("--browser_name should be chrome or firefox")
#     yield browser
#     print("\nquit browser..")
#     browser.quit()

# pytest -s -v --browser_name=firefox test_parser.py



# _______________________________________________________________________________________________________________________________________
# Чтобы указать язык браузера с помощью WebDriver, используйте класс Options и метод add_experimental_option, как указано в примере ниже:

# from selenium.webdriver.chrome.options import Options

# options = Options()
# options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
# browser = webdriver.Chrome(options=options)

# Для Firefox объявление нужного языка будет выглядеть немного иначе:

# fp = webdriver.FirefoxProfile()
# fp.set_preference("intl.accept_languages", user_language)
# browser = webdriver.Firefox(firefox_profile=fp)
# ______________
# В конструктор webdriver.Chrome или webdriver.Firefox вы можете добавлять разные аргументы, расширяя возможности тестирования ваших веб-приложений: 
# можно указывать прокси-сервер для контроля сетевого трафика или запускать разные версии браузера, указывая локальный путь к файлу браузера. 
# Предполагаем, что эти возможности вам понадобятся позже и вы сами сможете найти настройки для этих задач.
# _______________________________________________________________________________________________________________________________________
