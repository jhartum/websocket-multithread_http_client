# websocket-multithread_http_client

Websocket - подготавливает данные и отдает клиенту.

Многопоточный клиент - скачивает файл по частям в многопоточном режиме. Файл разбивается на части с учетом лимита по
байтам на поток и каждый поток загружает свою часть и сохраняет в папку files. Как разбивается на части загружаемый
файл: лимит потоков=5, лимит байтов на поток=1024, файл размером 4500 байт проходит итерацию в ренже количества потоков
и на выходе получаем список строк которые подставляем в header range для загрузки файла.

# How to startup

1. В одном терминале запустить server.py
2. В новом терминале запустить client.py
