import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

ARQUIVO = "inventory.json"

# Datos de ejemplo
itens_iniciais = [
    {"id": 1, "nome": "Luvas cirúrgicas", "descricao": "Luvas estéreis tamanho M", "quantidade": 50, "categoria": "Materiais descartáveis", "local": "Quirófano Ceye", "ultima_atualizacao": datetime.now().isoformat(), "atualizado_por": "Sistema"},
    {"id": 2, "nome": "Bisturi", "descricao": "Bisturi descartável #10", "quantidade": 20, "categoria": "Instrumentos cirúrgicos", "local": "Quirófano Ceye", "ultima_atualizacao": datetime.now().isoformat(), "atualizado_por": "Sistema"},
    {"id": 3, "nome": "Anestesia local", "descricao": "Lidocaína 2% - 10ml", "quantidade": 15, "categoria": "Medicamentos", "local": "Quirófano Ceye", "ultima_atualizacao": datetime.now().isoformat(), "atualizado_por": "Sistema"},
]

# Crear archivo si no existe
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(itens_iniciais, f, ensure_ascii=False, indent=2)

def carregar():
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar(itens):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/items":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            itens = carregar()
            self.wfile.write(json.dumps(itens, ensure_ascii=False).encode())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/items":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            dados = json.loads(body)
            itens = carregar()
            novo_id = max([i["id"] for i in itens], default=0) + 1
            dados["id"] = novo_id
            dados["ultima_atualizacao"] = datetime.now().isoformat()
            itens.append(dados)
            salvar(itens)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(dados, ensure_ascii=False).encode())

    def do_PUT(self):
        if self.path.startswith("/items/"):
            item_id = int(self.path.split("/")[-1])
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            dados = json.loads(body)
            itens = carregar()
            for item in itens:
                if item["id"] == item_id:
                    item["quantidade"] = dados.get("quantidade", item["quantidade"])
                    item["atualizado_por"] = dados.get("updated_by", item["atualizado_por"])
                    item["ultima_atualizacao"] = datetime.now().isoformat()
                    salvar(itens)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item, ensure_ascii=False).encode())
                    return
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/items/"):
            item_id = int(self.path.split("/")[-1])
            itens = carregar()
            itens = [i for i in itens if i["id"] != item_id]
            salvar(itens)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

print("Servidor rodando em http://localhost:8000")
HTTPServer(("localhost", 8000), Handler).serve_forever()
