import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from domain import create_task
from server import Handler


class DomainTests(unittest.TestCase):
    def test_valid_title(self):
        task = create_task("  Estudar testes  ")
        self.assertEqual(task["title"], "Estudar testes")
        self.assertFalse(task["done"])

    def test_distinct_ids(self):
        self.assertNotEqual(create_task("A")["id"], create_task("A")["id"])

    def test_boundaries(self):
        self.assertEqual(len(create_task("a" * 80)["title"]), 80)
        for invalid in (None, 1, [], "", "   ", "a" * 81):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                create_task(invalid)


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, body=None, headers=None):
        conn = HTTPConnection(*self.server.server_address, timeout=3)
        try:
            conn.request(method, path, body, headers or {})
            response = conn.getresponse()
            return response.status, response.read()
        finally:
            conn.close()

    def test_home(self):
        status, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b'lang="pt-BR"', body)

    def test_create(self):
        status, body = self.request("POST", "/api/tasks", json.dumps({"title":"Ler"}))
        self.assertEqual(status, 201)
        self.assertEqual(json.loads(body)["title"], "Ler")

    def test_bad_input(self):
        for body in ('{"title":" "}', '[]', '{', b'\xff'):
            with self.subTest(body=body):
                self.assertEqual(self.request("POST", "/api/tasks", body)[0], 400)

    def test_size(self):
        self.assertEqual(self.request("POST", "/api/tasks", "x" * 4097)[0], 413)

    def test_unknown_route(self):
        self.assertEqual(self.request("GET", "/missing")[0], 404)
        self.assertEqual(self.request("POST", "/missing", "{}")[0], 404)


if __name__ == "__main__":
    unittest.main()
