# entities/beam.py

from .base import BaseArc
from config import *

class Beam(BaseArc):
    """
    恒星から発射される光線を表すクラス
    """

    #-- クラス定数 ---
    SPEED = BEAM_SPEED
    MAX_RADIUS = BEAM_MAX_RADIUS

    def __init__(self, center_pos, angle, arc_range, radius, width):
        '''
        param center_pos: 光線の中心座標 (x, y)
        param angle: 光線の中心角度
        param arc_range: 光線の角度範囲
        param radius: 光線の初期半径（恒星の表面から）
        param width: 光線の線の幅  
        '''

        super().__init__(
            center_pos=center_pos,
            angle=angle,
            arc_range=arc_range,
            radius=radius, # 発射時の初期半径（恒星の表面から）
            width=width,
            color=WHITE
        )
        self.dodged = False # 回避されたかどうかを記録するフラグ

    def update(self):
        """
        光線の状態を更新する
        """
        self.radius += self.SPEED # 光線が広がる速度で半径を増加

    def is_alive(self):
        """
        光線がまだ有効かどうかを判定する
        """
        return self.radius < self.MAX_RADIUS # 最大半径に達していないか判定

    def draw(self, screen):
        """
        光線を画面に描画する
        param screen: 描画対象のPygameスクリーンオブジェクト
        """

        # 半径(radius)が惑星の公転半径(225)を超えたらフェードアウト
        fade_distance = self.MAX_RADIUS - PLANET_ORBIT_RADIUS
        
        # フェードアウトの進行度合いを計算 (0.0: フェード開始, 1.0: フェード完了)
        fade_progress = max(0, (self.radius - PLANET_ORBIT_RADIUS)) / fade_distance if fade_distance > 0 else 1.0
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
        '''
        param center_pos: 光線の中心座標 (x, y)
        param angle: 光線の中心角度
        param arc_range: 光線の角度範囲
        param radius: 光線の初期半径（恒星が衝突した時の半径）
        param width: 光線の線の幅  
        '''
        super().__init__(
            center_pos=center_pos,
            angle=angle,
            arc_range=arc_range,
            radius=radius,
            width=width,
            color=RED
        )
        self.life = self.DURATION # 残りの表示時間

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
        :param screen: 描画対象のPygameスクリーンオブジェクト
        """
        if self.is_alive():
            life_ratio = self.life / self.DURATION
            current_color = tuple(int(c * life_ratio) for c in self.color)
            self.draw_arc(screen, current_color, self.width)