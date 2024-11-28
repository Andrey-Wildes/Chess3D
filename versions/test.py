from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight, DirectionalLight, Vec4, VBase3

class ChessGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Carregar o tabuleiro
        self.board = self.loader.loadModel("models/chessboard.obj")
        self.board.reparentTo(self.render)
        self.board.setScale(2)  # Ajustar a escala do tabuleiro

        # Adicionar luz ambiente
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        ambientLightNode = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNode)

        # Adicionar luz direcional
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
        directionalLightNode = self.render.attachNewNode(directionalLight)
        directionalLightNode.setHpr(45, -45, 0)
        self.render.setLight(directionalLightNode)

        # Carregar e posicionar as peças
        self.loadPieces()

    def loadPieces(self):
        # Carregar modelo da peça
        pieceModel = self.loader.loadModel("models/Pawn.obj")

        # Criar uma instância de peça para cada peça
        for i in range(8):
            for j in range(8):
                piece = pieceModel.copyTo(self.render)  # Carregar o modelo sem uma animação
                piece.setPos(i - 3.5, j - 3.5, 0.5)  # Ajustar posição das peças
                piece.setScale(0.1)  # Ajustar escala das peças

if __name__ == "__main__":
    game = ChessGame()
    game.run()
