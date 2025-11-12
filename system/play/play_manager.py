# system/play/play_manager.py

import pygame

from config import *
from system.logic import Logic
from system.base_manager import Base_Manager
from system.play.ui.play_button import Play_Button
from system.play.ui.hud import HUD

class Play_Manager(Base_Manager):
    """
    PLAYモードを管理するサブクラス
    """

    def __init__(self, screen, clock):
        """
        PlayManagerオブジェクトの初期化
        """
       
        super().__init__(screen, clock)
        
        # ゲームの状態を初期化
        self.initialize_state()

    def initialize_state(self):
        """ゲームの状態を初期化する。"""
        self.start_time = pygame.time.get_ticks() # 経過時間の初期化

        # --- オブジェクトの生成 ---
        # logicオブジェクトを生成
        self.logic = Logic()
        
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
        self.logic.left_active = keys[pygame.K_LEFT] or \
                                (mouse_buttons[0] and self.left_button.is_clicked(mouse_pos))
        # 右方向への加速判定 (右キー or 右ボタンクリック)
        self.logic.right_active = keys[pygame.K_RIGHT] or \
                                (mouse_buttons[0] and self.right_button.is_clicked(mouse_pos))

        # logicオブジェクトの状態を更新
        self.logic.update()

    def draw(self):
        """
        画面に各オブジェクトを描画する
        """

        for corpse in self.logic.corpses:
            corpse.draw(self.screen)
        
        self.logic.star.draw(self.screen)
        self.logic.planet.draw(self.screen)
        
        self.left_button.draw(self.screen, self.logic.left_active)
        self.right_button.draw(self.screen, self.logic.right_active)
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.hud.draw(self.screen, self.logic.planet.speed, self.logic.planet.actual_acceleration, self.logic.kill_count, self.logic.score, elapsed_time)
