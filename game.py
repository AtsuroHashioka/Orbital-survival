# game.py 

import pygame
import sys       
import random  

from config import *
from mode.play.play import Play
from mode.start.start import Start

class Game:
    """
    ゲーム全体を管理するメインクラス
    """

    def __init__(self):
        """
        Gameオブジェクトの初期化
        """
        # Pygameの初期化
        pygame.init()
        # 画面の設定
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ORBITAL SURVIVAL")
        
        self.is_running = True # 人間がプレイする際のループ制御用
        self.game_mode = 'start'  # ゲームモードの初期設定

        # --- 背景の星を生成 ---
        self.background_stars = self._create_stars_(NUM_BACKGROUND_STARS)

        # ゲームモードオブジェクトの初期化
        self.play = Play(self.screen, self.clock)
        self.start = Start(self.screen)

    #--- 背景の星を生成 ---
    def _create_stars_(self, num_stars):
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

    #--- イベント処理 ---
    def _handle_events_(self):
        """
        キーボードやマウスのイベントを処理する
        """

        for event in pygame.event.get():
            # ウィンドウの閉じるボタンが押されたらループを抜ける
            if event.type == pygame.QUIT:
                self.is_running = False

            # ゲームモードごとのイベント処理
            if self.game_mode == 'start':
                if self.start.start_button.is_pressed(event):
                    self.game_mode = 'play'
                    self.play.initialize_play_state()  # プレイモードの初期化
            # 暫定対応
            elif self.game_mode == 'play':
                if self.start.start_button.is_pressed(event):
                    self.game_mode = 'start'

    #--- ゲーム状態の更新 ---
    def _update_(self):
        """
        ゲーム内の各オブジェクトの状態を更新する
        """
        if self.game_mode == 'start':
            self.start.update()
        elif self.game_mode == 'play':
            self.play.update()
        else:
            self.start.update()


    #--- 描画 ---
    def _draw_(self):
        """
        画面に各オブジェクトを描画する
        """
        self.screen.fill(BLACK)
        
        for star_data in self.background_stars:
            pygame.draw.circle(self.screen, star_data['color'], star_data['pos'], star_data['radius'])

        if self.game_mode == 'start':
            self.start.draw()
        elif self.game_mode == 'play':
            self.play.draw()
        else:
            self.start.draw()

        pygame.display.flip()

    def run(self):
        """
        ゲームのメインループ
        """

        # ゲームループ
        while self.is_running:
            # 1. イベント処理
            self._handle_events_()
            # 2. ゲームの状態更新
            self._update_()
            # 3. ゲームモードの実行
            self._draw_()
            # 4. フレームレートの制御
            self.clock.tick(FPS)

        # ゲーム終了処理
        pygame.quit()
        sys.exit()
