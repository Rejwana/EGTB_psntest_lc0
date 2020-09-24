import chess
import chess.syzygy
import chess.engine

from chess.engine import Cp, Mate, MateGiven
import csv
from pathlib import Path





def get_lc0_move(key,val):

    '''
    tablebase = chess.syzygy.open_tablebase("/Users/rejwanahaque/Downloads/Chess_Engins/EGTB/syzygy")
    #board = chess.Board("8/8/8/8/6b1/8/5k1K/5n2 w - - 0 1")
    board = chess.Board(key)
    table = chess.syzygy.Table("/Users/rejwanahaque/Downloads/Chess_Engins/EGTB/syzygy/KBNvK.rtbw")
    #print(table.variant)
    #print(tablebase.variant)
    print(board)
    print("WLD score",tablebase.probe_wdl(board))
    print("DTZ score",tablebase.probe_dtz(board))
    print("ab",tablebase.probe_ab(board,-3,3))
    print("Legal Move count",board.legal_moves.count())
    print("WDL table",tablebase.probe_dtz_table(board,tablebase.probe_wdl(board)))
    '''
    'Lc0'
    board = chess.Board(key)
    engine = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")
    engine.configure({"backend": 'blas',"WeightsFile":'/weights/weights_run1_10970.pb'})

    #engine.configure({"backend": 'blas',"syzygypath":'/Users/rejwanahaque/Downloads/Chess_Engins/EGTB/syzygy'})
    #engine.configure({"backend": 'blas',"logfile":"lc0_log_python","VerboseMoveStats":"true"})
    '''
    info = engine.analyse(board, chess.engine.Limit(nodes=10000))
    print("Analysis Score:", info['score'])
    print("Moves",info["pv"])
    print("Analysis items:", info.items())
    '''

    result_1 = engine.play(board, chess.engine.Limit(nodes=1))
    if result_1.move.uci() in val:
        print("match")
    print(result_1.move)


    result_10000 = engine.play(board, chess.engine.Limit(nodes=10000))
    if result_10000.move.uci() in val:
        print("match")
    print(result_10000.move)

    return result_1.move.uci(),result_10000.move.uci()

    '''
    #engine = chess.engine.SimpleEngine.popen_uci("/Users/rejwanahaque/Downloads/Chess_Engins/stockfish-11-mac/Mac/stockfish-11-64")
    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.3))    
        print(result.move)
        board.push(result.move)
    

    print(board)
    print(board.legal_moves.count())
    '''


key = '8/8/8/8/6b1/8/5k2/5n1K b - - 0 1'
val = ['g4f4']
policy, mcts = get_lc0_move(key,val)

myfile = open('moves.csv', 'w') 
wr = csv.writer(myfile, delimiter = ',')
wr.writerow(['key','policy','mcts'])
wr.writerow([key,policy,mcts])


'''
with open('output.csv', mode='r') as infile:
    reader = csv.reader(infile)
    best_moves = {rows[0]:rows[1] for rows in reader}



for key, val in best_moves.items():
    get_lc0_move(key,val)
'''
