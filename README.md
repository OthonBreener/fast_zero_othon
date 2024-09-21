Modo de execução:

```shell
fastapi dev fast_zero/app.py
```

Instalar dependencia para desenvolvimento, usa o --group dev para instalar a dependencia apenas para desenvolvimento, sem afetar o ambiente de produção

```shell
poetry add --group dev ruff
```

Para usar o taskipy para rodar as tasks, exemplo:

```shell
task run
```

Para formatar o código:

```shell
task format
```

Para rodar os testes:

```shell    
task test
```

Crie um bancos de dados postgres com a seguinte env:

```
DATABASE_URL='postgresql://postgres:postgres@localhost:5432/fastzero'
```

Para criar um docker com esse banco, basta usar o docker compose:

```shell
docker compose up --build
```

## Variáveis que devem conter no arquivo env

```
DATABASE_URL
SECRETY_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```