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