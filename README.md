# Beabagre

Na fase atual, esse projeto visa realizar um CRUD completo da entidade Bagre na base de dados. A API conta com cinco endpoints para efetuar esse ciclo de operações. Os endpoints podem ser encontrados ao acessar a rota: `/docs` ou `/redoc`. Essas rotas disponibilizam toda a documentação automática da API, provinda pelo framework FastAPI.

# Configuração

Primeiramente, crie um arquivo chamado `database.db` na raiz do projeto.

Após isso, rode o comando:

```shell
uvicorn main:app --reload --port 8000
```

# Endpoints

| Endpoint| Método| Descrição|
|-|-|-|
| /bagres/| GET| Retorna uma lista paginada de todos os bagres cadastrados no sistema. A paginação retorna até 10 bagres. |
| /bagres/| POST| Salva um modelo bagre no banco a partir do body da requisição. Realiza validação nos dados fornecidos.|
| /bagres/{uuid}/ | GET| Procura um modelo na tabela de bagres que tenha o uuid especificado e o retorna como um JSON. Retorna um erro 404 se não for encontrado.|
| /bagres/{uuid}/ | PUT| Atualiza os dados de um bagre específico com base no uuid. Realiza validação nos dados fornecidos. Retorna um erro 404 se o recurso não for encontrado.  |
| /bagres/{uuid}/ | DELETE| Deleta um modelo de bagre específico da tabela do banco a partir do uuid fornecido. Retorna um erro 404 se o recurso não for encontrado.|

# Requisições

Segue a lista de alguns comandos para teste:

| Descrição| Comando|
|-|-|
| GET /bagres/| `curl http://127.0.0.1:8000/bagres/`|
| POST /bagres/ (válido)| `curl -X POST "http://127.0.0.1:8000/bagres/" -H "Content-Type: application/json" -d '{"specie": "Bagre comum", "weight": 1.5, "size": 10, "color": "azul"}'` |
| POST /bagres/ (inválido)| `curl -X POST "http://127.0.0.1:8000/bagres/" -H "Content-Type: application/json" -d '{"specie": 123, "weight": "1.5", "size": "10", "color": true}'` |
| GET /bagres/{uuid}| `curl http://127.0.0.1:8000/bagres/example_uuid`|
| PUT /bagres/{uuid} (válido)| `curl -X PUT "http://127.0.0.1:8000/bagres/example_uuid" -H "Content-Type: application/json" -d '{"specie": "Bagre atualizado", "weight": 2.0, "size": 12, "color": "vermelho"}'` |
| PUT /bagres/{uuid} (inválido)| `curl -X PUT "http://127.0.0.1:8000/bagres/example_uuid" -H "Content-Type: application/json" -d '{"specie": 123, "weight": "2.0", "size": "doze", "color": true}'` |
| DELETE /bagres/{uuid}| `curl -X DELETE http://127.0.0.1:8000/bagres/example_uuid`|
