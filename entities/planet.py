# entities/planet.py

import pygame
import math

from .base import CelestialBody
from config import *

class Planet(CelestialBody):
    """
    惑星を表すクラス
    """
    # --- クラス定数 ---
    ACCELERATION = PLANET_ACCELERATION
    FRICTION = PLANET_FRICTION
    ORBIT_RADIUS = PLANET_ORBIT_RADIUS

    MAX_SPEED = ACCELERATION * FRICTION / (1 - FRICTION)
    MAX_TRAJECTORY_LENGTH = 2 * math.pi / 6
    TRAJECTORY_NUM = 60

    def __init__(self, center_pos, size, angle, radius):
        """
        Planetオブジェクトの初期化
        :param center_pos: 公転の中心座標 (x, y)
        :param size: 惑星の直径
        :param angle: 惑星の初期角度（ラジアン）
        :param radius: 公転の半径
        """
        super().__init__(
            center_pos=center_pos,
            size=size,
            acceleration=self.ACCELERATION,
            friction=self.FRICTION,
            angle=angle,
            speed=0.0
        )
        self.radius = radius # 公転の半径
        self.color = EARTH_BLUE
        
        # 表示用に、フレームごとの実際の角加速度を保持する
        self.actual_acceleration = 0.0
        
        # 最初の座標を計算し、矩形の位置を合わせる
        self.x = self.center_pos[0] + self.radius * math.cos(self.angle)
        self.y = self.center_pos[1] + self.radius * math.sin(self.angle)
        
    def update(self, direction):
        """
        惑星の状態を毎フレーム更新する
        1. 入力と摩擦を考慮して現在の速度，角度を計算
        2. 表示用の角加速度を算出
        3. 位置を更新
        :param direction: ユーザーからの入力方向 (-1: 左, 0: 無し, 1: 右)
        """
        # 実際の加速度を計算するために、更新前の速度を保存
        speed_before_update = self.speed

        # 速度，角度を更新
        self.update_angle_and_speed(direction)

        # HUD表示用の各加速度を計算
        self.actual_acceleration = self.speed - speed_before_update

        # (x,y)座標を計算
        self.x = self.center_pos[0] + self.radius * math.cos(self.angle)
        self.y = self.center_pos[1] + self.radius * math.sin(self.angle)

    def draw(self, screen):
        '''
        惑星本体と軌道の描画
        :param screen: 描画対象のPygameスクリーンオブジェクト
        '''
        # --- 軌道の描画 ---
        self.draw_trajectory(screen)

        # --- 惑星本体の描画 ---
        self.draw_planet(screen)
    
    def draw_planet(self, screen):
        """
        惑星本体を画面に描画する
        :param screen: 描画対象のPygameスクリーンオブジェクト
        """

        # --- 本体（ボール）の描画 ---
        # 惑星本体（黒い円）を描画
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size)
        # 惑星の縁（青色の枠）を描画
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, CIRCLE_WIDTH)  # 幅2の枠

    def draw_trajectory(self, screen):
        """
        惑星の軌道を画面に描画する
        :param screen: 描画対象のPygameスクリーンオブジェクト
        """
        for n in range(self.TRAJECTORY_NUM):
            tjy_angle = self.angle - self.MAX_TRAJECTORY_LENGTH * (self.speed / self.MAX_SPEED) * (n / self.TRAJECTORY_NUM)
            tjy_x = self.center_pos[0] + self.radius * math.cos(tjy_angle)
            tjy_y = self.center_pos[1] + self.radius * math.sin(tjy_angle)
            tjy_size = self.size * (1 - n / self.TRAJECTORY_NUM)
            tjy_color = tuple(int(c * math.sqrt(1 - n / self.TRAJECTORY_NUM)) for c in self.color)
            pygame.draw.circle(screen, tjy_color, (int(tjy_x), int(tjy_y)), int(tjy_size))