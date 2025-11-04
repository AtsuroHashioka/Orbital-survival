# entities/planet.py

import pygame
import math
import collections

from .base import CelestialBody
from config import EARTH, BLACK, TRAIL_MAX_LENGTH

class Planet(CelestialBody):
    """
    惑星を表すクラス
    """
    # --- クラス定数 ---
    SIZE = 12
    ACCELERATION = 0.0010
    FRICTION = 0.99
    MAX_SPEED = (ACCELERATION * FRICTION) / (1 - FRICTION) if (1 - FRICTION) != 0 else 0
    INITIAL_ANGLE = math.pi / 2
    TRAIL_INTERPOLATION_STEP = SIZE * 0.75

    def __init__(self, center_pos, size):
        """
        Planetオブジェクトの初期化
        :param center_pos: 公転の中心座標 (x, y)
        """
        super().__init__(
            center_pos=center_pos,
            size=size,
            acceleration=self.ACCELERATION,
            friction=self.FRICTION,
            initial_angle=self.INITIAL_ANGLE,
            initial_speed=0.0
        )
        self.radius = 225             # 公転の半径
        self.color = EARTH
        # 残像効果のための座標履歴 (固定長キュー)
        self.history = collections.deque(maxlen=TRAIL_MAX_LENGTH)
        
        # 表示用に、フレームごとの実際の角加速度を保持する
        self.actual_acceleration = 0.0
        
        # 最初の座標を計算し、矩形の位置を合わせる
        self.x = self.center_pos[0] + self.radius * math.cos(self.angle)
        self.y = self.center_pos[1] + self.radius * math.sin(self.angle)
    def update(self, direction):
        """
        惑星の状態を毎フレーム更新する
        1. 1フレーム前の速度を記憶
        2. 入力と摩擦を考慮して現在の速度を計算
        3. 実際の角加速度を算出
        4. 角度と位置を更新
        :param direction: ユーザーからの入力方向 (-1: 左, 0: 無し, 1: 右)
        """
        # 実際の加速度を計算するために、更新前の速度を保存
        speed_before_update = self.speed

        self.apply_physics(direction)

        # 1フレーム間での実際の速度変化（=角加速度）を計算
        self.actual_acceleration = self.speed - speed_before_update

        # --- 軌道補間処理 ---
        # 1フレームでの移動距離(円弧の長さ)を計算
        arc_length = abs((self.speed - speed_before_update) * self.radius)
        # 移動距離に基づいて、このフレームでいくつの点を描画すべきか計算
        num_steps = int(arc_length / self.TRAIL_INTERPOLATION_STEP) + 1
        
        # 1ステップあたりの角度の変化量を計算
        step_angle = (self.speed - speed_before_update) / num_steps

        # 計算されたステップ数だけループし、中間点を履歴に追加
        for _ in range(num_steps):
            self.angle += step_angle
            # 新しいx, y座標を三角関数で計算
            self.x = self.center_pos[0] + self.radius * math.cos(self.angle)
            self.y = self.center_pos[1] + self.radius * math.sin(self.angle)
            self.history.append((self.x, self.y)) # 座標を履歴に追加

    def draw(self, screen):
        """
        惑星と速度に応じた残像を画面に描画する
        :param screen: 描画対象のPygameスクリーンオブジェクト
        """
        # --- 描画する残像の長さを決定 ---
        speed_ratio = min(abs(self.speed) / self.MAX_SPEED, 1.0) if self.MAX_SPEED > 0 else 0
        visible_trail_length = int(TRAIL_MAX_LENGTH * speed_ratio)

        # 描画対象の履歴を取得 (dequeの末尾からスライス)
        visible_history = list(self.history)[-visible_trail_length:]
        num_points = len(visible_history)

        # --- 残像の描画 ---
        for i, pos in enumerate(visible_history):
            # i=0が最も古く、iが大きくなるほど新しくなる
            # 新しいものほど明るく、大きくなるように比率を計算 (2乗して自然な減衰に)
            ratio = (i / (num_points - 1)) ** 2 if num_points > 1 else 0
            
            # 色を計算 (青みがかった色に変更。だんだん明るくなる)
            blue_value = int(100 + 100 * ratio)  # 青色の成分を調整
            trail_color = (0, 0, blue_value)  # RGB: (0, 0, 青の濃さ)


            # サイズを計算 (古いものは20%のサイズから始まり、徐々に大きくなる)
            # ratioが0のとき0.2倍、ratioが1のとき1.0倍になる
            trail_size = self.size * (0.2 + ratio * 0.8)

            # サイズが1ピクセル未満の場合は描画しない
            if trail_size < 1:
                continue

            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), int(trail_size))

        # --- 本体（ボール）の描画 ---
        # 惑星本体（黒い円）を描画
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size)
        # 惑星の縁（青色の枠）を描画
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, 2)  # 幅2の枠