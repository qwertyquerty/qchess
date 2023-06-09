import chess
import chess.polyglot
from chess import WHITE, BLACK, KING, PAWN

from const import *

def is_mate_score(score):
	return abs(score) + 1000 >= CHECKMATE

def is_quiet_move(board, move, quiescence_depth=0):
	if board.is_capture(move):
		return False
	
	if (quiescence_depth <= QUIESCENCE_CHECK_DEPTH_LIMIT) and board.gives_check(move):
		return False
	
	piece = board.piece_at(move.from_square)

	if piece.piece_type == PAWN:
		if chess.square_rank(move.to_square) >= 6 and piece.color == WHITE:
			return False
		if chess.square_rank(move.to_square) <= 1 and piece.color == BLACK:
			return False
		if move.promotion is not None:
			return False

	return True

def lerp(start, end, position): # linear interpolation between start and end
	return int((1-position) * start + position * end)

def shrink_history(table):
	for i in range(len(table)):
		for j in range(len(table[0])):
			for k in range(len(table[0][0])):
				table[i][j][k] = table[i][j][k] // HISTORY_SHRINK_FACTOR

def generate_pv_line(board, table):
	nboard = board.copy()
	
	pv = []

	zh = chess.polyglot.zobrist_hash(nboard)

	hashes = set()

	while zh in table and zh not in hashes:
		if table[zh][BEST_MOVE] is not None:
			pv.append(table[zh][BEST_MOVE])
			nboard.push(table[zh][BEST_MOVE])
			hashes.add(zh)
			zh = chess.polyglot.zobrist_hash(nboard)
		else:
			break
	
	return pv
