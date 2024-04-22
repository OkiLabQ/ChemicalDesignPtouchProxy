# PtouchProxy
九州大学薬品登録システム `Chemical Design` のptouch非対応プリンター用プロキシサーバー

## 使い方

現状Windowsのみ対応

### 依存関係のインストール

```powershell
py -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

### 設定方法

`.env` ファイルを作成し、設定を記述する。
以下は例

```sh
PRINTERNAME="KL-M30"
AFFILIATION="XX MMMMM部門"
LABORATORY="XX OO研究室"
```

### プロキシの立ち上げ

```powershell
./.venv/Scripts/Activate.ps1
python ./main.py
```
