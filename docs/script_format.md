# HD2Dmaker 台本フォーマット仕様 v1.0

## 概要
`automation_script.txt` は1行1コマンドのシンプルなテキスト形式。
BAKINのNewScript.cs（ディレクター）がリアルタイムで読み取り実行する。

## ファイル場所
- 台本: `c:\repos\HD2Dmaker\output\automation_script.txt`
- ログ: `c:\repos\HD2Dmaker\output\automation_log.txt`

## 基本構文
```
COMMAND [target] [arg1] [arg2] ...
```
- 行頭が `#` の行はコメント（無視）
- 空行は無視
- 文字列に空白を含む場合は `"` で囲む

---

## コマンド一覧

### 移動系

#### MOVE - キャラクター移動
```
MOVE <target> <dx> <dz> [speed]
```
- `target`: `player` または キャラクターID
- `dx`: X方向の移動量（正=右、負=左）
- `dz`: Z方向の移動量（正=奥、負=手前）
- `speed`: 移動速度（省略時=1.0）

例:
```
MOVE player 3 0        # プレイヤーを右に3マス
MOVE player 0 -2       # プレイヤーを手前に2マス
MOVE npc01 -1 1 0.5    # NPC01を左奥にゆっくり移動
```

#### TELEPORT - 瞬間移動
```
TELEPORT <target> <x> <y> <z>
```
例:
```
TELEPORT player 10 0 15
```

#### FACE - 向き変更
```
FACE <target> <direction>
```
- `direction`: `up`, `down`, `left`, `right` または角度（0-359）

例:
```
FACE player down
FACE npc01 left
```

---

### 会話・UI系

#### SAY - 会話表示
```
SAY <speaker> "<message>"
```
- `speaker`: 話者名（表示用）。`_` で空白に変換
- `message`: セリフ（ダブルクォートで囲む）

例:
```
SAY 勇者 "ここが魔王の城か..."
SAY ??? "誰だ！侵入者め！"
SAY _ "（静寂が辺りを包む）"
```

#### CHOICE - 選択肢
```
CHOICE "<option1>" "<option2>" [option3] [option4]
```
選択結果は変数 `LAST_CHOICE` に格納（0,1,2,3）

---

### カメラ系

#### CAMERA_MOVE - カメラ移動
```
CAMERA_MOVE <x> <y> <z> <duration>
```
例:
```
CAMERA_MOVE 0 5 -3 2.0   # 2秒かけてカメラを上後方へ
```

#### CAMERA_ZOOM - ズーム
```
CAMERA_ZOOM <scale> <duration>
```
例:
```
CAMERA_ZOOM 1.5 1.0      # 1秒で1.5倍ズーム
CAMERA_ZOOM 1.0 0.5      # 0.5秒で元に戻す
```

#### CAMERA_FOLLOW - 追従対象設定
```
CAMERA_FOLLOW <target>
```
例:
```
CAMERA_FOLLOW player
CAMERA_FOLLOW npc_boss
```

#### CAMERA_SHAKE - カメラ揺れ
```
CAMERA_SHAKE <intensity> <duration>
```
例:
```
CAMERA_SHAKE 3 0.5       # 強度3で0.5秒揺らす
```

---

### 演出系

#### FLASH - 画面フラッシュ
```
FLASH <r> <g> <b> <duration>
```
例:
```
FLASH 255 255 255 0.1    # 白フラッシュ（雷）
FLASH 255 0 0 0.3        # 赤フラッシュ（ダメージ）
```

#### FADE - フェード
```
FADE <type> <duration>
```
- `type`: `in`, `out`, `white_in`, `white_out`

例:
```
FADE out 1.0             # 1秒で暗転
FADE in 0.5              # 0.5秒でフェードイン
```

#### EFFECT - エフェクト再生
```
EFFECT <effect_name> <x> <y> <z>
```
例:
```
EFFECT explosion 5 0 10
EFFECT magic_circle player
```

#### SOUND - 効果音
```
SOUND <sound_name>
```
例:
```
SOUND sword_slash
SOUND thunder
```

#### BGM - BGM制御
```
BGM <command> [name] [fade_time]
```
- `command`: `play`, `stop`, `fade`

例:
```
BGM play battle_theme
BGM fade 2.0
BGM stop
```

---

### 制御系

#### WAIT - 待機
```
WAIT <seconds>
```
例:
```
WAIT 1.5                 # 1.5秒待機
```

#### PARALLEL - 並列実行開始
```
PARALLEL
```
以降のコマンドを同時実行。ENDPARALLELまで。

#### ENDPARALLEL - 並列実行終了
```
ENDPARALLEL
```

#### LABEL - ラベル定義
```
LABEL <name>
```

#### GOTO - ジャンプ
```
GOTO <label_name>
```

#### IF - 条件分岐
```
IF <variable> <operator> <value> GOTO <label>
```
例:
```
IF LAST_CHOICE == 0 GOTO choice_a
IF hp < 10 GOTO low_hp
```

#### END - 台本終了
```
END
```

---

## サンプル台本

```
# 洋館イベント - 雷鳴と不気味な声

FADE in 1.0
WAIT 0.5

# 雷演出
FLASH 255 255 255 0.1
WAIT 0.1
FLASH 255 255 255 0.2
SOUND thunder
CAMERA_SHAKE 2 0.3

SAY 冒険者 "うわっ！すごい雷だ..."
WAIT 0.3

# 不気味な声
SAY ??? "...だ...れ...だ..."
CAMERA_SHAKE 1 1.0
MOVE player 0 -1

SAY 冒険者 "誰だ！？姿を見せろ！"

# クライマックス
FLASH 200 0 0 0.5
SAY ??? "...帰...れ..."
CAMERA_SHAKE 5 0.5
CAMERA_ZOOM 1.3 0.3

SAY 冒険者 "退却だ！逃げるぞ！！"
MOVE player 0 -3 2.0

FADE out 1.0
END
```
