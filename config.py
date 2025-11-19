# config.py
import math

# --- 描画に関連するパラメータ ---

# 画面のサイズ
SCREEN_SIZE = 400
SCREEN_WIDTH = SCREEN_SIZE*3
SCREEN_HEIGHT = SCREEN_SIZE*2
# 色の定義 (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
EARTH_BLUE = (51, 153, 204)
SUN_ORANGE = (252, 130, 0)
# フレームレート
FPS = 120
NUM_BACKGROUND_STARS = 250
BUTTON_RADIUS = 30

# --- ゲームシステムに関連するパラメータ ---

CENTER_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)  # 天体の中心座標 ボタンのスペースを考慮し少し上に配置
CIRCLE_WIDTH = 2    # 天体の円の線の太さ

ACCELERATION = 0.0010 # 各加速度
FRICTION = 0.99 # 減速率

# Beamに関するパラメータ
BEAM_SPEED = 2           # 光線が広がる速度
BEAM_MAX_RADIUS = SCREEN_SIZE    # 光線の最大半径(生存判定用)

# Planetに関するパラメータ
PLANET_SIZE = 12 # 惑星の半径
PLANET_ORBIT_RADIUS = 225  # 惑星の公転半径
PLANET_INITIAL_ANGLE = math.pi / 2  # 惑星の初期角度（90度、下方向）

# Starに関するパラメータ
STAR_SIZE = PLANET_SIZE*3 # 恒星の半径

# --- 機械学習に関連するパラメータ ---
SUB_SCREEN_SIZE = 400

MAX_BEAMS = 5  # 状態に含めるビームの最大数