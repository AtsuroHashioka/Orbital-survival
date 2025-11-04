# entities/beam.py

from .base import BaseArc
from config import WHITE, FPS

class Beam(BaseArc):
    """
    恒星から発射される光線を表すクラス
    """
    # --- クラス定数 ---
    SPEED = 2           # 光線が広がる速度
    MAX_RADIUS = 400    # 光線の最大半径

    def __init__(self, center_pos, angle, arc_range, initial_radius, width):
        super().__init__(
            center_pos=center_pos,
            angle=angle,
            arc_range=arc_range,
            radius=initial_radius, # 発射時の初期半径（恒星の表面から）
            width=width,
            color=WHITE
        )
        self.dodged = False # 回避されたかどうかを記録するフラグ

    def update(self):
        self.radius += self.SPEED

    def is_alive(self):
        return self.radius < self.MAX_RADIUS

    def draw(self, screen):
        # 半径(radius)が惑星の公転半径(225)を超えたらフェードアウト
        fade_start_radius = 225
        fade_distance = self.MAX_RADIUS - fade_start_radius
        
        # フェードアウトの進行度合いを計算 (0.0: フェード開始, 1.0: フェード完了)
        fade_progress = max(0, (self.radius - fade_start_radius)) / fade_distance if fade_distance > 0 else 1.0
        life_ratio = 1.0 - min(fade_progress, 1.0)

        current_color = tuple(int(c * life_ratio) for c in self.color)
        draw_width = min(self.width, int(self.radius))
        
        self.draw_arc(screen, current_color, draw_width)

class BeamCorpse(BaseArc):
    """
    衝突時に表示される光線の「死体」を表すクラス
    """
    DURATION = FPS // 4 # 表示時間 (0.25秒)

    def __init__(self, center_pos, angle, arc_range, radius, width):
        super().__init__(
            center_pos=center_pos,
            angle=angle,
            arc_range=arc_range,
            radius=radius,
            width=width,
            color=(255, 0, 0) # 赤色
        )
        self.life = self.DURATION

    def update(self):
        """
        死体の状態を更新する（フェードアウト）
        """
        self.life -= 1

    def is_alive(self):
        """
        死体がまだ表示されるべきか判定
        """
        return self.life > 0

    def draw(self, screen):
        """
        死体を描画する（フェードアウト）
        """
        if self.life > 0:
            life_ratio = self.life / self.DURATION
            current_color = tuple(int(c * life_ratio) for c in self.color)
            self.draw_arc(screen, current_color, self.width)