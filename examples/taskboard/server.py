"""Servidor didático local. Não adequado para produção."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from domain import create_task


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # Não registrar conteúdo de requisições.

    def reply(self, status, data, kind="application/json; charset=utf-8"):
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.reply(200, Path(__file__).with_name("index.html").read_bytes(), "text/html; charset=utf-8")
        else:
            self.reply(404, {"error": "Rota não encontrada."})

    def do_POST(self):
        if self.path != "/api/tasks":
            self.reply(404, {"error": "Rota não encontrada."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 4096:
                self.reply(413, {"error": "Tamanho da entrada inválido."})
                return
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError("Envie um objeto JSON.")
            task = create_task(data.get("title"))
        except (ValueError, UnicodeDecodeError):
            self.reply(400, {"error": "Informe um título de 1 a 80 caracteres em JSON válido."})
            return
        self.reply(201, task)


if __name__ == "__main__":
    print("Taskboard: http://127.0.0.1:8000 | Ctrl+C encerra")
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
