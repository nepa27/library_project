# Электронная библиотека

Удобная и лаконичная модель электронной библиотеки. После регистрации Вы сможете брать в аренду книги и возвращать их.
Администратор имеет расширенные функции, позволяющие редактировать список книг, а также просматривать список "должников".

### Установка

Во-первых установите Python и pip (команды для Ubuntu)
```
sudo apt-get install python
sudo apt-get install pip
```
Создайте виртуальное окружение
```
python -m venv venv
source venv/bin/activate    # (Ubuntu)
./venv/Scripts/python       # (Windows)
```
Затем установите необходимые зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

## Запуск

Перейдите в корневую директорию проекта, где находится файл manage.py
и запустите сервер
```
cd library_project
python manage.py runserver
```
Если вы все правильно сделали, то высветится приглашение
```
System check identified no issues (0 silenced).
March 25, 2024 - 15:35:58
Django version 3.2.16, using settings 'library_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Откройте браузер и перейдите по адресу http://127.0.0.1:8000/ 

При возникновении ошибки
```
python: can't open file 'library_project/manage.py'[Errno 2] No such file or directory
```
убедитесь, что вы находитесь в корневой директории проекта

### Стек технологий
