import sys
from functools import wraps
from json import dumps


def require_auth(func):
    @wraps(func)  # Сохраняем имя исходной функции
    def wrapper(params):
        if 'name' not in params:  # Более простой способ проверки ключа
            return [403, "Forbidden"]
        else:
            return func(params)
    return wrapper


def log_call(func):
    @wraps(func)  # Сохраняем имя исходной функции
    def wrapper(params):
        # Вызываем функцию, получаем её реальный ответ (например, кортеж (200, "text"))
        result = func(params)
            
        # Формируем словарь логирования
        data = {
            "handler": func.__name__, 
            "params": params, 
            "response": list(result)
        }
        # Декоратор должен возвращать JSON-строку (мы же импортировали dumps)
        return dumps(data, ensure_ascii=False)
    return wrapper


# Handler'ы для разных маршрутов
@log_call
def home_handler(params):
    return 200, "Home Page"


@log_call
def admin_handler(params):
    return 200, "Admin Panel"


@log_call
@require_auth
def user_handler(params):
    # Должен использовать параметр name из URL
    return 200, f"Hello, {params['name']}!"


@log_call
@require_auth
def attempt_handler(params):
    # Должен использовать параметр name из URL
    return (
        200,
        f"Good try, {params['name']}! Your attempt on task '{params['task']}' is accepted!",
    )


@log_call
def not_found_handler(params):
    return 404, "Not Found"


# Функция маршрутизации
def router(path):
    if path == "/":
        return home_handler
    elif path.startswith("/user"):
        return user_handler
    elif path.startswith("/attempt"):
        return attempt_handler
    elif path.startswith("/admin"):
        return admin_handler

    return not_found_handler


# WSGI-сервер (генератор) — ЭТУ ФУНКЦИЮ НУЖНО РЕАЛИЗОВАТЬ
def wsgi_server():
    """Обрабатывает запросы и возвращает каждый из ответов через yield"""
    request = yield None  # запуск генератора, приём первого запроса app.send(None)
    while True:
    # Здесь надо написать обработку request и вызов нужного handler`а для получения response
        if request.split("/")[0] == "GET ":
            route_get = request.split("/")[1].replace('\n', '')
            if route_get == '':
                params = {}
                response = home_handler(params)
            elif route_get == 'admin':
                params = {}
                response = admin_handler(params)
            elif "user?name=" in route_get:
                user_name = route_get.split("=")[1]
                params = {'name': user_name}
                response = user_handler(params)
            else:
                params = {}
                response = not_found_handler(params)
        else:
            route_post = request.split("/")[1].replace('\n', '')
            name_and_task = route_post.split("?")[1]
            
            if 'task' in name_and_task and 'name' in name_and_task:
                name = name_and_task.split("&")[0]
                get_name = name.split("=")[1]
                task = name_and_task.split("&")[1]
                get_task = task.split("=")[1]
            else:
                if 'name' in name_and_task and get_task == '':
                    name = name_and_task.split("&")[0]
                    get_name = name.split("=")[1]
                else:
                    get_name = ''
                
                if 'task' in name_and_task and get_name == '':
                    task = name_and_task.split("&")[0]
                    get_task = task.split("=")[1]
                else:
                    get_task = ''
                
                
            if get_name == '' and get_task != '':
                params = {'task': get_task}
            elif get_task == '' and get_name != '':
                params = {'name': get_name}
            elif get_task == '' and get_name == '':
                params = {}
            else:
                params = {'name': get_name, 'task': get_task}
            
            response = attempt_handler(params)
        request = yield response
    
    
# Имитация работы сервера
app = wsgi_server()
app.send(None)

for request in sys.stdin:
    print(app.send(request))