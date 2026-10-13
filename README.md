# API CRUD de Livros - FastAPI + MongoDB

Atividade prática de desenvolvimento de uma API REST utilizando Python, FastAPI e MongoDB.

## Integrantes da Dupla
- Arthur da Rosa Larcerda
- Jefferson Carneiro

## Tecnologias Utilizadas
- **Python 3**
- **FastAPI**: Framework para construção das rotas e validação de dados.
- **MongoDB + PyMongo**: Banco de dados NoSQL e driver de conexão.
- **Uvicorn**: Servidor local para rodar a aplicação.

## Como executar o projeto

1. Clone este repositório:
   `git clone https://github.com/ReyArthur/Desenvolvimento-de-API-CRUD.git`

2. Instale as dependências:
   `pip install -r requirements.txt`

3. Certifique-se de ter o MongoDB rodando localmente na porta 27017 (ou altere a string de conexão no `main.py`).

4. Inicie o servidor:
   `uvicorn main:app --reload`

5. Acesse a documentação do Swagger interativa no navegador:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Explicação do Código
- Utilizamos o **Pydantic** para validar a entrada de dados (título, autor, ano, preço).
- Criamos uma função auxiliar (`livro_helper`) para converter o `ObjectId` padrão do MongoDB em uma `string` legível para o formato JSON.
- A API retorna códigos HTTP adequados: `201` para criação, `200` para sucesso, `204` para exclusão sem retorno e `404` para não encontrado.
