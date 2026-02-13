## Docker 立ち上げ

1. ターミナルで下記をたたいて ubuntu を起動

```
wsl
```

2. コンテナを起動

```
docker compose up --build -d
```

3. コンテナを維持

```
docker compose up -d
```

# イメージを再ビルド

```
docker compose build --no-cache
```

# 利用可能な検出器を一覧表示

docker compose exec backend python run.py --list

# 古典的 LSD で実行

```
docker compose exec backend python run.py -d lsd_classic
```

# DeepLSD で実行

```
docker compose exec backend python run.py -d deeplsd
```

# すべての検出器で実行（比較）

```
docker compose exec backend python run.py --all
```
