import json
import random

from tictactoe_symmetry import *

__author__ = 'Glenn'

logging.basicConfig(level=logging.INFO)
class roboplayer:
    def __init__(self):
        self.boardDict = {}
        self.load_from_file('move_dict.dat')
        self.move_record = []

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                self.boardDict = json.load(f)
        except IOError:
            pass

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.boardDict, f)

    def _empty(self, board_string):
        canon_board, symmetry = canonical_board(board_string)
        board_list = boardutils.blank_list(canon_board)
        if not canon_board in self.boardDict:
            self.boardDict[canon_board] = 4 * board_list

    def get_move(self, board_string):
        # time.sleep(2)
        self._empty(board_string)
        canon_board, symmetry = canonical_board(board_string)
        moveList = self.boardDict[canon_board]
        assert len(moveList) > 0
        if len(moveList) > 1:
            randomIndex = random.randint(0, len(moveList) - 1)
        else:
            randomIndex = 0
        logging.debug('Canonical_board[0]:\n %s', boardutils.readable_board_string(canon_board))
        logging.debug('random index of moveList is: %d', moveList[randomIndex])
        logging.debug('Symmetry used = %d', symmetry)
        symm_move = get_symm_index(moveList[randomIndex], symmetry)
        self.move_record.append((canon_board, moveList[randomIndex]))
        logging.debug('Symmetry move is: %d', symm_move)
        return symm_move

    def adjust(self, board):
        winner = boardutils.winner(board)
        logging.debug(winner)
        move_length = len(self.move_record)
        if winner == 'O':
            for i in range(0, move_length):
                movesTuple = self.move_record[i]
                logging.debug(movesTuple)
                boardInstance = movesTuple[0]
                if boardInstance != self.move_record[move_length - 1][0]:
                    logging.debug(boardInstance)
                    logging.debug(movesTuple[1])
                    self.boardDict[boardInstance].append(movesTuple[1])
                else:
                    self.boardDict[boardInstance[0]] = [movesTuple[1]]
        elif winner == 'X':
            for i in range(0, len(self.move_record)):
                movesTuple = self.move_record[i]
                logging.debug(movesTuple)
                boardInstance = movesTuple[0]
                if boardInstance != self.move_record[move_length - 1][0]:
                    logging.info(boardInstance)
                    logging.info(movesTuple[1])
                    logging.info(self.boardDict[boardInstance])
                    assert boardInstance == movesTuple[0]
                    self.boardDict[boardInstance].remove(movesTuple[1])
                else:
                    self.boardDict[boardInstance] = [movesTuple[1]]
        logging.info(self.boardDict)
        self.save_to_file('move_dict.dat')