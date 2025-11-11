# play/ui/button.py

import pygame
import math
from config import WHITE, BLACK

class Button:
    """
    スタイリッシュな円形の矢印ボタンを表すクラス
    """
    def __init__(self, center_x, center_y, radius, direction):
        """
        Buttonオブジェクトの初期化
        :param center_x: ボタンの中心x座標
        :param center_y: ボタンの中心y座標
        :param radius: ボタンの半径
        :param direction: 矢印の向き ('left' or 'right')
        """
        self.center = (center_x, center_y)
        self.radius = radius
        self.direction = direction

        # パフォーマンス向上のため、ボタンの画像を事前に生成
        # 通常状態（黒地に白マーク）とアクティブ状態（白地に黒マーク）の2種類
        self.image_normal = self._create_surface(icon_color=WHITE, bg_color=BLACK)
        self.image_active = self._create_surface(icon_color=BLACK, bg_color=WHITE)
        self.rect = self.image_normal.get_rect(center=self.center)

    def _create_surface(self, icon_color, bg_color):
        """
        指定された色のアイコンを持つボタンのSurfaceを生成する内部メソッド
        :param icon_color: 矢印アイコンの色
        :return: 描画済みのPygame Surfaceオブジェクト
        """
        # ボタンの直径サイズの透明なSurfaceを作成
        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        # 背景の円を描画
        pygame.draw.circle(surface, bg_color, (self.radius, self.radius), self.radius)
        # ボタンの縁に白い円の枠を追加
        pygame.draw.circle(surface, WHITE, (self.radius, self.radius), self.radius, 2)
        
        # 矢印のポリゴン（三角形）の頂点を計算
        # ボタンの半径を基準に、相対的な座標を計算する
        arrow_size = self.radius * 0.4
        if self.direction == 'left':
            p1 = (self.radius - arrow_size, self.radius)
            p2 = (self.radius + arrow_size, self.radius - arrow_size)
            p3 = (self.radius + arrow_size, self.radius + arrow_size)
        else: # 'right'
            p1 = (self.radius + arrow_size, self.radius)
            p2 = (self.radius - arrow_size, self.radius - arrow_size)
            p3 = (self.radius - arrow_size, self.radius + arrow_size)

        # アンチエイリアスを有効にして、滑らかな矢印を描画
        pygame.draw.polygon(surface, icon_color, [p1, p2, p3])
        
        return surface

    def draw(self, screen, is_active=False):
        """
        ボタンを画面に描画する。アクティブ状態に応じて表示を切り替える。
        :param screen: 描画対象のPygameスクリーンオブジェクト
        :param is_active: ボタンが押されている状態かどうか
        """
        if is_active:
            screen.blit(self.image_active, self.rect)
        else:
            screen.blit(self.image_normal, self.rect)

    def is_clicked(self, pos):
        """
        指定された座標がボタンの円形領域内にあるか判定する
        :param pos: マウスのクリック座標 (x, y)
        :return: クリックされていればTrue, そうでなければFalse
        """
        # 中心点とマウス位置の距離を計算し、半径と比較
        return math.hypot(pos[0] - self.center[0], pos[1] - self.center[1]) <= self.radius