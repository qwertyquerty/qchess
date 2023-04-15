import chess
import chess.polyglot
from chess import WHITE, BLACK, KING, PAWN

import threading

import time

from functools import partial
print = partial(print, flush=True)

VERSION = "MADCHESS v1.0"
AUTHOR = "Madeline"

UPPER = 1
LOWER = 2
EXACT = 3
CHECKMATE = 10000

MAX_PTABLE_SIZE = 1000000

PIECE_VALUES = (0, 1, 3, 3, 5, 9, 0)
CP_PIECE_VALUES = (0, 100, 300, 300, 500, 900, 0)
ENDGAME_PIECE_COUNT = 16

MIDGAME_PIECE_POSITION_TABLES = (
	(None,),	
	( # Pawn
		0,  0,  0,  0,  0,  0,  0,  0,
		5, 10, 10,-20,-20, 10, 10,  5,
		5, -5,-10,  0,  0,-10, -5,  5,
		0,  0,  0, 20, 20,  0,  0,  0,
		5,  5, 10, 25, 25, 10,  5,  5,
		10, 10, 20, 30, 30, 20, 10, 10,
		50, 50, 50, 50, 50, 50, 50, 50,
		0,  0,  0,  0,  0,  0,  0,  0,
	),

	( # Knight
		-50,-40,-30,-30,-30,-30,-40,-50,
		-40,-20,  0,  5,  5,  0,-20,-40,
		-30,  5, 10, 15, 15, 10,  5,-30,
		-30,  0, 15, 20, 20, 15,  0,-30,
		-30,  5, 15, 20, 20, 15,  5,-30,
		-30,  0, 10, 15, 15, 10,  0,-30,
		-40,-20,  0,  0,  0,  0,-20,-40,
		-50,-40,-30,-30,-30,-30,-40,-50,
	),

	( # Bishop
		-20,-10,-10,-10,-10,-10,-10,-20,
		-10,  5,  0,  0,  0,  0,  5,-10,
		-10, 10, 10, 10, 10, 10, 10,-10,
		-10,  0, 10, 10, 10, 10,  0,-10,
		-10,  5,  5, 10, 10,  5,  5,-10,
		-10,  0,  5, 10, 10,  5,  0,-10,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-20,-10,-10,-10,-10,-10,-10,-20,
	),

	( # Rook
		0,  0,  0,  5,  5,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		5, 10, 10, 10, 10, 10, 10,  5,
		0,  0,  0,  0,  0,  0,  0,  0
	),

	( # Queen
		-20,-10,-10, -5, -5,-10,-10,-20,
		-10,  0,  5,  0,  0,  0,  0,-10,
		-10,  5,  5,  5,  5,  5,  0,-10,
		0,  0,  5,  5,  5,  5,  0, -5,
		-5,  0,  5,  5,  5,  5,  0, -5,
		-10,  0,  5,  5,  5,  5,  0,-10,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-20,-10,-10, -5, -5,-10,-10,-20
	),

	( # King
		20, 30, 10,  0,  0, 10, 30, 20,
		20, 20,  0,  0,  0,  0, 20, 20,
		-10,-20,-20,-20,-20,-20,-20,-10,
		-20,-30,-30,-40,-40,-30,-30,-20,
		-30,-40,-40,-50,-50,-40,-40,-30,
		-30,-40,-40,-50,-50,-40,-40,-30,
		-30,-40,-40,-50,-50,-40,-40,-30,
		-30,-40,-40,-50,-50,-40,-40,-30
	)
)

