# mode/play/play.py

import pygame

from config import *
from mode.system import System
from mode.play.ui.play_button import Play_Button
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
        # systemオブジェクトを生成
        self.system = System()
        
        # 円形ボタンを画面左右中心に配置
        self.left_button = Play_Button(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT - 80, BUTTON_RADIUS, 'left')
        self.right_button = Play_Button(SCREEN_WIDTH / 2 + 100, SCREEN_HEIGHT - 80, BUTTON_RADIUS, 'right')
        # HUDオブジェクトを生成
        self.hud = HUD()

    def update(self):
        """
        ゲーム内の各オブジェクトの状態を更新する
        """
        # --- 惑星の操作（キーボードとマウスの両方に対応） ---
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # 左方向への加速判定 (左キー or 左ボタンクリック)
        self.system.left_active = keys[pygame.K_LEFT] or \
                                (mouse_buttons[0] and self.left_button.is_clicked(mouse_pos))
        # 右方向への加速判定 (右キー or 右ボタンクリック)
        self.system.right_active = keys[pygame.K_RIGHT] or \
                                (mouse_buttons[0] and self.right_button.is_clicked(mouse_pos))

        # systemオブジェクトの状態を更新
        self.system.update()

    def draw(self):
        """
        画面に各オブジェクトを描画する
        """

        for corpse in self.system.corpses:
            corpse.draw(self.screen)
        
        self.system.star.draw(self.screen)
        self.system.planet.draw(self.screen)
        
        self.left_button.draw(self.screen, self.system.left_active)
        self.right_button.draw(self.screen, self.system.right_active)
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.hud.draw(self.screen, self.system.planet.speed, self.system.planet.actual_acceleration, self.system.kill_count, self.system.score, elapsed_time)
