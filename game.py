# game.py

import pygame
import sys
import math
import random
import numpy as np

from config import *
from entities.planet import Planet
from entities.star import Star
from entities.beam import BeamCorpse
from ui.button import Button
from ui.hud import HUD

class Game:
    """
    ゲーム全体を管理するメインクラス
    """
    # 強化学習エージェントが観測するビームの数
    NUM_OBSERVED_BEAMS = 5

    def __init__(self):
        """
        Gameオブジェクトの初期化
        """
        # Pygameの初期化
        pygame.init()
        # 画面の設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ORBITAL SURVIVAL")
        # 時間管理用のClockオブジェクト
        self.clock = pygame.time.Clock()
        self.is_running = True # 人間がプレイする際のループ制御用
        self._initialize_game_state()

    def _create_stars(self, num_stars):
        """背景用の星を生成する"""
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            # 小さい星を多く、大きい星を少なく
            radius = random.choice([1, 1, 1, 2])
            # 明るさをランダムに設定
            brightness = random.randint(50, 150)
            color = (brightness, brightness, brightness)
            stars.append({'pos': (x, y), 'radius': radius, 'color': color})
        return stars

    def _initialize_game_state(self):
        """ゲームの状態を初期化する。__init__とresetから呼ばれる。"""
        self.start_time = pygame.time.get_ticks() # 経過時間の初期化
        # --- 背景の星を生成 ---
        self.background_stars = self._create_stars(NUM_BACKGROUND_STARS)

        # --- オブジェクトの生成 ---
        # ボタンのスペースを考慮し、公転の中心を少し上に設定
        center_point = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        # Planetオブジェクトを生成
        self.planet = Planet(center_point, Planet.SIZE)
        # Starオブジェクトを生成
        self.star = Star(center_point, Planet.SIZE * 3.0)
        # 新しいデザインの円形ボタンを画面左右中心に配置
        button_radius = 40
        self.left_button = Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 80, button_radius, 'left')
        self.right_button = Button(SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 80, button_radius, 'right')
        # HUDオブジェクトを生成
        self.hud = HUD()
        self.left_active = False
        self.right_active = False
        self.score = 0
        self.kill_count = 0
        self.corpses = []

    def run(self):
        """
        ゲームのメインループ
        """
        while self.is_running:
            # 1. イベント処理
            self._handle_events()
            # 2. ゲーム状態の更新
            self._update()
            # 3. 画面の描画
            self._draw()
            # フレームレートを維持
            self.clock.tick(FPS)
        
        # ゲーム終了処理
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """
        キーボードやマウスのイベントを処理する
        """
        for event in pygame.event.get():
            # ウィンドウの閉じるボタンが押されたらループを抜ける
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
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
        self._update_corpses()

        # 衝突の判定とビームの削除
        self._check_collisions()


    def _check_collisions(self):
        """惑星と光線の衝突を判定する"""
        planet_angle = self.planet.angle
        planet_orbit_radius = self.planet.radius
        planet_size = self.planet.size

        if planet_orbit_radius > planet_size:
            angle_margin = math.asin(planet_size / planet_orbit_radius)
        else:
            angle_margin = math.pi

        surviving_beams = []
        for beam in self.star.beams:
            beam_front_radius = beam.radius + beam.width + self.planet.size 
            beam_back_radius = max(0, beam.radius - beam.width - self.planet.size)

            collided = False
            if beam_back_radius < planet_orbit_radius < beam_front_radius:
                angle_diff = (planet_angle + beam.angle + math.pi) % (2 * math.pi) - math.pi

                if abs(angle_diff) < beam.arc_range / 2 + angle_margin:
                    self.kill_count += 1
                    self.score -= 200
                    self.corpses.append(BeamCorpse(beam.center_pos, beam.angle, beam.arc_range, beam.radius, beam.width))
                    collided = True
            elif beam.radius > planet_orbit_radius and not beam.dodged:
                self.score += 10
                beam.dodged = True
            
            if not collided:
                surviving_beams.append(beam)

        self.star.beams = surviving_beams

    def _update_corpses(self):
        """光線の死体を更新し、寿命が尽きたものを削除する"""
        for corpse in self.corpses:
            corpse.update()
        self.corpses = [c for c in self.corpses if c.is_alive()]

    # --- 強化学習用インターフェース ---

    def reset(self):
        """
        RL環境をリセットし、初期状態を返す
        """
        self._initialize_game_state()
        return self._get_state()

    def step(self, action):
        """
        RLエージェントのアクションを実行し、環境を1ステップ進める
        action: 0: 何もしない, 1: 左に加速, 2: 右に加速
        returns: (state, reward, done, info)
        """
        # 1. アクションに基づいて方向を決定し、ボタンの表示状態を更新
        direction = 0
        self.left_active = False
        self.right_active = False
        if action == 1:  # 左
            direction = 1
            self.left_active = True
        elif action == 2:  # 右
            direction = -1
            self.right_active = True

        # 2. ゲーム状態を更新
        self.planet.update(direction)
        self.star.update()
        self._update_corpses()

        # 3. 衝突判定と報酬計算
        score_before = self.score
        kills_before = self.kill_count
        self._check_collisions()

        done = self.kill_count > kills_before

        if done:
            reward = -100.0  # 衝突時の大きなペナルティ
        else:
            # 生存報酬 + ビーム回避によるスコア変動
            reward = 0.1 + (self.score - score_before)

        # 4. 新しい状態を取得
        state = self._get_state()

        # 5. Gym/Gymnasium互換の形式で返す
        info = {}
        return state, reward, done, info

    def _get_state(self):
        """現在のゲーム状態を固定長のNumpy配列として取得する"""
        # 惑星の状態 (3次元)。値は正規化する。
        planet_state = np.array([
            self.planet.angle / (2 * math.pi),
            self.planet.speed,
            self.planet.radius / (SCREEN_HEIGHT / 2)
        ])

        # 惑星に近い順にビームをソート
        beams = sorted(self.star.beams, key=lambda b: abs(b.radius - self.planet.radius))

        beam_features = []
        for i in range(self.NUM_OBSERVED_BEAMS):
            if i < len(beams):
                beam = beams[i]
                # [相対距離, 相対角度, 円弧の範囲, 幅] を正規化して追加
                features = [(beam.radius - self.planet.radius) / (SCREEN_HEIGHT / 2), (beam.angle - self.planet.angle + math.pi) % (2 * math.pi) - math.pi, beam.arc_range, beam.width / (SCREEN_HEIGHT / 2)]
                beam_features.extend(features)
            else: # ビームが足りない場合は-1で埋める
                beam_features.extend([-1] * 4)
        return np.concatenate([planet_state, np.array(beam_features)]).astype(np.float32)

    def _draw(self):
        """
        画面に各オブジェクトを描画する
        """
        self.screen.fill(BLACK)

        for star_data in self.background_stars:
            pygame.draw.circle(self.screen, star_data['color'], star_data['pos'], star_data['radius'])

        for corpse in self.corpses:
            corpse.draw(self.screen)
        
        self.star.draw(self.screen)
        self.planet.draw(self.screen)
        
        self.left_button.draw(self.screen, self.left_active)
        self.right_button.draw(self.screen, self.right_active)

        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.hud.draw(self.screen, self.planet.speed, self.planet.actual_acceleration, self.kill_count, self.score, elapsed_time)

        pygame.display.flip()