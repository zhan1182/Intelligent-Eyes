

class ChessboardNotFound(Exception):

    def __init__(self, imagePath):
        self.imagePath = imagePath

    def __str__(self):
        print(self.imagePath + "cannot detect chessboard corners.")

