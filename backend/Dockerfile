FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

# タイムゾーンの質問をスキップする設定
ENV DEBIAN_FRONTEND=noninteractive

# OpenCVとDeepLSDに必要なシステムライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# DeepLSDのインストール（quickstart版：推論のみ）
RUN git clone --recurse-submodules https://github.com/cvg/DeepLSD.git /opt/DeepLSD \
    && cd /opt/DeepLSD \
    && pip install -e .

# 事前学習済みモデルのダウンロード（直接.pthファイルとして保存）
RUN mkdir -p /opt/DeepLSD/weights \
    && curl -L -o /opt/DeepLSD/weights/deeplsd_wireframe.pth https://cvg-data.inf.ethz.ch/DeepLSD/deeplsd_wireframe.tar \
    && ls -la /opt/DeepLSD/weights/

ENV DEEPLSD_WEIGHTS=/opt/DeepLSD/weights/deeplsd_wireframe.pth

# ローカルのソースコードをマウントするので、開発時はCOPY . . はなくても動きますが
# コンテナ単体で動かすために記述しておきます
COPY . .

CMD ["python", "run.py", "--list"]