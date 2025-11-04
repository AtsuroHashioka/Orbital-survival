# entities/star.py

import pygame
import math
import random

from .base import CelestialBody
from .beam import Beam
from config import SUN, BLACK, FPS

class Star(CelestialBody):
    """
    恒星を表すクラス
    """
    # --- クラス定数 ---
    ACCELERATION = 0.0010   # 恒星の角加速度
    FRICTION = 0.99         # 恒星の摩擦

    def __init__(self, center_pos, size):
        """
        Starオブジェクトの初期化
        :param center_pos: 恒星の中心座標 (x, y)
        :param size: 恒星の直径
        """
        super().__init__(
            center_pos=center_pos,
            size=size,
            acceleration=self.ACCELERATION,
            friction=self.FRICTION,
            initial_angle=random.uniform(0, 2 * math.pi),
            initial_speed=random.uniform(-0.005, 0.005)
        )
        self.color = SUN
        self.arc_range = math.pi * 60 / 360  # 黒い円弧の描画範囲

        # ランダム制御用のタイマーと現在の進行方向
        self.random_timer = 0
        self.random_direction = 0
        self.beam_timer = 0
        
        # 砲台の発光を制御するためのタイマー
        self.cannon_flash_timers = [0, 0, 0]
        self.beams = [] # 発射した光線を管理するリスト
        self.cannon_initial_radius = self.size               # 砲台の初期半径を保存
        self.cannon_radii = [self.cannon_initial_radius] * 3 # 各砲台の半径

    def update(self):
        """
        ランダムに恒星の自転（位相）を更新し、光線を発射する。
        """
        # 光線の更新と削除
        for beam in self.beams[:]: # コピーをループして、ループ中に安全に削除
            beam.update()
            if not beam.is_alive():
                self.beams.remove(beam)

        self.random_timer += 1
        self.beam_timer += 1

        # 加速度をランダムに変更
        if self.random_timer >= FPS // 8:
            self.random_timer = 0
            # 加速度0を選ぶ確率を20%、左右をそれぞれ40%に設定
            self.random_direction = random.choices([-1, 0, 1], weights=[40, 20, 40], k=1)[0]

        # 光線を発射
        if self.beam_timer >= FPS // 8:
            self.beam_timer = 0
            # 3つの砲台から光線を発射
            for i in range(3):  
                if random.random() < 0.20: # 20%の確率で発射
                    cannon_angle = self.angle + (2 * math.pi / 3) * i
                    beam = Beam(self.center_pos, cannon_angle, self.arc_range, self.size, int(self.size // 4))
                    self.beams.append(beam)
                    # 発射エフェクト：対応する砲台の半径を一時的に小さくする
                    self.cannon_radii[i] = self.cannon_initial_radius * 0.75

        # 各砲台の半径を徐々に初期サイズに戻す
        for i in range(3):
            if self.cannon_radii[i] < self.cannon_initial_radius:
                self.cannon_radii[i] += 0.5  # 半径の回復速度
                # 初期半径を超えないように補正
                if self.cannon_radii[i] > self.cannon_initial_radius:
                    self.cannon_radii[i] = self.cannon_initial_radius

        self.apply_physics(self.random_direction)
        
    def draw(self, screen):
        """
        恒星、砲台、光線を画面に描画する
        :param screen: 描画対象のPygameスクリーンオブジェクト
        """
        # 発射された光線を描画 (恒星より奥にあるように見せるため先に描画)
        for beam in self.beams:
            beam.draw(screen)

        # 恒星本体（黒い円）を描画
        pygame.draw.circle(screen, BLACK, self.center_pos, self.size / 2)
        # 恒星の縁（オレンジ色の枠）を描画
        pygame.draw.circle(screen, self.color, self.center_pos, self.size / 2, 2)  # 幅2の枠

        # 次に、angle付近に砲台を描画します
        for i in range(3):  # 3つの砲台を描画
            arc_radius = self.cannon_radii[i] # 各砲台の半径を使用
            # 位相を3等分
            cannon_angle = self.angle + (2 * math.pi / 3) * i  
            start_angle = cannon_angle - self.arc_range / 2
            end_angle = cannon_angle + self.arc_range / 2
            rect = pygame.Rect(self.center_pos[0] - arc_radius, self.center_pos[1] - arc_radius, arc_radius * 2, arc_radius * 2)
            pygame.draw.arc(screen, self.color, rect, start_angle, end_angle, int(self.size // 4))