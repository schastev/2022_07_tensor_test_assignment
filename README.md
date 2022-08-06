[![test-assignment](https://github.com/schastev/2022_07_test_assignment/actions/workflows/python-app.yml/badge.svg?branch=main&event=push)](https://github.com/schastev/2022_07_test_assignment/actions/workflows/python-app.yml)

[Отчет Allure](https://schastev.github.io/2022_07_test_assignment)

[Автоматизированные сценарии](https://github.com/schastev/2022_07_test_assignment/blob/main/test-cases.md)

### Подготовка окружения

Данный проект можно запустить как с локальным браузером, так и с использованием Selenoid.

#### Локальный браузер

1. Необходимо убедиться, что в системе есть `chromedriver`.
2. В файле `config` выставить `local=true`.

#### Selenoid

1. Убедиться, что в системе установлены `docker`, `docker-compose`.
2. Скачать образ используемого Selenoid браузера командой `docker pull selenoid/vnc_chrome:103.0` .
3. Перейти в папку `Selenoid`, запустить Selenoid командой `docker-compose up`.
4. В браузере перейти по адресу `localhost:8080`, там должен развернуться Selenoid (далее `selenoid-ui`).

### Запуск тестов

1. Запустить тесты командой `pytest`. Если нужно, чтобы по результату прогона был сгенерирован отчет,
   добавить ` --alluredir=allure-results`.
2. *Сгенерировать и открыть отчет Allure командой `allure serve allure-results`.
   Для этого в системе должен быть установлен `allure`.

> Прим. 1.
> Selenoid настроен таким образом, что через веб-интерфейс можно наблюдать за тем, что происходит в контейнерах с
> браузерами.
> Для этого нужно после запуска теста в selenoid-ui найти появившуюся строку с браузером (Chrome 103.0) и кликнуть на
> неё.
> Откроется окно с логами контейнера справа и GUI слева.

> Прим. 2.
> Разработка данного проекта велась на машине с OS Linux.
> При попытке запуска проекта на машине с OS Windows могут возникнуть проблемы с поиском файла `confiq`.
> В этом случае можно либо обратиться к отчету, ссылку на который можно найти в начале данного файла, либо подменить
> тело метода `test.utils.config_utils.local_browser` на `return True`, если нужен запуск в локальном браузере,
> или на `return False`, если нужен запуск в Selenoid.
