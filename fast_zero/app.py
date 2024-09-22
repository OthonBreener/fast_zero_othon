from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers.auth import router_auth
from fast_zero.routers.users import router_users

app = FastAPI()
app.include_router(router_users)
app.include_router(router_auth)


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root():
    html = """
    <html>
        <head>
            <title>Fast Zero</title>
        </head>
        <body>
            <h1>Hello World</h1>
            <p>Fast Zero</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)
