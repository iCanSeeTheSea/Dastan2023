# Skeleton Program code for the AQA A Level Paper 1 Summer 2023 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9 programming environment

import random


# It's a class that represents a game of Dastan
class Dastan:
    def __init__(self, R, C, NoOfPieces):
        """
        It creates a board, creates two players, creates a list of move options, creates a list of move options offered,
        creates pieces, and sets the current player to the first player

        :param R: Number of rows
        :param C: The number of columns in the board
        :param NoOfPieces: The number of pieces each player has
        """
        self._Board = []
        self._Players = []
        self._MoveOptionOffer = []
        self._Players.append(Player("Player One", 1))
        self._Players.append(Player("Player Two", -1))
        self.__CreateMoveOptions()
        self._NoOfRows = R
        self._NoOfColumns = C
        self._MoveOptionOfferPosition = 0
        self.__CreateMoveOptionOffer()
        self.__CreateBoard()
        self.__CreatePieces(NoOfPieces)
        self._CurrentPlayer = self._Players[0]

    def __DisplayBoard(self):
        """
        The function prints the board, with the column numbers at the top, the row numbers on the left, and the pieces in
        the squares
        """
        print("\n" + "   ", end="")
        for Column in range(1, self._NoOfColumns + 1):
            print(str(Column) + "  ", end="")
        print("\n" + "  ", end="")
        for Count in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print("-")
        for Row in range(1, self._NoOfRows + 1):
            print(str(Row) + " ", end="")
            for Column in range(1, self._NoOfColumns + 1):
                Index = self.__GetIndexOfSquare(Row * 10 + Column)
                print("|" + self._Board[Index].GetSymbol(), end="")
                PieceInSquare = self._Board[Index].GetPieceInSquare()
                if PieceInSquare is None:
                    print(" ", end="")
                else:
                    print(PieceInSquare.GetSymbol(), end="")
            print("|")
        print("  -", end="")
        for Column in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print()
        print()

    def __DisplayState(self):
        """
        It displays the board, the move option offer, the current player's state, and the current player's name
        """
        self.__DisplayBoard()
        print("Move option offer: " + self._MoveOptionOffer[self._MoveOptionOfferPosition])
        print()
        print(self._CurrentPlayer.GetPlayerStateAsString())
        print("Turn: " + self._CurrentPlayer.GetName())
        print()

    def __GetIndexOfSquare(self, SquareReference):
        """
        It takes a square reference (e.g. A1, B2, C3, etc.) and returns the index of the square in the list of squares

        :param SquareReference: The reference of the square you want to get the index of
        :return: The index of the square in the list of squares.
        """
        Row = SquareReference // 10
        Col = SquareReference % 10
        return (Row - 1) * self._NoOfColumns + (Col - 1)

    def __CheckSquareInBounds(self, SquareReference):
        """
        It checks if a square reference is within the bounds of the board

        :param SquareReference: The square reference of the square you want to check
        :return: a boolean value.
        """
        Row = SquareReference // 10
        Col = SquareReference % 10
        if Row < 1 or Row > self._NoOfRows:
            return False
        elif Col < 1 or Col > self._NoOfColumns:
            return False
        else:
            return True

    def __CheckSquareIsValid(self, SquareReference, StartSquare):
        """
        If the square is in bounds, and the piece in the square is either empty or belongs to the other player, then the
        square is valid

        :param SquareReference: The square you want to check
        :param StartSquare: This is a boolean value that is true if the square is the starting square of the piece
        :return: A boolean value.
        """
        if not self.__CheckSquareInBounds(SquareReference):
            return False
        PieceInSquare = self._Board[self.__GetIndexOfSquare(SquareReference)].GetPieceInSquare()
        if PieceInSquare is None:
            if StartSquare:
                return False
            else:
                return True
        elif self._CurrentPlayer.SameAs(PieceInSquare.GetBelongsTo()):
            if StartSquare:
                return True
            else:
                return False
        else:
            if StartSquare:
                return False
            else:
                return True

    def __CheckIfGameOver(self):
        """
        If a mirza is in a kotla that does not belong to the player who owns the mirza, the game is over
        :return: a boolean value.
        """
        Player1HasMirza = False
        Player2HasMirza = False
        for S in self._Board:
            PieceInSquare = S.GetPieceInSquare()
            if PieceInSquare is not None:
                if S.ContainsKotla() and PieceInSquare.GetTypeOfPiece() == "mirza" and not PieceInSquare.GetBelongsTo().SameAs(
                        S.GetBelongsTo()):
                    return True
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(
                        self._Players[0]):
                    Player1HasMirza = True
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(
                        self._Players[1]):
                    Player2HasMirza = True
        return not (Player1HasMirza and Player2HasMirza)

    def __GetSquareReference(self, Description):
        """
        The function __GetSquareReference() takes two arguments, self and Description, and returns the value of the variable
        SelectedSquare.

        :param Description: The description of the square you want to get
        :return: The square reference is being returned.
        """
        SelectedSquare = int(input("Enter the square " + Description + " (row number followed by column number): "))
        return SelectedSquare

    def __UseMoveOptionOffer(self):
        """
        The player chooses a move option from their queue to replace with a new move option from the offer
        """
        ReplaceChoice = int(input("Choose the move option from your queue to replace (1 to 5): "))
        self._CurrentPlayer.UpdateMoveOptionQueueWithOffer(ReplaceChoice - 1, self.__CreateMoveOption(
            self._MoveOptionOffer[self._MoveOptionOfferPosition], self._CurrentPlayer.GetDirection()))
        self._CurrentPlayer.ChangeScore(-(10 - (ReplaceChoice * 2)))
        self._MoveOptionOfferPosition = random.randint(0, 4)

    def __GetPointsForOccupancyByPlayer(self, CurrentPlayer):
        """
        For each square on the board, add the points for occupancy for the current player

        :param CurrentPlayer: The player whose score is being adjusted
        :return: The score adjustment for the current player.
        """
        ScoreAdjustment = 0
        for S in self._Board:
            ScoreAdjustment += (S.GetPointsForOccupancy(CurrentPlayer))
        return ScoreAdjustment

    def __UpdatePlayerScore(self, PointsForPieceCapture):
        """
        The function updates the score of the current player by adding the points for the current player's occupancy and the
        points for the piece capture

        :param PointsForPieceCapture: The number of points that the current player gets for capturing a piece
        """
        self._CurrentPlayer.ChangeScore(
            self.__GetPointsForOccupancyByPlayer(self._CurrentPlayer) + PointsForPieceCapture)

    def __CalculatePieceCapturePoints(self, FinishSquareReference):
        """
        It returns the points of the piece that is captured if the piece is captured

        :param FinishSquareReference: The reference of the square that the piece is moving to
        :return: The points of the piece that is being captured.
        """
        if self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare() is not None:
            return self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare().GetPointsIfCaptured()
        return 0

    def PlayGame(self):
        """
        The function PlayGame() is a while loop that runs until the game is over.
        """
        GameOver = False
        while not GameOver:
            self.__DisplayState()
            SquareIsValid = False
            Choice = 0

            # allows player to choose either a valid move option or the move offer
            while Choice < 1 or Choice > 3:
                Choice = int(input("Choose move option to use from queue (1 to 3) or 9 to take the offer: "))
                if Choice == 9:
                    self.__UseMoveOptionOffer()
                    self.__DisplayState()

            # allows the player to select the piece they want to move
            while not SquareIsValid:
                StartSquareReference = self.__GetSquareReference("containing the piece to move")
                SquareIsValid = self.__CheckSquareIsValid(StartSquareReference, True)

            # allows the player to select the position to move the piece to
            SquareIsValid = False
            while not SquareIsValid:
                FinishSquareReference = self.__GetSquareReference("to move to")
                SquareIsValid = self.__CheckSquareIsValid(FinishSquareReference, False)

            # determines whether the specified move is legal or not
            MoveLegal = self._CurrentPlayer.CheckPlayerMove(Choice, StartSquareReference, FinishSquareReference)
            if MoveLegal:
                # updating game state based on move
                PointsForPieceCapture = self.__CalculatePieceCapturePoints(FinishSquareReference)
                self._CurrentPlayer.ChangeScore(-(Choice + (2 * (Choice - 1))))
                self._CurrentPlayer.UpdateQueueAfterMove(Choice)
                self.__UpdateBoard(StartSquareReference, FinishSquareReference)
                self.__UpdatePlayerScore(PointsForPieceCapture)
                print("New score: " + str(self._CurrentPlayer.GetScore()) + "\n")

            # swapping the currently active player
            if self._CurrentPlayer.SameAs(self._Players[0]):
                self._CurrentPlayer = self._Players[1]
            else:
                self._CurrentPlayer = self._Players[0]

            GameOver = self.__CheckIfGameOver()

        self.__DisplayState()
        self.__DisplayFinalResult()

    def __UpdateBoard(self, StartSquareReference, FinishSquareReference):
        """
        It takes a start square reference and a finish square reference, and it moves the piece from the start square to the
        finish square

        :param StartSquareReference: The reference of the square that the piece is moving from
        :param FinishSquareReference: The square that the piece is moving to
        """
        self._Board[self.__GetIndexOfSquare(FinishSquareReference)].SetPiece(
            self._Board[self.__GetIndexOfSquare(StartSquareReference)].RemovePiece())

    def __DisplayFinalResult(self):
        """
        If the scores are equal, print "Draw!", otherwise print the name of the player with the higher score, followed by "
        is the winner!"
        """
        if self._Players[0].GetScore() == self._Players[1].GetScore():
            print("Draw!")
        elif self._Players[0].GetScore() > self._Players[1].GetScore():
            print(self._Players[0].GetName() + " is the winner!")
        else:
            print(self._Players[1].GetName() + " is the winner!")

    def __CreateBoard(self):
        """
        It creates a board with the number of rows and columns specified by the user
        """
        for Row in range(1, self._NoOfRows + 1):
            for Column in range(1, self._NoOfColumns + 1):
                if Row == 1 and Column == self._NoOfColumns // 2:
                    S = Kotla(self._Players[0], "K")
                elif Row == self._NoOfRows and Column == self._NoOfColumns // 2 + 1:
                    S = Kotla(self._Players[1], "k")
                else:
                    S = Square()
                self._Board.append(S)

    def __CreatePieces(self, NoOfPieces):
        """
        It creates the pieces for the game

        :param NoOfPieces: The number of pieces each player has
        """
        for Count in range(1, NoOfPieces + 1):
            CurrentPiece = Piece("piece", self._Players[0], 1, "!")
            self._Board[self.__GetIndexOfSquare(2 * 10 + Count + 1)].SetPiece(CurrentPiece)
        CurrentPiece = Piece("mirza", self._Players[0], 5, "1")
        self._Board[self.__GetIndexOfSquare(10 + self._NoOfColumns // 2)].SetPiece(CurrentPiece)
        for Count in range(1, NoOfPieces + 1):
            CurrentPiece = Piece("piece", self._Players[1], 1, '"')
            self._Board[self.__GetIndexOfSquare((self._NoOfRows - 1) * 10 + Count + 1)].SetPiece(CurrentPiece)
        CurrentPiece = Piece("mirza", self._Players[1], 5, "2")
        self._Board[self.__GetIndexOfSquare(self._NoOfRows * 10 + (self._NoOfColumns // 2 + 1))].SetPiece(CurrentPiece)

    def __CreateMoveOptionOffer(self):
        """
        It appends the names of the units to the list of units that can be moved
        """
        self._MoveOptionOffer.append("jazair")
        self._MoveOptionOffer.append("chowkidar")
        self._MoveOptionOffer.append("cuirassier")
        self._MoveOptionOffer.append("ryott")
        self._MoveOptionOffer.append("faujdar")

    def __CreateRyottMoveOption(self, Direction):
        """
        It creates a MoveOption object, adds four Move objects to it, and returns the MoveOption object

        :param Direction: 1 for white, -1 for black
        :return: A MoveOption object.
        """
        NewMoveOption = MoveOption("ryott")
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateFaujdarMoveOption(self, Direction):
        """
        It creates a MoveOption object with the name "faujdar" and adds four moves to it

        :param Direction: The direction the piece is moving in
        :return: A MoveOption object.
        """
        NewMoveOption = MoveOption("faujdar")
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateJazairMoveOption(self, Direction):
        """
        It creates a MoveOption object that contains all the possible moves for a Jazair piece

        :param Direction: 1 for white, -1 for black
        :return: A MoveOption object.
        """
        NewMoveOption = MoveOption("jazair")
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateCuirassierMoveOption(self, Direction):
        """
        It creates a MoveOption object for a Cuirassier, which is a type of chess piece

        :param Direction: 1 for white, -1 for black
        :return: A MoveOption object.
        """
        NewMoveOption = MoveOption("cuirassier")
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateChowkidarMoveOption(self, Direction):
        """
        It creates a MoveOption object for the chowkidar piece, which is a piece that can move in any direction, but only
        one square at a time

        :param Direction: 1 for white, -1 for black
        :return: A MoveOption object.
        """
        NewMoveOption = MoveOption("chowkidar")
        NewMove = Move(1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateMoveOption(self, Name, Direction):
        """
        It returns a list of all the possible moves for a given piece in a given direction

        :param Name: The name of the piece
        :param Direction: The direction the piece is moving in
        :return: the move options for the piece.
        """
        if Name == "chowkidar":
            return self.__CreateChowkidarMoveOption(Direction)
        elif Name == "ryott":
            return self.__CreateRyottMoveOption(Direction)
        elif Name == "faujdar":
            return self.__CreateFaujdarMoveOption(Direction)
        elif Name == "jazair":
            return self.__CreateJazairMoveOption(Direction)
        else:
            return self.__CreateCuirassierMoveOption(Direction)

    def __CreateMoveOptions(self):
        """
        It creates a list of move options for each player, and adds them to the player's move option queue
        """
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", 1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", -1))


# The Piece class is a class that represents a piece on the board.
class Piece:
    def __init__(self, T, B, P, S):
        """
        The function __init__() is a constructor that initializes the data members of the class

        :param T: Type of piece
        :param B: The player that the piece belongs to
        :param P: Points if captured
        :param S: The symbol that will be used to represent the piece on the board
        """
        self._TypeOfPiece = T
        self._BelongsTo = B
        self._PointsIfCaptured = P
        self._Symbol = S

    def GetSymbol(self):
        """
        It returns the value of the variable _Symbol.
        :return: The symbol of the stock.
        """
        return self._Symbol

    def GetTypeOfPiece(self):
        """
        It returns the type of piece.
        :return: The type of piece.
        """
        return self._TypeOfPiece

    def GetBelongsTo(self):
        """
        It returns the value of the variable _BelongsTo.
        :return: The value of the _BelongsTo attribute.
        """
        return self._BelongsTo

    def GetPointsIfCaptured(self):
        """
        It returns the value of the variable _PointsIfCaptured.
        :return: The points that the player will get if they capture the piece.
        """
        return self._PointsIfCaptured


# A Square is a place on the board where a piece can be placed
class Square:
    def __init__(self):
        """
        The function __init__() is a constructor that initializes the instance variables of the class Square
        """
        self._PieceInSquare = None
        self._BelongsTo = None
        self._Symbol = " "

    def SetPiece(self, P):
        """
        The function SetPiece() takes a piece as an argument and sets the piece in the square

        :param P: The piece that is being set in the square
        """
        self._PieceInSquare = P

    def RemovePiece(self):
        """
        It removes the piece from the square and returns it
        :return: The piece that was in the square.
        """
        PieceToReturn = self._PieceInSquare
        self._PieceInSquare = None
        return PieceToReturn

    def GetPieceInSquare(self):
        """
        This function returns the piece in the square
        :return: The piece in the square.
        """
        return self._PieceInSquare

    def GetSymbol(self):
        """
        It returns the value of the variable _Symbol.
        :return: The symbol of the stock.
        """
        return self._Symbol

    def GetPointsForOccupancy(self, CurrentPlayer):
        """
        > This function returns 0 points for the current player

        :param CurrentPlayer: The player who is currently occupying the space
        :return: 0
        """
        return 0

    def GetBelongsTo(self):
        """
        It returns the value of the variable _BelongsTo.
        :return: The value of the _BelongsTo attribute.
        """
        return self._BelongsTo

    def ContainsKotla(self):
        """
        If the symbol of the current object is "K" or "k", return True, otherwise return False
        :return: a boolean value.
        """
        if self._Symbol == "K" or self._Symbol == "k":
            return True
        else:
            return False


# Kotla is a subclass of Square, and it has a constructor that takes in a Player and a Symbol, and it has a method called
# GetPointsForOccupancy that takes in a Player and returns an integer
class Kotla(Square):
    def __init__(self, P, S):
        """
        The function __init__() is a constructor that initializes the class Kotla

        :param P: The player who owns the kotla
        :param S: The symbol of the Kotla
        """
        super(Kotla, self).__init__()
        self._BelongsTo = P
        self._Symbol = S

    def GetPointsForOccupancy(self, CurrentPlayer):
        """
        If the square is occupied by a piece of the current player, return 5, if it's occupied by a piece of the opponent,
        return 1, else return 0

        :param CurrentPlayer: The player whose turn it is
        :return: The points for the player who is occupying the square.
        """
        if self._PieceInSquare is None:
            return 0
        elif self._BelongsTo.SameAs(CurrentPlayer):
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (
                    self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 5
            else:
                return 0
        else:
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (
                    self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 1
            else:
                return 0


# The MoveOption class is a class that contains a list of possible moves that a piece can make
class MoveOption:
    def __init__(self, N):
        """
        The function __init__() is a constructor that initializes the object's name and possible moves

        :param N: The name of the player
        """
        self._Name = N
        self._PossibleMoves = []

    def AddToPossibleMoves(self, M):
        """
        It takes a move (M) and adds it to the list of possible moves

        :param M: The move to be added to the list of possible moves
        """
        self._PossibleMoves.append(M)

    def GetName(self):
        """
        The function GetName() returns the value of the private variable _Name
        :return: The name of the person.
        """
        return self._Name

    def CheckIfThereIsAMoveToSquare(self, StartSquareReference, FinishSquareReference):
        """
        If the start square and the finish square are the same, then the piece can't move

        :param StartSquareReference: The reference of the square the piece is on
        :param FinishSquareReference: The square that the piece is trying to move to
        :return: A boolean value.
        """
        StartRow = StartSquareReference // 10
        StartColumn = StartSquareReference % 10
        FinishRow = FinishSquareReference // 10
        FinishColumn = FinishSquareReference % 10
        for M in self._PossibleMoves:
            if StartRow + M.GetRowChange() == FinishRow and StartColumn + M.GetColumnChange() == FinishColumn:
                return True
        return False


# The Move class is a class that represents a move in the game of chess.
class Move:
    def __init__(self, R, C):
        self._RowChange = R
        self._ColumnChange = C

    def GetRowChange(self):
        return self._RowChange

    def GetColumnChange(self):
        return self._ColumnChange


# It's a queue of MoveOption objects
class MoveOptionQueue:
    def __init__(self):
        """
        The function __init__() initializes the queue
        """
        self.__Queue = []

    def GetQueueAsString(self):
        """
        It takes a queue of movies and returns a string of the movies in the queue
        :return: The queue as a string.
        """
        QueueAsString = ""
        Count = 1
        for M in self.__Queue:
            QueueAsString += str(Count) + ". " + M.GetName() + "   "
            Count += 1
        return QueueAsString

    def Add(self, NewMoveOption):
        """
        It adds a new move option to the queue

        :param NewMoveOption: The MoveOption object to add to the queue
        """
        self.__Queue.append(NewMoveOption)

    def Replace(self, Position, NewMoveOption):
        """
        Replace(self, Position, NewMoveOption) replaces the MoveOption at Position with NewMoveOption.

        :param Position: The position in the queue to replace
        :param NewMoveOption: The new move option to replace the old one
        """
        self.__Queue[Position] = NewMoveOption

    def MoveItemToBack(self, Position):
        """
        It takes the item at the position specified by the user and moves it to the back of the queue

        :param Position: The position of the item you want to move to the back of the queue
        """
        Temp = self.__Queue[Position]
        self.__Queue.pop(Position)
        self.__Queue.append(Temp)

    def GetMoveOptionInPosition(self, Pos):
        """
        It returns the move option in the position of the queue

        :param Pos: The position of the move option in the queue
        :return: The move option in the position specified.
        """
        return self.__Queue[Pos]


# A player has a name, a direction, a score and a queue of move options
class Player:
    def __init__(self, N, D):
        """
        The __init__ function initializes the class with the name, direction, and score of the player

        :param N: Name of the player
        :param D: The direction the player is facing
        """
        self.__Score = 100
        self.__Name = N
        self.__Direction = D
        self.__Queue = MoveOptionQueue()

    def SameAs(self, APlayer):
        """
        If the player is not None and the player's name is the same as the name of the player who called the function,
        return True, otherwise return False

        :param APlayer: The player to compare to
        :return: The name of the player.
        """
        if APlayer is None:
            return False
        elif APlayer.GetName() == self.__Name:
            return True
        else:
            return False

    def GetPlayerStateAsString(self):
        """
        It returns a string that contains the player's name, score, and the contents of the player's move option queue.
        :return: The player's name, score, and the queue of moves.
        """
        return self.__Name + "\n" + "Score: " + str(
            self.__Score) + "\n" + "Move option queue: " + self.__Queue.GetQueueAsString() + "\n"

    def AddToMoveOptionQueue(self, NewMoveOption):
        """
        It adds a new move option to the queue

        :param NewMoveOption: The MoveOption object to add to the queue
        """
        self.__Queue.Add(NewMoveOption)

    def UpdateQueueAfterMove(self, Position):
        """
        It moves the item at the given position to the back of the queue

        :param Position: The position of the item in the queue
        """
        self.__Queue.MoveItemToBack(Position - 1)

    def UpdateMoveOptionQueueWithOffer(self, Position, NewMoveOption):
        """
        It replaces the MoveOption at the given position in the queue with the given MoveOption

        :param Position: The position in the queue to replace
        :param NewMoveOption: This is the new move option that will be added to the queue
        """
        self.__Queue.Replace(Position, NewMoveOption)

    def GetScore(self):
        """
        The function GetScore() returns the value of the private variable __Score
        :return: The score of the player.
        """
        return self.__Score

    def GetName(self):
        """
        The function GetName() returns the value of the private variable __Name
        :return: The name of the person.
        """
        return self.__Name

    def GetDirection(self):
        """
        It returns the direction of the robot.
        :return: The direction of the car.
        """
        return self.__Direction

    def ChangeScore(self, Amount):
        """
        The function ChangeScore() takes in a parameter called Amount, and adds it to the variable Score

        :param Amount: The amount to change the score by
        """
        self.__Score += Amount

    def CheckPlayerMove(self, Pos, StartSquareReference, FinishSquareReference):
        """
        It checks if there is a move from StartSquareReference to FinishSquareReference in the position Pos

        :param Pos: The position of the move in the queue
        :param StartSquareReference: The reference of the square the player wants to move from
        :param FinishSquareReference: The square that the player wants to move to
        :return: A boolean value.
        """
        Temp = self.__Queue.GetMoveOptionInPosition(Pos - 1)
        return Temp.CheckIfThereIsAMoveToSquare(StartSquareReference, FinishSquareReference)


def Main():
    """
    It creates a new game, plays it, and then prints "Goodbye!" and waits for the user to press enter
    """
    ThisGame = Dastan(6, 6, 4)
    ThisGame.PlayGame()
    print("Goodbye!")
    input()


#
if __name__ == "__main__":
    Main()
