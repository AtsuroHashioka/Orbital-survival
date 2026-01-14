# system/base_manager.py

class Base_Manager:
    """
    ゲームモードの基底クラス
    """

    def __init__(self, screen, clock):
        """
        Base_Managerオブジェクトの初期化

        :param screen: 画面オブジェクト
        :param clock: クロックオブジェクト
        """
        self.screen = screen
        # 時間管理用のClockオブジェクト
        self.clock = clock

    def update(self):
        """
        ゲーム内の各オブジェクトの状態を更新する
        """
        pass

    def draw(self):
        """
        画面に各オブジェクトを描画する
        """
        pass