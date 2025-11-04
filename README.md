# Orbital Survival

宇宙空間を舞台にした2Dサバイバルゲームです。

## 概要

プレイヤーは天体を操作し、公転軌道上を生き残ることを目指します。

## 特徴

- 美しい宇宙空間の背景と惑星の軌跡
- シンプルで直感的な操作

## 要件

- Python 3.8 以上
- Pygame

## インストールと実行方法

1. **リポジトリをクローンします:**

    ```bash
    git clone https://github.com/your-username/Orbital-survival.git
    cd Orbital-survival
    ```

2. **必要なライブラリをインストールします:**

    ```bash
    pip install pygame
    ```

    *(注: `requirements.txt`を作成すると、`pip install -r requirements.txt`で一括インストールできて便利です)*

3. **ゲームを実行します:**

    ```bash
    python main.py 
    ```

    *(注: メインの実行ファイル名が異なる場合は修正してください)*

## ディレクトリ構造

```
.
├── .gitignore      # Gitの追跡対象外ファイルを指定
├── README.md       # このファイル
├── config.py       # ゲームの設定ファイル
├── main.py         # ゲームの実行ファイル (エントリーポイント)
└── game.py         # ゲームのメインロジック (※推測)
```

## 操作方法

- **[>]**: 右に移動
- **[<]**: 左に移動