## Docker 立ち上げ

1. ターミナルで下記をたたいて ubuntu を起動

```
wsl
```

2. コンテナを起動

```
docker compose up --build -d
```

```
docker compose exec backend python main.py
```