ENDGAME_PIECE_POSITION_TABLES = (
	(None,),	
	( # Pawn
		0,  0,  0,  0,  0,  0,  0,  0,
		5, 10, 10,-20,-20, 10, 10,  5,
		5, -5,-10,  0,  0,-10, -5,  5,
		0,  0,  0, 20, 20,  0,  0,  0,
		5,  5, 10, 25, 25, 10,  5,  5,
		10, 10, 20, 30, 30, 20, 10, 10,
		50, 50, 50, 50, 50, 50, 50, 50,
		0,  0,  0,  0,  0,  0,  0,  0,
	),

	( # Knight
		-50,-40,-30,-30,-30,-30,-40,-50,
		-40,-20,  0,  5,  5,  0,-20,-40,
		-30,  5, 10, 15, 15, 10,  5,-30,
		-30,  0, 15, 20, 20, 15,  0,-30,
		-30,  5, 15, 20, 20, 15,  5,-30,
		-30,  0, 10, 15, 15, 10,  0,-30,
		-40,-20,  0,  0,  0,  0,-20,-40,
		-50,-40,-30,-30,-30,-30,-40,-50,
	),

	( # Bishop
		-20,-10,-10,-10,-10,-10,-10,-20,
		-10,  5,  0,  0,  0,  0,  5,-10,
		-10, 10, 10, 10, 10, 10, 10,-10,
		-10,  0, 10, 10, 10, 10,  0,-10,
		-10,  5,  5, 10, 10,  5,  5,-10,
		-10,  0,  5, 10, 10,  5,  0,-10,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-20,-10,-10,-10,-10,-10,-10,-20,
	),

	( # Rook
		0,  0,  0,  5,  5,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		0,  0,  0,  0,  0,  0,  0,  0,
		5, 10, 10, 10, 10, 10, 10,  5,
		0,  0,  0,  0,  0,  0,  0,  0
	),

	( # Queen
		-20,-10,-10, -5, -5,-10,-10,-20,
		-10,  0,  5,  0,  0,  0,  0,-10,
		-10,  5,  5,  5,  5,  5,  0,-10,
		0,  0,  5,  5,  5,  5,  0, -5,
		-5,  0,  5,  5,  5,  5,  0, -5,
		-10,  0,  5,  5,  5,  5,  0,-10,
		-10,  0,  0,  0,  0,  0,  0,-10,
		-20,-10,-10, -5, -5,-10,-10,-20
	),

	( # King
		-50,-30,-30,-30,-30,-30,-30,-50,
		-30,-30,  0,  0,  0,  0,-30,-30,
		-30,-10, 20, 30, 30, 20,-10,-30,
		-30,-10, 30, 40, 40, 30,-10,-30,
		-30,-10, 30, 40, 40, 30,-10,-30,
		-30,-10, 20, 30, 30, 20,-10,-30,
		-30,-20,-10,  0,  0,-10,-20,-30,
		-50,-40,-30,-20,-20,-30,-40,-50
	)
)

COLOR_MOD = (-1, 1)

def score_move(board, move):
	score = 0

	attacker = board.piece_at(move.from_square)
	victim = board.piece_at(move.to_square)

	if victim is not None:
		# MVV LVA
		score += CP_PIECE_VALUES[victim.piece_type] - CP_PIECE_VALUES[attacker.piece_type]
	
	# Change in positional scoring
	score -= MIDGAME_PIECE_POSITION_TABLES[attacker.piece_type][move.from_square if board.turn else chess.square_mirror(move.from_square)]
	score += MIDGAME_PIECE_POSITION_TABLES[attacker.piece_type][move.to_square if board.turn else chess.square_mirror(move.to_square)]

	return score 

def sorted_moves(board):
	legal_moves = list(board.legal_moves)
	legal_moves.sort(key=lambda move: score_move(board, move), reverse=True)

	return legal_moves

def score_board(board):
	if board.is_checkmate():
		return CHECKMATE if board.turn else -CHECKMATE
	
	if board.is_fivefold_repetition() or board.is_insufficient_material() or board.is_stalemate():
		return 0

	score = 0

	endgame = len(board.piece_map()) <= ENDGAME_PIECE_COUNT

	for square in range(64):
		pc = board.color_at(square)

		if pc is not None:
			pt = board.piece_type_at(square)

			if endgame:
				score += ENDGAME_PIECE_POSITION_TABLES[pt][square if pc == WHITE else chess.square_mirror(square)] if pc else -ENDGAME_PIECE_POSITION_TABLES[pt][square if pc == WHITE else chess.square_mirror(square)]
			else:
				score += MIDGAME_PIECE_POSITION_TABLES[pt][square if pc == WHITE else chess.square_mirror(square)] if pc else -MIDGAME_PIECE_POSITION_TABLES[pt][square if pc == WHITE else chess.square_mirror(square)]
			
			score += CP_PIECE_VALUES[pt] if pc else -CP_PIECE_VALUES[pt]

	score += len(list(board.legal_moves)) if board.turn else -len(list(board.legal_moves))

	return score if board.turn else -score


nodes = 0
pt_hits = 0
search_start_time = 0

position_table = {}

stop = False
lock = threading.Lock()

