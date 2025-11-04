# entities/base.py

import pygame

# --- 基底クラス ---

class CelestialBody:
    """惑星や恒星など、回転する天体の基底クラス。"""
    def __init__(self, center_pos, size, acceleration, friction, initial_angle, initial_speed):
        self.center_pos = center_pos
        self.size = size
        self.x = center_pos[0]
        self.y = center_pos[1]
        self.angle = initial_angle
        self.speed = initial_speed
        self.acceleration = acceleration
        self.friction = friction

    def apply_physics(self, direction=0):
        """物理法則（加速と摩擦）を適用して速度と角度を更新する。"""
        self.speed += self.acceleration * direction
        self.speed *= self.friction
        self.angle += self.speed

class BaseArc:
    """円弧を描画するオブジェクト（光線やその死体）の基底クラス。"""
    def __init__(self, center_pos, angle, arc_range, radius, width, color):
        self.center_pos = center_pos
        self.angle = angle
        self.arc_range = arc_range
        self.radius = radius
        self.width = width
        self.color = color

    def update(self):
        """状態を更新する。サブクラスで実装。"""
        raise NotImplementedError

    def is_alive(self):
        """生存しているか。サブクラスで実装。"""
        raise NotImplementedError

    def draw_arc(self, screen, current_color, draw_width):
        """指定された色と幅で円弧を描画する。"""
        if draw_width > 0:
            start_angle = self.angle - self.arc_range / 2
            end_angle = self.angle + self.arc_range / 2
            rect = pygame.Rect(int(self.center_pos[0] - self.radius), int(self.center_pos[1] - self.radius), int(self.radius * 2), int(self.radius * 2))
            pygame.draw.arc(screen, current_color, rect, start_angle, end_angle, draw_width)