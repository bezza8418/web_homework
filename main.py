from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Определяем, какую страницу отдать
        if path == "/" or path == "/index.html":
            self.serve_html("index.html")
        elif path == "/catalog":
            self.serve_html("catalog.html")
        elif path == "/category1":
            self.serve_html("category1.html")
        elif path == "/contacts":
            self.serve_html("contacts.html")
        else:
            # Страница 404 - используем английский текст для статуса
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Отправляем красивую страницу 404 на русском
            error_page = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>404 - Страница не найдена</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <div class="alert alert-danger">
                        <h1>404</h1>
                        <h4>Страница не найдена</h4>
                        <p>Запрашиваемая страница не существует.</p>
                        <a href="/" class="btn btn-primary">Вернуться на главную</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(error_page.encode('utf-8'))

    def do_POST(self):
        """Обработка POST-запросов (для формы контактов)"""
        if self.path == "/contacts":
            # Получаем длину содержимого
            content_length = int(self.headers.get('Content-Length', 0))

            # Читаем данные из тела запроса
            post_data = self.rfile.read(content_length)

            # Декодируем данные
            data_string = post_data.decode('utf-8')

            # Парсим данные из формы
            parsed_data = parse_qs(data_string)

            # Выводим в консоль красиво
            print("\n" + "=" * 50)
            print("📬 Получены данные из формы контактов:")
            print("=" * 50)
            for key, value in parsed_data.items():
                print(f"{key}: {value[0]}")
            print("=" * 50 + "\n")

            # Отправляем ответ пользователю
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Отправляем страницу с подтверждением
            response = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Сообщение отправлено</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-5">
                    <div class="alert alert-success">
                        <h4>✅ Спасибо за обращение!</h4>
                        <p>Ваше сообщение успешно отправлено. Мы свяжемся с вами в ближайшее время.</p>
                        <a href="/contacts" class="btn btn-primary">Вернуться к контактам</a>
                        <a href="/" class="btn btn-secondary">На главную</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page not found</h1>")

    def serve_html(self, filename):
        """Вспомогательная функция для отправки HTML-файлов"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h1>404 - Файл {filename} не найден</h1>".encode('utf-8'))


def run_server(port=8080):
    """Запуск сервера"""
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"🚀 Сервер запущен на http://localhost:{port}")
    print("📝 Чтобы остановить сервер, нажмите Ctrl+C")
    print("\nДоступные страницы:")
    print("  - http://localhost:8080/        (Главная)")
    print("  - http://localhost:8080/catalog (Каталог)")
    print("  - http://localhost:8080/contacts (Контакты с формой)")
    print("  - http://localhost:8080/category1 (Электроника)")
    print("\n✨ Готов к работе!\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Сервер остановлен")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
