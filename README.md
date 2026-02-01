# HD2Dmaker

BAKIN（RPG Developer Bakin）と連携して、HD2D RPGの演出を自動生成するツール

## 概要

```
┌─────────────────┐      ┌──────────────────────┐      ┌─────────────────┐
│  Python         │      │  automation_script   │      │  BAKIN          │
│  台本ジェネレータ│ ───▶ │       .txt           │ ───▶ │  NewScript.cs   │
│                 │      │  (コマンド台本)       │      │  (ディレクター)  │
└─────────────────┘      └──────────────────────┘      └─────────────────┘
```

**ユーザーはテストプレイを押すだけ！**

## クイックスタート

### 1. Python台本を生成

```python
from src.script_writer import Script, Effects

# 新しい台本を作成
s = Script()

s.comment("オープニングシーン")
s.fade_in(1.0)
s.say("勇者", "ここが魔王の城か...")
s.camera_shake(2, 0.5)
Effects.thunder(s)  # 雷演出プリセット
s.say("???", "よく来たな...")
s.end()

# 台本を保存
s.save()  # → output/automation_script.txt
```

### 2. BAKINでテストプレイ

1. BAKINプロジェクトを開く
2. マップにイベントを配置し、NewScript.csを紐付け
3. テストプレイを開始
4. 台本が自動実行される

## コマンド一覧

| コマンド | 説明 | 例 |
|---------|------|-----|
| `MOVE` | キャラ移動 | `MOVE player 3 0` |
| `TELEPORT` | 瞬間移動 | `TELEPORT player 10 0 15` |
| `FACE` | 向き変更 | `FACE player down` |
| `SAY` | 会話表示 | `SAY 勇者 "こんにちは"` |
| `WAIT` | 待機 | `WAIT 1.5` |
| `CAMERA_SHAKE` | 揺れ | `CAMERA_SHAKE 3 0.5` |
| `CAMERA_ZOOM` | ズーム | `CAMERA_ZOOM 1.5 1.0` |
| `FLASH` | フラッシュ | `FLASH 255 255 255 0.1` |
| `FADE` | フェード | `FADE out 1.0` |
| `SOUND` | 効果音 | `SOUND thunder` |
| `BGM` | BGM制御 | `BGM play battle_theme` |
| `END` | 台本終了 | `END` |

詳細は [docs/script_format.md](docs/script_format.md) を参照

## 演出プリセット

```python
from src.script_writer import Script, Effects

s = Script()
Effects.thunder(s)      # 雷演出
Effects.damage(s, 3)    # ダメージ演出
Effects.surprise(s)     # 驚き演出
Effects.dramatic_zoom(s) # ドラマチックズーム
Effects.scene_transition(s) # シーン切り替え
```

## ファイル構成

```
HD2Dmaker/
├── src/
│   ├── script_writer.py   # Python台本ジェネレーター
│   └── generator.py       # Bakinイベント形式生成（旧）
├── output/
│   ├── automation_script.txt  # メイン台本（BAKINが読む）
│   ├── automation_log.txt     # 実行ログ
│   └── *.txt                  # サンプル台本
├── docs/
│   └── script_format.md       # 台本フォーマット仕様書
└── README.md
```

## BAKIN側の設定

`script/NewScript.cs` をBAKINプロジェクトに配置：
- 場所: `[BAKINプロジェクト]/script/NewScript.cs`
- マップ上のイベントに紐付けて使用

## ホットリロード

台本ファイル（automation_script.txt）を編集して保存すると、
BAKINが自動的に再読み込みして最初から実行し直します。

## ログ確認

実行ログは `output/automation_log.txt` に出力されます：

```
[12:34:56.789] === HD2Dmaker Director Started ===
[12:34:56.800] Loading script: 25 lines
[12:34:56.801] Parsed 18 commands
[12:34:56.850] [3] FADE in 1.0
[12:34:57.900] [5] SAY 勇者 ここが魔王の城か...
...
```

## サンプル台本を生成

```bash
python src/script_writer.py
```

以下のサンプルが生成されます：
- `haunted_mansion.txt` - 洋館ホラーシーン
- `battle_intro.txt` - ボス戦イントロ
- `emotional_scene.txt` - 感動の別れシーン
