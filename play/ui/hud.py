# play/ui/hud.py

import pygame
from config import WHITE, SCREEN_WIDTH

class HUD:
    """
    Heads-Up Display: ゲームの情報を画面に表示するクラス
    """
    def __init__(self, font_size=30):
        """
        HUDオブジェクトの初期化
        :param font_size: 表示するテキストのフォントサイズ
        """
        # システムに存在する等幅フォントを自動的に選択する
        # これにより、数字の幅が常に一定になり、表示のガタつきがなくなる
        font_names = ['consolas', 'dejavusansmono', 'couriernew', 'monospace']
        self.font = pygame.font.SysFont(font_names, font_size)  
        self.color = WHITE

    def draw(self, screen, planet_speed, actual_planet_acceleration, kill_count, score, elapsed_time):        
       """
       各種情報を画面に描画する
       :param screen: 描画対象のPygameスクリーンオブジェクト
       :param ...: 表示する各種ゲームデータ
       """

       # --- 速度の表示 ---
       display_speed = planet_speed * 1000
       speed_text = self.font.render(f"SPEED:{display_speed:+08.4f}", True, (0, 255, 0))
       speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))  
       screen.blit(speed_text, speed_rect)  

       # --- 経過時間の表示 ---
       time_text = self.font.render(f"TIME: {elapsed_time / 1000:6.2f}s", True, (0, 255, 0))
       time_rect = time_text.get_rect(topleft=(10, 10))
       screen.blit(time_text, time_rect)

       # --- 加速度の表示 ---
       display_accel = actual_planet_acceleration * 1000
       accel_text = self.font.render(f"ACCEL:{display_accel:+08.4f}", True, (0, 255, 0))
       accel_rect = accel_text.get_rect(topright=(SCREEN_WIDTH - 10, speed_rect.bottom + 5))
       screen.blit(accel_text, accel_rect)
       
       # --- スコアと衝突回数の表示 ---
       score_text = self.font.render(f"SCORE: {score}", True, (0, 255, 0))
       score_rect = score_text.get_rect(topleft=(10, time_rect.bottom + 5))
       screen.blit(score_text, score_rect)

       kill_text = self.font.render(f"KILLED: {kill_count}", True, (0, 255, 0))
       kill_rect = kill_text.get_rect(topleft=(10, score_rect.bottom + 5))
       screen.blit(kill_text, kill_rect)