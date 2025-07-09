
import os
import subprocess
import whisper

# 現在の作業ディレクトリを確認
print("現在の作業ディレクトリ:", os.getcwd())

# FFmpegのインストール確認
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False

if not check_ffmpeg():
    print("FFmpegがインストールされていないか、PATHに追加されていません。")
    print("FFmpegをインストールし、PATHに追加してから再試行してください。")
else:
    # 音声ファイルの絶対パスを指定
    audio_file = os.path.join(os.getcwd(), "output.wav")

    # ファイルの存在を確認
    if os.path.isfile(audio_file):
        print("ファイルが存在します:", audio_file)
        
        # モデルのロード
        model = whisper.load_model("base")

        try:
            # 音声ファイルの文字起こし
            result = model.transcribe(audio_file)

            # 結果の表示
            print(result["text"])
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            print("エラーの詳細:")
            import traceback
            traceback.print_exc()
    else:
        print("ファイルが見つかりません:", audio_file)
