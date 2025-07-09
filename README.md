# LFBA_whisper
LFBA × whisperの研究リポジトリです。

## 環境構築
コンテナのビルド：
```bash
docker build -t whisper-python312 .
```
コンテナ内でコードの実行
```bash
docker run -it --rm --device /dev/snd -v "$PWD":/app whisper-python312 python <file_name>
```
