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

    def player_udate(self, x, y):
        self.dot_x = x
        self.dot_y = y

class Shot:
    def __init__(self):
        self.shot_x = 0
        self.shot_y = 0
        #たまを撃つ向き 0上 1下 2左 3右
        self.vectol = 0

    def shot_update(self, x, y, vec):
        self.shot_x = x
        self.shot_y = y
        self.vectol = vec

class App:

    def __init__(self):
        
        self.player = Player()
        
        #タマ格納
        self.shots = []
        
        pyxel.init(128,128,caption="Battle Tower", fps=20)

        pyxel.load("tower.pyxres")

        pyxel.run(self.update, self.draw)

        

    def update(self):

        self.player_move()
        self.player_shot()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        self.tilemap_draw()
        self.player_draw()
        self.draw_shot()
        
        #デバッグ
        print(len(self.shots))
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
                    self.player.player_udate(self.player.dot_x, 120)
        
        #下に移動
        if pyxel.tilemap(0).get(map_x, map_y+1) == 36:
            if pyxel.btn(pyxel.KEY_DOWN):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_y = self.player.dot_y + 8
                    self.player.vectol = 1
                if  (self.player.dot_y + 8) > 128:
                    self.player.minimap_y += 16
                    self.player.map_count_y += 1
                    self.player.player_udate(self.player.dot_x, 8)
            
        #左に移動
        if pyxel.tilemap(0).get(map_x-1, map_y) == 36:
            if pyxel.btn(pyxel.KEY_LEFT):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_x = self.player.dot_x - 8
                    self.player.vectol = 2

                if (self.player.dot_x - 8) < -8:
                    self.player.minimap_x -= 16
                    self.player.map_count_x -= 1
                    self.player.player_udate(120, self.player.dot_y)

        #右に移動
        if pyxel.tilemap(0).get(map_x+1, map_y) == 36:
            if pyxel.btn(pyxel.KEY_RIGHT):
                if pyxel.frame_count % 3 == 0:
                    self.player.dot_x = self.player.dot_x + 8
                    self.player.vectol = 3

                if (self.player.dot_x + 8) > 128:
                    self.player.minimap_x += 16
                    self.player.map_count_x += 1
                    self.player.player_udate(8, self.player.dot_y)
        
    #たま発射
    def player_shot(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            #if len(self.shots) < 3:
            new_shot = Shot()
            new_shot.vectol = self.player.vectol
            new_shot.shot_update(self.player.dot_x, self.player.dot_y, new_shot.vectol)
            self.shots.append(new_shot)    
    
    #たま描画
    def draw_shot(self):
        for i in self.shots:
            x = 16*(self.player.map_count_x -1)
            y = 16*(self.player.map_count_y -1)
            shot_map_x = i.shot_x / 8 + x
            shot_map_y = i.shot_y / 8 + y
            if 0 < i.shot_x and i.shot_x < 128 and pyxel.tilemap(0).get(shot_map_x, shot_map_y) == 36:
                #左ショット
                if i.vectol == 2:
                    pyxel.rect(i.shot_x, i.shot_y+1, 2, 2, 10)
                    i.shot_update(i.shot_x - 8, i.shot_y, 2)
                #右ショット
                if i.vectol == 3:
                    pyxel.rect(i.shot_x+8, i.shot_y+1, 2, 2, 10)
                    i.shot_update(i.shot_x + 8, i.shot_y, 3)
            else:
                self.shots = [item for item in self.shots if item != i]

            if 0 < i.shot_y and i.shot_y < 128 and pyxel.tilemap(0).get(shot_map_x, shot_map_y) == 36: 
                #上ショット
                if i.vectol == 0:
                    pyxel.rect(i.shot_x+1, i.shot_y, 2, 2, 10)
                    i.shot_update(i.shot_x, i.shot_y - 8, 0)
                #下ショット
                if i.vectol == 1:
                    pyxel.rect(i.shot_x+3, i.shot_y+3, 2, 2, 10)
                    i.shot_update(i.shot_x, i.shot_y + 8, 1)
            else:
                self.shots = [item for item in self.shots if item != i]
                

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