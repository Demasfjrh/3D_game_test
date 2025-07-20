class MapManager():
    def __init__(self):
        self.model = 'asset/block.egg'
        self.texture = 'asset/block.png'
        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode('land')

    def getColorByHeight(self, z):
        """Beri warna berbeda untuk tiap ketinggian"""
        r = (z * 50) % 256 / 255
        g = (z * 85) % 256 / 255
        b = (z * 120) % 256 / 255
        return (r, g, b, 1)

    def addBlck(self, position):
        x, y, z = position
        block = loader.loadModel(self.model)
        block.setTexture(loader.loadTexture(self.texture))
        block.setPos(position)
        block.setColor(self.getColorByHeight(z))
        block.reparentTo(self.land)
        return block

    def loadLand(self, filename):
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.strip().split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        self.addBlck((x, y, z0))
                    x += 1
                y += 1