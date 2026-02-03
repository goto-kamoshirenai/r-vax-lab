FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

# タイムゾーンの質問をスキップする設定
ENV DEBIAN_FRONTEND=noninteractive

# OpenCVに必要なシステムライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ローカルのソースコードをマウントするので、開発時はCOPY . . はなくても動きますが
# コンテナ単体で動かすために記述しておきます
COPY . .

CMD ["python", "LSD-1.py"]