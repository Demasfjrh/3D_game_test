class Hero:
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.mode = True
        self.cameraBind()
        self.acceptEvents()
    
    def just_move(self, angle): #Pergerakan mode spectator
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)

        return from_x + dx, from_y + dy, from_z
    
    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        self.hero.setZ(self.hero.getZ() + 1)
    
    def down(self):
        self.hero.setZ(self.hero.getZ() - 1)

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, 1)
        elif angle <= 65:
            return (-1, 1)
        elif angle <= 110:
            return (-1, 0)
        elif angle <= 155:
            return (-1, -1)
        elif angle <= 200:
            return (0, -1)
        elif angle <= 245:
            return (1, -1)
        elif angle <= 290:
            return (1, 0)
        elif angle <= 335:
            return (1, 1)
        else:
            return (0, 1)


    def try_move(self, angle): #Pergerakan pemain
        
        
    def move_to(self, angle):
        if self.mode == True: #Mode spectator
            self.just_move(angle)
        else: #Mode pemain
            self.try_move(angle)

    def acceptEvents(self):
        base.accept('c', self.changeView)
        base.accept('m', self.turn_right)
        base.accept('m' + '-repeat', self.turn_right)
        base.accept('n', self.turn_left)
        base.accept('n' + '-repeat', self.turn_left)
        base.accept('w', self.forward)
        base.accept('w-repeat', self.forward)
        base.accept('a', self.left)
        base.accept('a-repeat', self.left)
        base.accept('s', self.back)
        base.accept('s-repeat', self.back)
        base.accept('d', self.right)
        base.accept('d-repeat', self.right)
        base.accept('j', self.up)
        base.accept('n', self.down)
        base.accept('z', self.changemode)

    def changemode(self):
        if self.mode == True:
            self.mode = False
        else:
            self.mode = True


    def turn_right(self):
        angle = self.hero.getH()
        angle -= 5
        self.hero.setH(angle % 360)
    
    def turn_left(self):
        angle = self.hero.getH()
        angle += 5
        self.hero.setH(angle % 360)
        

    def changeView(self):
        if self.cameraOn == True:
            self.cameraUp()
        else:
            self.cameraBind()
    
    def cameraBind(self): #POV Pemain
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True
    
    def cameraUp(self): #POV Editor
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False