# Python 3.12 ベースの公式スリムイメージ
FROM python:3.12-slim

# 必要なシステムパッケージをインストール（gcc, portaudio含む）
RUN apt-get update && \
    apt-get install -y \
        git \
        ffmpeg \
        gcc \
        libportaudio2 \
        libportaudiocpp0 \
        libasound-dev \
        portaudio19-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# pipアップグレードとパッケージインストール
RUN pip install --upgrade pip && \
    pip install git+https://github.com/openai/whisper.git pyaudio resampy sounddevice scipy

# 作業ディレクトリ作成（任意）
WORKDIR /app

CMD ["bash"]