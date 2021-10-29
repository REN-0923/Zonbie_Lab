import pyxel

class Player:

    def __init__(self):
        
        #プレイヤーの実際の座標
        self.dot_x = 16
        self.dot_y = 24

        #プレイヤーのタイルマップ上の座標
        self.map_x = int(self.dot_x / 8)
        self.map_y = int(self.dot_y / 8)

        #プレイヤーの向き 0上 1下 2左 3右
        self.vectol = 0

        #プレイヤーの描画タイル 上32,33 下0,1 左34,35 右2,3 
        self.image = 32

class App:

    def __init__(self):
        
        self.player = Player()
        
        pyxel.init(128,128,caption="Battle Tower", fps=25)

        pyxel.load("tower.pyxres")

        pyxel.run(self.update, self.draw)

        

    def update(self):

        self.player_move()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        self.tilemap_draw()
        self.player_draw()
    def tilemap_draw(self):
        base_x = 0
        base_y = 0
        tm = 0
        u = 0
        v = 0
        w = 16
        h = 16

        pyxel.bltm(base_x,base_y,tm,u,v,w,h)

    def player_move(self):
        #上に移動
        if pyxel.tilemap(0).get(self.player.map_x, self.player.map_y-1) == 36:
            if pyxel.btnp(pyxel.KEY_UP):
                self.player.dot_y = self.player.dot_y - 8
                self.player.vectol = 0
        
        #下に移動
        if pyxel.tilemap(0).get(self.player.map_x, self.player.map_y+1) == 36:
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.player.dot_y = self.player.dot_y + 8
                self.player.vectol = 1
            
        #左に移動
        if pyxel.tilemap(0).get(self.player.map_x-1, self.player.map_y) == 36:
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.player.dot_x = self.player.dot_x - 8
                self.player.vectol = 2
        #右に移動
        if pyxel.tilemap(0).get(self.player.map_x+1, self.player.map_y) == 36:
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.player.dot_x = self.player.dot_x + 8
                self.player.vectol = 3

    def player_draw(self):
        
        #もし上キー押された後やったら
        if self.player.vectol == 0:
            if pyxel.frame_count % 2 == 0:
                self.player.image = 32
            else:
                self.player.image = 33

        #もし下キー押された後やったら
        elif self.player.vectol == 1:
            if pyxel.frame_count % 2 == 0:
                self.player.image = 0
            else:
                self.player.image = 1
        
        #もし左キー押された後やったら
        elif self.player.vectol == 2:
            if pyxel.frame_count % 2 == 0:
                self.player.image = 34
            else:
                self.player.image = 35

        #もし右キー押された後やったら
        elif self.player.vectol == 3:
            if pyxel.frame_count % 2 == 0:
                self.player.image = 2
            else:
                self.player.image = 3

        #描画範囲をimageから計算
        if self.player.image < 32:
            u = self.player.image * 8
            v = 0
        elif self.player.image >= 32:
            u = self.player.image - 32
            u = u * 8
            v = 8
        
        pyxel.blt(self.player.dot_x, self.player.dot_y, 0, u, v, 8, 8, 0)

App()