def alpha_beta(board, current_depth, max_depth, alpha, beta):
	if stop:
		return None, None
	
	global nodes
	nodes += 1

	alpha_orig = alpha
	
	pt_hash = chess.polyglot.zobrist_hash(board)
	pt_entry = position_table.get(pt_hash)
	
	if pt_entry is not None and (pt_entry["leaf_distance"]) >= (max_depth-current_depth):
		if pt_entry["flag"] == EXACT:
			return pt_entry["value"], pt_entry["board"]
		elif pt_entry["flag"]  == LOWER:
			alpha = max(alpha, pt_entry["value"])
		elif pt_entry["flag"]  == UPPER:
			beta = min(beta, pt_entry["value"])
		
		if alpha >= beta:
			return pt_entry["value"], pt_entry["board"]


	if current_depth == max_depth or board.is_game_over() or board.is_repetition():
		score, end_board = quiescence(board, current_depth, max_depth, alpha, beta)
		return score, end_board

	best_board = board
	best_score = -CHECKMATE

	for move in sorted_moves(board):
		nboard = board.copy()
		nboard.push(move)

		score, end_board = alpha_beta(nboard, current_depth + 1, max_depth, -beta, -alpha)

		if score is None:
			return None, None

		score = -score

		if score > best_score:
			best_score = score
			best_board = end_board
			if pt_entry:
				pt_entry["value"] = score
				pt_entry["board"] = best_board

			if best_score > alpha:
				alpha = best_score

		if alpha >= beta:
			break

	if pt_entry is not None or len(position_table) < MAX_PTABLE_SIZE:
		if best_score <= alpha_orig:
			position_table[pt_hash] = {"leaf_distance": max_depth-current_depth, "flag": UPPER, "value": best_score, "board": best_board}
		elif best_score >= beta:
			position_table[pt_hash] = {"leaf_distance": max_depth-current_depth, "flag": LOWER, "value": best_score, "board": best_board}
		else:
			position_table[pt_hash] = {"leaf_distance": max_depth-current_depth, "flag": EXACT, "value": best_score, "board": best_board}

	return best_score, best_board


def quiescence(board, current_depth, max_depth, alpha, beta):
	global nodes
	nodes += 1

	score = score_board(board)

	if score >= beta:
		return beta, board

	alpha = max(alpha, score)

	if board.outcome() is not None or board.can_claim_draw():
		return score, board

	best_board = board

	quiescence_moves = [move for move in sorted_moves(board) if board.is_capture(move) or board.gives_check(move) or board.is_check()]

	for move in quiescence_moves:
		nboard = board.copy()
		nboard.push(move)

		score, end_board = quiescence(nboard, current_depth+1, max_depth, -beta, -alpha)
		score = -score

		if score >= beta:
			return beta, end_board
		
		if score > alpha:
			alpha = score
			best_board = end_board

	return alpha, best_board

def info_loop():
	global search_start_time
	search_start_time = time.time()
	start = search_start_time
	offset = 0
	while not stop:
		time.sleep(0.1)
		end = time.time()
		nps = (nodes-offset) / (end - start)
		offset = nodes
		start = time.time()

		pt_hash = chess.polyglot.zobrist_hash(board)
		entry = position_table.get(pt_hash)

		if entry:
			with lock:
				print(f"info nodes {nodes} nps {int(nps)} time {int((time.time()-search_start_time) * 1000)} hashfull {int(len(position_table) / MAX_PTABLE_SIZE * 1000)} depth {len(entry['board'].move_stack) - len(board.move_stack)} score cp {entry['value']} pv {' '.join([str(move) for move in entry['board'].move_stack[len(board.move_stack):]])}")

def begin(board):
	global stop
	global nodes
	stop = False
	nodes = 0
	depth = 0
	position_table.clear()

	while not stop:
		alpha_beta(board, 0, depth, -CHECKMATE, CHECKMATE)
		depth += 1

def halt():
	global stop
	stop = True

stop = True

board = chess.Board()

search_thread = threading.Thread(target=lambda: begin(board), daemon=True)
node_info_thread = threading.Thread(target=lambda: info_loop(), daemon=True)

while True:
	line = input()
	args = line.split()
	cmd = args[0] if len(args) else None

	if cmd == "uci":
		print(f"id name {VERSION}")
		print(f"id author {AUTHOR}")
		print("uciok")
	
	elif cmd == "isready":
		print("readyok")
	
	elif cmd == "quit":
		halt()
		break

	elif cmd == "position":
		if "fen" in args:
			fen = line.split(" fen ")[1].split("moves")[0]
			board = chess.Board(fen=fen)
		elif "startpos" in args:
			board = chess.Board()
			
		if "moves" in args:
			moves = line.split(" moves ")[1].split()
			for move in moves:
				board.push(chess.Move.from_uci(move))
			
	elif cmd == "go":
		if stop:
			search_thread = threading.Thread(target=lambda: begin(board), daemon=True)
			node_info_thread = threading.Thread(target=lambda: info_loop(), daemon=True)
			search_thread.start()
			node_info_thread.start()

	elif cmd == "stop":
		halt()
		while search_thread.is_alive() or node_info_thread.is_alive():
			pass