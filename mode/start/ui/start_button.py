# mode/start/ui/start_button.py

import pygame

from config import *

class Start_Button:
    """
    スペースキーの入力を感知するクラス
    """

    def __init__(self):
        pass # 初期化は特に必要なし

    def is_pressed(self, event):
        """
        キーボードイベントを処理し、スペースキーが押されたら True を返す
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False
