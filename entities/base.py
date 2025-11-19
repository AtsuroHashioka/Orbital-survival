# entities/base.py

import pygame

from config import *

# --- 基底クラス ---

class CelestialBody:
    """惑星や恒星など、回転する天体の基底クラス。"""

    # --- クラス定数 ---
    ACCELERATION = ACCELERATION
    FRICTION = FRICTION
    MAX_SPEED = ACCELERATION * FRICTION / (1 - FRICTION)

    def __init__(self, center_pos, size, acceleration, friction, angle, speed):
        self.center_pos = center_pos # 天体の中心座標 (x, y)
        self.size = size # 天体のサイズ
        self.angle = angle # 天体の角度
        self.speed = speed # 天体の角速度
        self.acceleration = acceleration # 天体の角加速度
        self.friction = friction # 天体の減速率

    def update_angle_and_speed(self, direction):
        """
        物理法則（加速と摩擦）を適用して速度と角度を更新する。
        param direction: 加速度の方向（1: 正方向, -1: 負方向）
        """
        self.speed += self.acceleration * direction # 加速度から速度を更新
        self.speed *= self.friction # 減速率を適用
        self.angle += self.speed # 速度から角度を更新

class BaseArc:
    """円弧を描画するオブジェクト（光線やその死体）の基底クラス。"""
    def __init__(self, center_pos, angle, arc_range, radius, width, color):
        self.center_pos = center_pos # 円弧の中心座標 (x, y)
        self.angle = angle # 円弧の中心角度
        self.arc_range = arc_range # 円弧の角度範囲
        self.radius = radius # 円弧の半径
        self.width = width # 円弧の線の幅
        self.color = color # 円弧の色

    def update(self):
        """状態を更新する。サブクラスで実装。"""
        raise NotImplementedError

    def is_alive(self):
        """生存しているか。サブクラスで実装。"""
        raise NotImplementedError

    def draw_arc(self, screen, color, draw_width):
        """
        指定された色と幅で円弧を描画する。
        param screen: 描画先の画面
        param color: 描画する色
        param draw_width: 描画する線の幅
        """
        if draw_width > 0:
            # 円弧の開始角度と終了角度を計算
            start_angle = self.angle - self.arc_range / 2
            end_angle = self.angle + self.arc_range / 2

            # 円弧を描画するための矩形を作成
            rect = pygame.Rect(int(self.center_pos[0] - self.radius), int(self.center_pos[1] - self.radius), int(self.radius * 2), int(self.radius * 2))
            pygame.draw.arc(screen, color, rect, start_angle, end_angle, draw_width)