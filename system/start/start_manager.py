# system/start/start_manager.py

import pygame

from config import *
from system.base_manager import Base_Manager
from system.start.ui.start_button import Start_Button

class Start_Manager(Base_Manager):
    """
    スタート画面を管理するサブクラス
    """

    def __init__(self, screen, clock):
        """
        StartManagerオブジェクトの初期化
        """
       
        super().__init__(screen, clock)

        # スペースキーハンドラを生成
        self.start_button = Start_Button()
        
        # フォントの準備
        font_names = ['consolas', 'dejavusansmono', 'couriernew', 'monospace']
        self.title_font = pygame.font.SysFont(font_names, 74)
        self.prompt_font = pygame.font.SysFont(font_names, 36)
        
    def update(self):
        """
        ゲーム内の各オブジェクトの状態を更新する
        """
        pass

    def draw(self):
        """
        画面に各オブジェクトを描画する
        """

        # 画面中央にゲームタイトルを表示
        title_text = self.title_font.render("ORBITAL SURVIVAL", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        self.screen.blit(title_text, title_rect)

        # タイトルの下に "Press SPACE" を表示
        prompt_text = self.prompt_font.render("PRESS SPACE TO PLAY", True, GREEN)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 30))
        self.screen.blit(prompt_text, prompt_rect)