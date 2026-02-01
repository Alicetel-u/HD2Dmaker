# BAKIN C# Scripting API ガイド

## 座標系 (Bakin Standard)

```
        Z- (奥/北)
           ↑
           |
X- (左) ←─┼─→ X+ (右)
           |
           ↓
        Z+ (手前/南)
```

## 方向角度

| 方向 | 角度 | ベクトル |
|-----|------|---------|
| UP (奥/北) | 0° | (0, 0, -1) |
| LEFT (左) | 90° | (-1, 0, 0) |
| DOWN (手前/南) | 180° | (0, 0, +1) |
| RIGHT (右) | 270° | (+1, 0, 0) |

## 必須パターン

### 1. 移動: Lerp over Physics

```csharp
// NG: 物理移動（滑る、震える）
hero.Move(vx, vz, 0, false);

// OK: Lerp補間
Vector3 newPos = Vector3.Lerp(startPos, endPos, rate);
hero.setPosition(newPos);
```

### 2. カメラ同期 (必須)

```csharp
hero.setPosition(newPos);
mapScene.SyncCamera();  // これがないとカメラが置いていかれる
```

### 3. 向き強制 (カニ歩き防止)

```csharp
// setDirection(角度, 即時回転, 強制)
hero.setDirection(angle, true, true);
```

### 4. アニメーション強制 (毎フレーム)

```csharp
// Update内で毎フレーム呼ぶ
hero.playMotion("walk");
```

## 完全な移動ループ

```csharp
private void UpdateWalk()
{
    var hero = mapScene.hero;
    if (hero == null) return;

    // 1. 向き強制
    hero.setDirection(currentDirectionAngle, true, true);

    // 2. アニメ強制
    hero.playMotion("walk");

    // 3. 進捗計算
    walkProgress += 0.0166f;
    float rate = walkProgress / walkTotalDuration;

    if (rate >= 1.0f)
    {
        // 4a. 完了
        hero.setPosition(walkEndPos);
        mapScene.SyncCamera();
        isWalking = false;
        hero.playMotion("wait");
    }
    else
    {
        // 4b. Lerp移動
        Vector3 newPos = Vector3.Lerp(walkStartPos, walkEndPos, rate);
        hero.setPosition(newPos);
        mapScene.SyncCamera();
    }
}
```

## 利用可能なモーション

- `wait` - 待機
- `walk` - 歩行
- `run` - 走り
- `praise` - 賞賛/喜び
- `damage` - ダメージ
- その他はキャラクター設定に依存
