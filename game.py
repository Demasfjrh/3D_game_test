from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, WindowProperties, CollisionTraverser, CollisionNode, CollisionHandlerPusher, CollisionSphere
from mapmanager import MapManager

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.land = MapManager()
        self.land.loadLand("asset/land.txt")

        self.disableMouse()
        self.camera.setPos(5, -5, 10)
        self.camera.lookAt(5, 5, 0)

        # Mouse settings
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(props)

        self.centerX = int(self.win.getProperties().getXSize() / 2)
        self.centerY = int(self.win.getProperties().getYSize() / 2)
        self.win.movePointer(0, self.centerX, self.centerY)

        self.camLens.setFov(100)

        # Input Key Setup
        self.keys = {"w": False, "a": False, "s": False, "d": False, "space": False}
        for key in self.keys:
            self.accept(key, self.setKey, [key, True])
            self.accept(f"{key}-up", self.setKey, [key, False])

        # Mouse Movement
        self.mouseSensitivity = 0.2
        self.pitch = 0
        self.yaw = 0

        # Gerakan
        self.velocity = Vec3(0, 0, 0)
        self.speed = 8
        self.gravity = -25
        self.jumpSpeed = 10
        self.isJumping = False
        self.onGround = False

        # Collision sphere
        self.initCollision()

        self.taskMgr.add(self.update, "update")

    def setKey(self, key, value):
        self.keys[key] = value

    def initCollision(self):
        base.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        self.colliderNode = CollisionNode("player")
        self.colliderNode.addSolid(CollisionSphere(0, 0, 1, 1))
        self.collider = self.camera.attachNewNode(self.colliderNode)

        self.pusher.addCollider(self.collider, self.camera)
        base.cTrav.addCollider(self.collider, self.pusher)

    def update(self, task):
        dt = globalClock.getDt()

        # Mouse Look
        if self.mouseWatcherNode.hasMouse():
            pointer = self.win.getPointer(0)
            x = pointer.getX()
            y = pointer.getY()

            dx = (x - self.centerX) * self.mouseSensitivity
            dy = (y - self.centerY) * self.mouseSensitivity

            self.yaw -= dx
            self.pitch -= dy  # NEGATIF agar tidak terbalik ke atas-bawah
            self.pitch = clamp(self.pitch, -89, 89)

            self.camera.setH(self.yaw)
            self.camera.setP(self.pitch)

            self.win.movePointer(0, self.centerX, self.centerY)  # Reset ke tengah

        # Gerakan
        moveVec = Vec3(0, 0, 0)
        quat = self.camera.getQuat(render)

        if self.keys["w"]:
            moveVec += quat.getForward()
        if self.keys["s"]:
            moveVec -= quat.getForward()
        if self.keys["a"]:
            moveVec -= quat.getRight()
        if self.keys["d"]:
            moveVec += quat.getRight()

        moveVec.setZ(0)
        moveVec.normalize()
        moveVec *= self.speed

        self.velocity.setX(moveVec.getX())
        self.velocity.setY(moveVec.getY())

        # Gravity
        self.velocity.setZ(self.velocity.getZ() + self.gravity * dt)

        # Jump
        if self.keys["space"] and self.onGround:
            self.velocity.setZ(self.jumpSpeed)
            self.onGround = False

        # Posisi baru
        newPos = self.camera.getPos() + self.velocity * dt
        if newPos.getZ() <= 2:
            newPos.setZ(2)
            self.velocity.setZ(0)
            self.onGround = True
        else:
            self.onGround = False

        self.camera.setPos(newPos)
        return task.cont

# Clamp helper
def clamp(value, minVal, maxVal):
    return max(min(value, maxVal), minVal)

game = Game()
game.run()
