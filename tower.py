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

        #プレイヤーが現在いるミニマップの座標(16の倍数のやつ)
        self.minimap_x = 0
        self.minimap_y = 0

        #プレイヤーが何枚目のマップにいるか
        self.map_count_x = 1
        self.map_count_y = 1

class App:

    def __init__(self):
        
        self.player = Player()
        
        pyxel.init(128,128,caption="Battle Tower", fps=20)

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
        
        #デバッグ
        map_x = self.player.dot_x/8
        map_y = self.player.dot_y/8
    def tilemap_draw(self):
        base_x = 0
        base_y = 0
        tm = 0
        u = self.player.minimap_x
        v = self.player.minimap_y
        w = 16
        h = 16

        pyxel.bltm(base_x,base_y,tm,u,v,w,h)
      

    def player_move(self):
        x = 16*(self.player.map_count_x -1)
        y = 16*(self.player.map_count_y -1)
        map_x = self.player.dot_x/8 + x
        map_y = self.player.dot_y/8 + y
        #上に移動
        if pyxel.tilemap(0).get(map_x, map_y-1) == 36:
            if pyxel.btn(pyxel.KEY_UP):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_y = self.player.dot_y - 8
                    self.player.vectol = 0
                if  (self.player.dot_y - 8) < -8:
                    self.player.minimap_y -= 16
                    self.player.map_count_y -= 1
                    self.player_udate(self.player.dot_x, 120)
        
        #下に移動
        if pyxel.tilemap(0).get(map_x, map_y+1) == 36:
            if pyxel.btn(pyxel.KEY_DOWN):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_y = self.player.dot_y + 8
                    self.player.vectol = 1
                if  (self.player.dot_y + 8) > 128:
                    self.player.minimap_y += 16
                    self.player.map_count_y += 1
                    self.player_udate(self.player.dot_x, 8)
            
        #左に移動
        if pyxel.tilemap(0).get(map_x-1, map_y) == 36:
            if pyxel.btn(pyxel.KEY_LEFT):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_x = self.player.dot_x - 8
                    self.player.vectol = 2

                if (self.player.dot_x - 8) < -8:
                    self.player.minimap_x -= 16
                    self.player.map_count_x -= 1
                    self.player_udate(120, self.player.dot_y)

        #右に移動
        if pyxel.tilemap(0).get(map_x+1, map_y) == 36:
            if pyxel.btn(pyxel.KEY_RIGHT):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_x = self.player.dot_x + 8
                    self.player.vectol = 3

                if (self.player.dot_x + 8) > 128:
                    self.player.minimap_x += 16
                    self.player.map_count_x += 1
                    self.player_udate(8, self.player.dot_y)
        

    def player_udate(self, x, y):
        self.player.dot_x = x
        self.player.dot_y = y

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