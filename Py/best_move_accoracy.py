import chess
import chess.syzygy
import chess.engine
from chess.engine import Cp, Mate, MateGiven
import csv
from pathlib import Path


#tablebase = chess.syzygy.open_tablebase("/Users/rejwanahaque/Downloads/Chess_Engins/EGTB/syzygy")
'Lc0'
engine_MCTS = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")
engine_Policy = chess.engine.SimpleEngine.popen_uci("/lc0/build/release/lc0")

#engine_Policy.configure({"backend": 'blas',"syzygypath":'/Users/rejwanahaque/Downloads/Chess_Engins/EGTB/syzygy'})
#engine_Policy.configure({"backend": 'blas',"logfile":"lc0_log_python","VerboseMoveStats":"true"})
engine_MCTS.configure({"backend": 'blas',"WeightsFile":'/weights/weights_run1_10970.pb'})
engine_Policy.configure({"backend": 'blas',"WeightsFile":'/weights/weights_run1_10970.pb'})


global total_psn_w_move 


#def get_lc0_move(key,total_psn_w_move):
def get_lc0_move(board):

    '''move with search'''
   
    result_MCTS = engine_MCTS.play(board, chess.engine.Limit(nodes=400))

    '''move without search'''
    result_Policy = engine_Policy.play(board, chess.engine.Limit(nodes=1))
    

    return result_MCTS.move.uci(),result_Policy.move.uci()
    #return result_Policy.move.uci()
    



def get_EGTB():

    #with open('test_KQkq.csv', mode='r') as infile:
    with open('Moves/sample_KQkq.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = next(reader)

        moves = {rows[1]:rows[2:8] for rows in reader}

        return moves
      


def start():
    
    moves = get_EGTB()
    
    total_psn_w_move = 0
    Policy_best = 0
    MCTS_best = 0

    total_winning_psn = 0
    Policy_win = 0
    MCTS_win = 0

    total_drawing_psn = 0
    total_loasing_psn = 0

    drawing_psn_w_loasing_move = 0
    can_draw_policy = 0
    can_draw_mcts = 0

    '''
    best_win_S = 0
    best_draw_S = 0
    best_loos_S = 0

    best_win_P = 0
    best_draw_P = 0
    best_loos_P = 0
    '''


    myfile = open('failing_KQkq.csv', 'w') 
    wr = csv.writer(myfile, delimiter = ',')
    wr.writerow(['position','WDL','Policy_pred','MCTS_pred','winning_moves','drawing_moves','loasing_moves','move_Policy','move_MCTS'])


    for key, val in moves.items():
    
        winning_moves = val[0]
        loasing_moves = val[1]
        drawing_moves = val[2]
        best_moves = val[3]
        WLD = val[4]

        #for game record
        Policy_pred = 0
        MCTS_pred = 0
        
        #print(key, winning_moves, loasing_moves,drawing_moves,best_moves)

        #print(key)


        board = chess.Board(key)
    
        if not ((board.is_stalemate()) or (board.is_checkmate())) and (board.legal_moves.count()>1):
            move_MCTS,move_Policy = get_lc0_move(board)
            #move_Policy = get_lc0_move(board)
            #print(board.legal_moves.count())
            total_psn_w_move += 1
            '''
            if (len(winning_moves)>2):
                total_winning_psn += 1
            elif (len(drawing_moves)>2):
                total_drawing_psn += 1
            elif (len(loasing_moves)>2):
                total_loasing_psn += 1
            '''
            
            if (WLD == 'W'):
                total_winning_psn += 1
            elif (WLD == 'D'):
                total_drawing_psn += 1
            else:
                total_loasing_psn += 1
            
            if (WLD == 'W'):
                #as [ and ] is counted as elements of winning_move so no elements means len 2
                
                if move_Policy in winning_moves:
                    Policy_win += 1
                    Policy_pred = 1
                if move_MCTS in winning_moves:
                    MCTS_win += 1
                    MCTS_pred = 1
                
                if (((Policy_pred==0)or(MCTS_pred==0))and(WLD != 'L')):
                    wr.writerow([key,WLD,Policy_pred,MCTS_pred,winning_moves,drawing_moves,loasing_moves,move_Policy,move_MCTS])
                
            elif((len(drawing_moves)>2)and (len(loasing_moves)>2)):
                drawing_psn_w_loasing_move += 1

                if move_Policy in drawing_moves:
                    can_draw_policy += 1
                    Policy_pred = 1
                    #print("match policy")

                if move_MCTS in drawing_moves:
                    can_draw_mcts += 1
                    MCTS_pred = 1
                    #print("match search")
                
                if (((Policy_pred==0)or(MCTS_pred==0))and(WLD != 'L')):
                    wr.writerow([key,WLD,Policy_pred,MCTS_pred,winning_moves,drawing_moves,loasing_moves,move_Policy,move_MCTS])
                
            
            
            
            #print(key,move_MCTS,move_Policy,val)
            '''
            if move_Policy in best_moves:
                Policy_best += 1
                if (WLD == 'W'):
                    best_win_P +=1
                elif (WLD == 'D'):
                    best_draw_P +=1
                else:
                    best_loos_P +=1
                    

            if move_MCTS in best_moves:
                MCTS_best += 1
                if (WLD == 'W'):
                    best_win_S +=1
                elif (WLD == 'D'):
                    best_draw_S +=1
                else:
                    best_loos_S +=1
                #print("match search")
            '''

        


    print ("total number of positions with move", total_psn_w_move)
    print("total correct prediction of best move by policy", Policy_best)
    print("total correct prediction of best move by mcts", MCTS_best)

    print ("total winning psn ", total_winning_psn)
    print("total correct prediction of winning move by policy", Policy_win)
    print("total correct prediction of winning move by mcts", MCTS_win)

    print("total drawing psn",total_drawing_psn)
    print("total loasing psn",total_loasing_psn)

    print("total drawing psn with loasing move",drawing_psn_w_loasing_move)
    print("can draw drawing psn policy",can_draw_policy)
    print("can draw drawing psn mcys",can_draw_mcts)

    '''
    print ("best winning move mcts",best_win_S)
    print ("best drawing move mcts",best_draw_S)
    print ("best losing move mcts",best_loos_S)

    print ("best winning move policy",best_win_P)
    print ("best drawing move policy",best_draw_P)
    print ("best losing move policy",best_loos_P)
    '''


start()
