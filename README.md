<h2>게시판 API</h2>

* Project Structure
``` bash
├── Dockerfile
├── alembic.ini
├── app.py
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── poetry.lock
├── pyproject.toml
├── src
│   ├── config.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── users.py
│   ├── modules
│   │   ├── cache.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── pagination.py
│   │   └── utils.py
│   └── services
│       ├── admin.py
│       ├── auth.py
│       ├── request.py
│       └── users.py
└── start_server.sh
```
--------------------------

* Requirements
``` bash
aiomysql==0.2.0
alembic==1.13.2
annotated-types==0.7.0
anyio==4.4.0
bcrypt==4.2.0
Brotli==1.1.0
brotli-asgi==1.4.0
certifi==2024.7.4
click==8.1.7
dnspython==2.6.1
ecdsa==0.19.0
email_validator==2.2.0
fastapi==0.111.1
fastapi-cli==0.0.4
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.5
httptools==0.6.1
httpx==0.27.0
idna==3.7
Jinja2==3.1.4
Mako==1.3.5
markdown-it-py==3.0.0
MarkupSafe==2.1.5
mdurl==0.1.2
passlib==1.7.4
pyasn1==0.6.0
pydantic==2.8.2
pydantic-settings==2.3.4
pydantic_core==2.20.1
Pygments==2.18.0
PyMySQL==1.1.1
python-dotenv==1.0.1
python-jose==3.3.0
python-multipart==0.0.9
PyYAML==6.0.1
redis==5.0.7
rich==13.7.1
rsa==4.9
shellingham==1.5.4
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.31
starlette==0.37.2
typer==0.12.3
typing_extensions==4.12.2
ua-parser==0.18.0
user-agents==2.2.0
uvicorn==0.30.3
uvloop==0.19.0
watchfiles==0.22.0
websockets==12.0
```
