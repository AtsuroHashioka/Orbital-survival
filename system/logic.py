# system/logic.py

import math

from config import *
from entities.planet import Planet
from entities.star import Star
from entities.beam import BeamCorpse

class Logic:
    """
    ゲームのロジックを管理するクラス
    """

    def __init__(self):
        """
        Systemオブジェクトの初期化
        param center_pos: 惑星と恒星の中心位置 (x, y)
        param planet_size: 惑星のサイズ(半径)
        param planet_initial_angle: 惑星の初期角度
        param planet_orbit_radius: 惑星の公転半径
        param star_size: 恒星のサイズ(半径)
        """
        # --- オブジェクトの生成 ---
        # Planetオブジェクトを生成
        self.planet = Planet(CENTER_POS, PLANET_SIZE, PLANET_INITIAL_ANGLE, PLANET_ORBIT_RADIUS)
        # Starオブジェクトを生成
        self.star = Star(CENTER_POS, STAR_SIZE)

        # 方向ボタンの状態
        self.left_active = False
        self.right_active = False

        # 光線の死体リスト
        self.corpses = []
        # スコアとキルカウント
        self.score = 0 
        self.kill_count = 0

    def update(self):
        """
        ゲーム内の各オブジェクトの状態を更新する
        """

        # 加速方向を決定
        direction = 0
        if self.left_active:
            direction = 1
        elif self.right_active:
            direction = -1

        # 決定した方向を渡して惑星の状態を更新
        self.planet.update(direction)
        # 恒星の状態をAIに基づいて更新
        self.star.update()
        # 死体の更新
        self.update_corpses()

        # 衝突の判定とビームの削除
        self.check_collisions()

    def update_corpses(self):
        """光線の死体を更新し、寿命が尽きたものを削除する"""
        for corpse in self.corpses:
            corpse.update()
        self.corpses = [c for c in self.corpses if c.is_alive()]

    def check_collisions(self):
        """惑星と光線の衝突を判定する"""
        planet_angle = self.planet.angle
        planet_orbit_radius = self.planet.radius
        planet_size = self.planet.size

        # 衝突判定のための角度のマージンを計算
        if planet_orbit_radius > planet_size:
            angle_margin = math.asin(planet_size / planet_orbit_radius)
        else:
            angle_margin = math.pi

        # ビームと惑星の衝突を判定し、衝突したビームを死体リストに追加し、生き残ったビームはリストに保持
        surviving_beams = [] # 生き残ったビームのリスト
        for beam in self.star.beams:
            beam_front_radius = beam.radius + beam.width + self.planet.size 
            beam_back_radius = max(0, beam.radius - beam.width - self.planet.size)

            collided = False
            if beam_back_radius < planet_orbit_radius < beam_front_radius:
                angle_diff = (planet_angle + beam.angle + math.pi) % (2 * math.pi) - math.pi

                if abs(angle_diff) < beam.arc_range / 2 + angle_margin:
                    self.kill_count += 1
                    self.score -= 200
                    # 衝突したビームの死体を追加
                    self.corpses.append(BeamCorpse(beam.center_pos, beam.angle, beam.arc_range, beam.radius, beam.width))
                    collided = True
            elif beam.radius > planet_orbit_radius and not beam.dodged:
                self.score += 10
                beam.dodged = True
            
            if not collided:
                # 生き残ったビームとしてリストに追加
                surviving_beams.append(beam)

        # 恒星のビームリストを更新(生き残ったビームのみを保持)
        self.star.beams = surviving_beams