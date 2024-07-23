# Различные утилиты которые лень писать каждый раз 

- [`saver`](#saver) - Предназначена для сохранения файлов
- [`ua`](#ua) - Ротация юзер агентов. Мне не очень нравятся другие библиотеки
- [`repo`](#repo) - Базовый репозиторий для crud операция а также фабрика
- [`parsed`](#parsed) - Сохраняет в csv спарсенные и не удачно спарсенные файлы 
- [`proxy`](#proxy) - Менеджер для сервиса ротации прокси (самописного)
---

## **`saver`** 

### Назначение 
Cохранять структурированно скаченные файлы в зависимости от даты и времени в формате:  
`{базовая_папка}/год/месяц/день/час/путь`

### Установка:
```bash 
pip install mangust228[saver]
```

### Пример использования: 
```python
from mangust228.saver import AsyncSaveManager, SyncSaveManager

saver = AsyncSaveManager(base_path="example", compress=True)
# Первый аргумент - контент str, все последующие: то что добавить к названию
path = await saver.save_html("this is content", "seller_id", 4, 5)
print(path)  # "example/2024/05/29/22/seller_id_4_5.html.xz"
```
<span style="color:red">Для Синхронного метода методы аналогичные, только без await</span>


### Возможные аргументы 
- `base_path`: **str** Начальная папка в которую будет все сохраняться
- `add_uuid`: **bool** Добавить случайные символы в конце(на самом деле используется nanoid)
- `compress`: **bool** Сжать ли документ в формат .xz
- `debug`: **bool** Отображать ли логи 

---

## **`ua`** 

### Назначение 
Ротация user-agent. Мне не очень нравятся другие библиотеки из за устаревших ua.   

### Установка:
```bash 
pip install mangust228[ua]
```

### Пример использования: 
```python

# get Random User-Agent
UaRandom.web()
# get User-Agent like Chrome
UaRandom.web("chrome") 
# get User-Agent like Firefox
UaRandom.web("firefox")
# get User-Agent like Safari
UaRadom.web("safari")
```

--- 

## **`repo`** 

### Назначение 
Фабрика и Базовый репозиторий для выполнения CRUD операция 

### Установка:
```bash 
pip install mangust228[repo]
```

### Пример использования: 
```python

from mangust228.utils.repo import AsyncBaseRepo, AsyncBaseRepoFactory

# Модель алхимии
class UserModel(Base): 
    name: Mapped[str]
    surname: Mapped[str]

class UserRepo(AsyncBaseRepo[UserModel]):
    model = UserModel

    # Кастомный метод для работы с моделью
    async def do_something(self):
        stmt = select().where()
        self.session.execute(stmt)
        return 42

class Repository(AsyncBaseRepoFactory):
    session = session_maker # Объект SQLAlchemy 
    # Добавить кол-во репозиториев можно сколько угодно.
    user: UserRepo  
    another_repo: AnotherRepo 

async with Repository() as repo:
    user_model = UserModel(name="Sergey", surname="Sergeevich") # >> None 
    user = await repo.user.add_by_model(user_model) # Добавить в сессию модель

    await repo.user.add_by_kwargs(name="Ivan", surname="Ivanov") # >> UserModel

    # Удаляет по фильтру
    await repo.user.delete(name="Ivan") # >> int (Количество удаленных строк) 

    # Обновить по id (Модель должна содержать поле id!)
    await repo.user.update_by_id(id=5) # >> UserModel | None

    # Получить одного удовлетворящего условиям
    await repo.user.get_one_or_none(id=2, name="Sergey") # >> UserModel | None

    # Получить много моделей по фильтру. Можно передать limit and offset
    await repo.user.get_many(limit=5, name="Ivan") # list[UserModel]

    # Получить кол-во записей, удовлетворяющих условию(можно не передавать условия)
    await repo.user.count(surname="Petrov") # int (Кол-во Петровых) 


```

Аргументы которые можно передать в `Repository()`:

- `commit` (default: True): Сохраянть ли изменения, если использовать только GET, то можно поставить False  
- `debug` (default: False): Выводить логи
- `kwargs` Аргументы которые передатутся в сессию 

---

## **`proxy`** 

### Назначение 
Методы для работы с собственным сервисом ротации проксей 

### Установка:

```bash 
pip install mangust228[proxy]
```

### Пример использования: 

```python

from mangust228.proxy import SyncProxyManager, AsyncProxyManager

with SyncProxyManager() as pm:
    # Получить прокси
    proxy_1: ProxySchema = pm.get() 

    # Поменять прокси, если была вызвана ошибка 
    proxy_2: ProxySchema = pm.change_with_error(new_proxy, reason="just a test")

    # Поменять прокси, просто для профилактики
    proxy_3: ProxySchema = pm.change_without_error(new_proxy)

    # Освободить прокси 
    pm.free(proxy_3) 

async with AsyncProxyManager as pm: 
    proxy = await pm.get() # Методы аналоичные


# атрибуты объекта proxy: 
proxy.req_conn # формат, который подходит для вставки в requests или httpx
proxy.pw_conn # формат, который подходит для вставки в playwright   
```

### Переменные окружения 

```bash

PROXY_SERVICE_URL=http://100.100.100.100 # IP на котором сервис ротации
PROXY_SERVICE_API_KEY=SUPER_SECRET_API_KEY # API ключ 
PROXY_SERVICE_SERVICE_NAME=test # Сервис который парсим
PROXY_SERVICE_SERVICE_ID=1 # id сервиса который парсим 
PROXY_SERVICE_LOCK_TIME=300 # На сколько замораживаем прокси (в сек.) 

# not required
PROXY_SERVICE_LOGIC=linear # Алгоритм вычисления блокировки прокси
PROXY_SERVICE_LOGIC_BASE_TIME=10 # Базовое время блокировки (см. доку по сервису Ротации)
PROXY_SERVICE_IGNORE_HOURS=24 # см. доку по сервису Ротации
PROXY_SERVICE_TYPE_ID=1 # Тип прокси 1 - IPv4
PROXY_SERVICE_LOCATION_ID=1 # Геолокация 1 - Россия 

```


## **`parsed`** 

### Назначение 
Отслеживать, что спарсил, а что нет. 

### Установка:

```bash 
pip install mangust228[parsed]
```

### Пример использования: 

```python 

from parsed_manager import AsyncParsedManager as ParsedManager

# Добавить в неудачно спарсенные
await ParsedManager.wrong.add("url/path", reason) 

# Добавить в те что удачно спарсились 
await ParsedManager.success.add("url/path")  

# Проверить, есть ли в неудачно спарсенных, 
if ParsedManager.wrong.is_exist("url/path"):
    pass  # This block is executed if the URL/path has been parsed before.

``` 

<span style="color:red">Для Синхронного метода методы аналогичные, только без await</span>

В качестве аргумента функции принимают любые строки, в целом можно использовать и для других целей.
