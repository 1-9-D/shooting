import pyxel as px   
import random as rd 
W, H = 256, 192
FPS = 60
SCENE = 0
class Plyaer:
    def __init__(self):
        self._x = W / 2 #X座標
        self._y = 180 #Y座標

    def _move(self, dir, speed):
        self._x += dir * speed
    
    def _shoot(self):
        bullets.append(Bullet(self._x + 5, self._y))

    def draw(self):
        #描画
        px.blt(self._x, self._y, 0, 16, 0, 11, 7, 0)

class Bullet:
    def __init__(self, x, y):
        self._x = x #X座標
        self._y = y #Y座標
        self._dir = 1
        self._move_count = 0
        self._anime = 1

    def update(self):
        self._y -= 8
        self._x += self._dir * 2
        self._move_count += 1
        if self._move_count % 5 == 0:
            self._dir *= -1
            self._anime *= -1
        #画面外で削除
        if self._y < 0:
            bullets.remove(self)

    def draw(self):
        #描画
        if self._anime == 1:
            px.blt(self._x, self._y, 0, 31, 0, 1, 2, 0)
        if self._anime == -1:
            px.blt(self._x, self._y, 0, 31, 3, 1, 2, 0)

class Enemy:
    def __init__(self, x, y):
        self._x = x #X座標
        self._y = y #Y座標
        self._dir = 1
        self._move_count = 0
        self._anime = 1
    
    def update(self):
        self._y += 2
        self._x += self._dir * 2
        self._move_count += 1
        if self._move_count % (FPS / 5) == 0:
            self._dir *= -1
            self._anime *= -1
        #画面外で削除
        if self._y > H:
            enemies.remove(self)
    
    def draw(self):
        if self._anime == 1:
            px.blt(self._x, self._y, 0, 32, 0, 11, 8, 0)
        if self._anime == -1:
            px.blt(self._x, self._y, 0, 32, 8, 11, 8, 0)

class App():
    def __init__(self):
        global bullets, enemies
        px.init(W, H, title="INVADER", fps=FPS)
        #画像読み込み
        px.load("img.pyxres")
        #プレイヤーを構築
        self.player = Plyaer() 
        #弾のリスト
        bullets = []
        #敵のリスト
        enemies = []
        #タイマー
        self.timer = 0
        self._time_limit = 10
        #スコア
        self.score = 0
        self.save_score = 0
        self.time_up_socre = 0
        self.time_up_need_socre = 1000
        
    def game_end(self):
        global SCENE, bullets, enemies
        self.save_score = self.score
        SCENE = 0
        #弾のリスト
        bullets = []
        #敵のリスト
        enemies = []
        #タイマー
        self.timer = 0
        self._time_limit = 10
        #スコア
        self.score = 0
        self.time_up_socre = 0
        self.time_up_need_socre = 1000
        
    def update(self):
        global SCENE, bullets, enemies
        #ESCで終了
        if px.btnp(px.KEY_ESCAPE):
            px.quit()
        if SCENE == 0:
            if px.btnp(px.KEY_S) or px.btn(px.MOUSE_BUTTON_LEFT):
                SCENE = 1
            pass
        elif SCENE == 1:
            if px.btn(px.KEY_D):
                self.player._move(1, 3)
            if px.btn(px.KEY_A):
                self.player._move(-1, 3)
            if px.btn(px.KEY_SPACE):
                self.player._shoot()
            if px.btn(px.MOUSE_BUTTON_LEFT):
                if px.mouse_y >= 50:
                    if px.mouse_x >= W - 50 and px.mouse_x <= W:
                        self.player._move(1, 3)
                    elif px.mouse_x >= 0 and px.mouse_x <= 50:
                        self.player._move(-1, 3)
                elif px.mouse_y <= 50:
                    self.player._shoot()
            if self.timer % (FPS / 5) == 0:
                enemies.append(Enemy(rd.randint(0, 256), 20))
            for bullet in bullets:
                bullet.update()
            for enemy in enemies:
                enemy.update()
            # 弾と敵の衝突判定 + プレイヤーと敵の衝突判定（統合）
            for enemy in enemies[:]:  
                for bullet in bullets[:]:  
                    if (enemy._x < bullet._x < enemy._x + 11) and (enemy._y < bullet._y < enemy._y + 8):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        self.score += 250
                        self.time_up_socre  += 250
                # プレイヤーとの衝突判定
                if (self.player._x < enemy._x + 11 and self.player._x + 11 > enemy._x) and \
                (self.player._y < enemy._y + 8 and self.player._y + 7 > enemy._y):
                    self.game_end()  
            #タイマー
            self.timer += 1
            if self.time_up_socre >= self.time_up_need_socre:
                self._time_limit += 1
                self.time_up_socre = 0
                self.time_up_need_socre *= 1.1
            if self.timer % FPS == 0:
                self._time_limit -= 1
            if self._time_limit <= 0:
                self.game_end()
        
    def draw(self):
        if SCENE == 0:
            #背景を黒に
            px.cls(0)
            px.text(W / 2 - 25, H / 2, "START:KEY_S", 4)
            px.text(W / 2 - 25, H / 2 - 10, f"SCORE:{self.save_score}", 12)

        elif SCENE == 1:
            #背景を黒に
            px.cls(0)
            #プレイヤー
            self.player.draw()
            #弾描画
            for bullet in bullets:
                bullet.draw()
            #敵描画
            for enemy in enemies:
                enemy.draw()
            px.text(5, 5, f"TIME:{self._time_limit}", 7)
            px.text(85, 5, f"SCORE:{self.score}", 7)

def main():
    app = App()
    px.run(app.update, app.draw)

if __name__ == "__main__":
    main()