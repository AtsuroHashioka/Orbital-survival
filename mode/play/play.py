# mode/play/play.py

import pygame
import math


from config import *
from entities.planet import Planet
from entities.star import Star
from entities.beam import BeamCorpse
from mode.play.ui.button import Button
from mode.play.ui.hud import HUD

class Play:
    """
    PLAYモードを管理するクラス
    """

    def __init__(self, screen, clock):
        """
        Playオブジェクトの初期化
        """
       
        # 画面の設定
        self.screen = screen
        # 時間管理用のClockオブジェクト
        self.clock = clock

    def initialize_play_state(self):
        """ゲームの状態を初期化する。"""
        self.start_time = pygame.time.get_ticks() # 経過時間の初期化

        # --- オブジェクトの生成 ---
        # Planetオブジェクトを生成
        self.planet = Planet(CENTER_POS, PLANET_SIZE, PLANET_INITIAL_ANGLE, PLANET_ORBIT_RADIUS)
        # Starオブジェクトを生成
        self.star = Star(CENTER_POS, STAR_SIZE)
        # 円形ボタンを画面左右中心に配置
        self.left_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 80, BUTTON_RADIUS, 'left')
        self.right_button = Button(SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 80, BUTTON_RADIUS, 'right')
        # HUDオブジェクトを生成
        self.hud = HUD()
        self.left_active = False
        self.right_active = False
        self.score = 0
        self.kill_count = 0
        self.corpses = []

    def update(self):
        """
        ゲーム内の各オブジェクトの状態を更新する
        """
        # --- 惑星の操作（キーボードとマウスの両方に対応） ---
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # 左方向への加速判定 (左キー or 左ボタンクリック)
        self.left_active = keys[pygame.K_LEFT] or \
                                (mouse_buttons[0] and self.left_button.is_clicked(mouse_pos))
        # 右方向への加速判定 (右キー or 右ボタンクリック)
        self.right_active = keys[pygame.K_RIGHT] or \
                                (mouse_buttons[0] and self.right_button.is_clicked(mouse_pos))

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

    def draw(self):
        """
        画面に各オブジェクトを描画する
        """

        for corpse in self.corpses:
            corpse.draw(self.screen)
        
        self.star.draw(self.screen)
        self.planet.draw(self.screen)
        
        self.left_button.draw(self.screen, self.left_active)
        self.right_button.draw(self.screen, self.right_active)

        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.hud.draw(self.screen, self.planet.speed, self.planet.actual_acceleration, self.kill_count, self.score, elapsed_time)
