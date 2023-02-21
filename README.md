# Devman notify bot 
С помощью **`devman notify bot`** получаем уведомления о результатах проверки предодавателем пройденных 
уроков по курсам  [dvmn.org](https://dvmn.org).  

## Как работает
Запускаем **`devman.py`** в консоли, при этом указываем chat_id пользователя. Производится направление запроса к [Long 
Polling API](https://dvmn.org/api/docs/), при получении ответа - информация передается ботом в чат пользователя. 

### Как установить
* Python3 должен уже быть установлен.
* Для изоляции проекта рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html).
* Чтобы развернуть зависимости, используйте **`pip`** (или **`pip3`**, если есть конфликт с Python2):

```bash
pip install -r requirements.txt
```
### Авторизация
Для хранения чувствительных данных (токен devman, токен бота, chat_id пользователя) создайте файл .env 
с переменными **`DEVMAN_TOKEN, TG_TOKEN, CHAT_ID`**.

#### Токен Devman
Персональный токен вида **`a7895e2a783d0XXXXXca804deca28a9035490e1`** указан на 
сайте [https://dvmn.org/api/docs/](https://dvmn.org/api/docs/).\
Сохраните его в переменной окружения .env, например:
**```DEVMAN_TOKEN=a7895e2a783d0XXXXXca804deca28a9035490e1```**.

#### Создание бота в Телеграме:

1. Перейдите в диалог с инструментом для разработки чатов — [https://telegram.me/BotFather](https://telegram.me/BotFather).
2. Нажмите кнопку "Start" или введите в диалоге команду /start.
3. Далее введите команду /newbot, чтобы сделать новый бот.
4. Укажите название — как будет отображаться чат в списке контактов.
5. Последнее — системное имя: это то, что будет ником после знака @. 
Cистемное имя обязательно должно быть уникальным. Если имя уже занято, вы увидите подсказку: "Sorry, this username is already taken. 
Please try something different".

![image](https://developers.sber.ru/help/assets/ideal-img/telegram-chat-bot.32e2f94.941.png)

6. После успешного создания вы получите токен HTTP API. 

![image](https://developers.sber.ru/help/assets/ideal-img/ti1.12da233.939.png)

7. Сохраните его в переменной окружения .env, например:
**```TG_TOKEN=95132391:wP3db3301vnrob33BZdb33KwP3db3F1I```**.

#### Узнать свой ID
Чтобы получить свой chat_id, напишите в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot).\
Полученный id сохраните в переменной окружения .env, например:
**```CHAT_ID=951323```**.

### Примеры
Для получения справки используйте аргумент ```-h``` или ```--help```.
 
```bash
$ python devman.py -h
```
Вывод:
```
usage: devman.py [-h] [chat_id]

Получение уведомлений с сайта dvmn.org

positional arguments:
  chat_id     Ввести chat_id

options:
  -h, --help  show this help message and exit
```
По умолчанию значение **`chat_id`** равно chat_id из переменной окружения.

Чтобы остановить сервис уведомлений, нажмите **`CTRL+C`**.
Ошибки будут выводится в консоль.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).

### Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [ЛИЦЕНЗИЯ](LICENSE).
