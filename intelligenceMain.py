# 15 Puzzle
# Artifical Intelligence

from   Board   import Board;
from   toolbox import Node;
from   toolbox import PriorityQueue;
import copy;

def get_indicies(val , board_lst):
    '''
    Returns indicies as a tuple given the value and the boardlist. Works by iterating through entire board list
    Parameters:
    \t1) Value to search for
    \t2) boardlist to search through
    '''
    for row in range(len(board_lst)):
        for col in range(len(board_lst[row])):
            if (board_lst[row][col] == val) :
                return (row,col);

def manhattan_dist(board):
    '''
    Calculates the sum of manhattan distances given the current board state. Works by iterating through entire board.
    Parameters:
    \t1) Board Object (current state of the board)
    '''
    curr_state = board.get_board();
    goal_state = board.get_goal_board();

    sum = 0
    for row in range(len(curr_state)):
        for col in range(len(curr_state[row])):
            if (curr_state[row][col] != 0):
                ind_curr =  (row,col);
                ind_goal =   get_indicies(curr_state[row][col], goal_state);
                diff_x   =   abs(ind_curr[0] - ind_goal[0]);
                diff_y   =   abs(ind_curr[1] - ind_goal[1]);
                sum      +=  diff_x;
                sum      +=  diff_y;
            else:
                pass
    return sum;

def a_star(board, heuristic):
    '''
    A Star search Algorithm takes in a board state and a heuristic function and solves the board. It returns the solution sequence and the number of nodes generated
    Parameters:
    \t1) Board Object
    \t1) Heuristic Function
    '''
    # initialize frontier and explored
    frontier = PriorityQueue();
    node = Node(board, None, heuristic(board));
    explored = PriorityQueue();
    num_nodes_gen = 1;
    # add root to frontier
    frontier.add(node, heuristic(node.data) + (len(node.sequence()) - 1));
    
    #while the frontier is not empty
    while frontier.not_empty():
        node = frontier.pop();

        # check if lowest is the goal
        if node.data.is_solved():
            print("solved\n", "\tExplored Length :", len(explored), "\n\tNodes Gen :", num_nodes_gen,"\n");
            return (node.sequence(), num_nodes_gen);

        #expand node
        for move in node.data.available_moves():
            child = Node(node.data.potential_board(move), node);
            num_nodes_gen +=1;
            child.set_fn(heuristic(child.data) + len(child.sequence()) - 1)
            
            # child not in explored and not in frontier
            if (frontier.has(child)==False) and (explored.has(child) == False) : #(child.data not in explored):
                frontier.add(child, (heuristic(child.data) + len(child.sequence()) - 1) );
            
            # child is in frontier
            elif frontier.has(child):
                child_f_n = heuristic(child.data) + (len(child.sequence())-1);

                if (child_f_n < frontier.get_val(child)):
                    frontier.remove(child);
                    child.set_fn(child_f_n);
                    frontier.add(child, child_f_n);

                if (explored.has(child)):
                    explored.remove(child);
            
            #child.data in explored:
            elif explored.has(child) : 
                child_f_n = heuristic(child.data) + (len(child.sequence())-1);
                if (child_f_n < explored.get_val(child)):
                    explored.remove(child);
                    child.set_fn(child_f_n);
                    frontier.add(child, child_f_n);
            
            #append to explored
            if explored.has(child) == False:
                explored.add(child, heuristic(child.data) + (len(child.sequence())-1))
    
    return None, num_nodes_gen;

def find_move_seq(board_seq_lst):
    '''
    Returns a list of move sequences given the list of board sequences received from the A star algorithm.
    Paramters:
    \t1) list of solution sequence of board states
    '''
    coor_lst = [];
    for i in range(len(board_seq_lst)): # iterate through board solution sequence
        coor_lst.append(get_indicies(0 , board_seq_lst[i]));
    #print(coor_lst)
    move_lst = [];
    for i in range(len(coor_lst)-1): # move list is one less that solution sequence
        delta_row = coor_lst[i][0] - coor_lst[i+1][0];
        delta_col = coor_lst[i][1] - coor_lst[i+1][1];

        if delta_row == -1:
            move_lst.append("U");
        if delta_row == 1:
            move_lst.append("D");
        if delta_col == -1:
            move_lst.append("L");
        if delta_col == 1:
            move_lst.append("R");

    return move_lst;

def print_file_contents(file):
    '''
    Used for debugging, prints the contents of any file
    '''
    if file.mode == "r":
        contents = file.read();
        print(contents);

def get_init_and_goal_boards(file):
    '''
    Given the input file, this function returns the intial and goal states of the board as a nested list
    '''
    init_board = []
    final_board = []
    counter = -1;
    f_lines = file.readlines();

    for i in f_lines:
        counter+=1;
        if counter < 4:
            init_board.append(i.strip().split(" "));

        elif (counter < 9) and (counter > 4):
            final_board.append(i.strip().split(" "));
    
    for i in range(4):
        init_board[i] = [int(i) for i in init_board[i]];
        final_board[i] = [int(i) for i in final_board[i]] 

    return (init_board, final_board )

def make_blank_move_lst(move_lst):
    '''
    Because the assignment defines the solution sequences as the movement of the blank space, this function converts our move\
    list of tiles to the movement of the blank space. Works by iterating though move list and a making a new list.
    '''
    blank_moves = [];
    for i in range(len(move_lst)):
        if move_lst[i] == "R":
            blank_moves.append("L");

        elif move_lst[i] == "L":
            blank_moves.append("R");

        elif move_lst[i] == "U":
            blank_moves.append("D");

        elif move_lst[i] == "D":
            blank_moves.append("U");

    return blank_moves;

def print_process_file(file):
    '''
    Used for debugging - process the input files and prints the results instead of creating output files
    '''
    f_i_1 = file;
    board_init_lst_1, board_goal_lst_1 = get_init_and_goal_boards(f_i_1);

    # Construct Boards
    blank_tup_1 = get_indicies(0, board_init_lst_1);
    board_prob_1 = Board(board_init_lst_1, board_goal_lst_1, blank_tup_1);

    # Solve Board
    seq_1, num_explored_1 = a_star(board_prob_1, manhattan_dist);
    
    # Print solution sequence
    print("\nSolution Sequence: ");
    print("\tData:")
    for i in range(len(seq_1)):
        print("\t\t",seq_1[i].data);
    
    # print f(n) values
    print("\tf(n):")
    for i in range(len(seq_1)):
        print("\t\t",seq_1[i].fn);
    
    # print Moves
    print("\tMoves:")
    board_lst_1 = []
    for i in range(len(seq_1)):
        board_lst_1.append(seq_1[i].data.get_board())
    
    move_lst_1 = find_move_seq(board_lst_1);
    blank_lst = make_blank_move_lst(move_lst_1);
    for i in range(len(move_lst_1)):
        print("\t\t", blank_lst[i]);
    
    #print N
    print("\nNum Explored: ", num_explored_1,"\n")
    #print d
    print("d = ", len(board_lst_1) - 1, "\n");

def process_file(file):
    '''
    solves the board in a way that makes it easier to write outfiles
    '''
    f_i_1 = file;
    board_init_lst_1, board_goal_lst_1 = get_init_and_goal_boards(f_i_1);

    # Construct Boards
    blank_tup_1 = get_indicies(0, board_init_lst_1);
    board_prob_1 = Board(board_init_lst_1, board_goal_lst_1, blank_tup_1);

    # Solve Board
    seq_1, num_explored_1 = a_star(board_prob_1, manhattan_dist);
    
    fn_lst = [];
    for i in range(len(seq_1)):
        fn_lst.append(seq_1[i].fn);
    
    board_lst_1 = []
    for i in range(len(seq_1)):
        board_lst_1.append(seq_1[i].data.get_board())
    
    move_lst_1 = find_move_seq(board_lst_1);
    

    d = len(board_lst_1) - 1;

    return board_init_lst_1, board_goal_lst_1, move_lst_1, fn_lst, num_explored_1, d

def write_board(f_o, board_lst):
    '''
    write out any board (initial or goal) to an output file (f_o) given the output file stream and the board list
    '''
    for i in range(4):
        for j in range(4):
            f_o.write(str(board_lst[i][j]) + " ");
            if j == 3:
                f_o.write("\n");

    f_o.write("\n");

def write_lst(f_o, lst):
    '''
    writes out any list to an output file iven the output file stream and the lst
    '''
    for i in range(len(lst)):
        f_o.write(str(lst[i]) + " ");
        
def write_out(f_o, board_lst, goal_lst, d, num_explored, move_lst, fn_lst ):
    '''
    writes out given all the necessary information
    Parameters:
    \t1) output file stream
    \t2) intial board list
    \t3) goal goard list
    \t4) shawllowest depth
    \t5) Number of nodes generated
    \t6) list of moves
    \t7) list of f(n) values
    '''
    write_board(f_o, board_lst);
    write_board(f_o, goal_lst);

    f_o.write(str(d) + "\n");
    f_o.write(str(num_explored) + "\n");

    blank_movements_lst = make_blank_move_lst(move_lst);

    write_lst(f_o, blank_movements_lst);
    f_o.write("\n");
    write_lst(f_o, fn_lst);

    return 

def project_printer(f_i_1, f_i_2, f_i_3, f_i_4):
    '''
    prints solution of problems given input files
    '''
    print("\n-------------------------------   FILE 1   -------------------------------   ");
    print_process_file(f_i_1);
    print("\n-------------------------------   FILE 2   -------------------------------   ");
    print_process_file(f_i_2);
    print("\n-------------------------------   FILE 3   -------------------------------   ");
    print_process_file(f_i_3);
    print("\n-------------------------------   FILE 4   -------------------------------   ");
    print_process_file(f_i_4);

def main():
    '''
    Main
    '''

    f_i_1 = open("Input1.txt", "r");
    f_i_2 = open("Input2.txt", "r");
    f_i_3 = open("Input3.txt", "r");
    f_i_4 = open("Input4.txt", "r");
    
    #project_printer(f_i_1, f_i_2, f_i_3, f_i_4);
    
    board_lst1, goal_lst1, move_lst_1, fn_lst_1, num_explored_1, d_1 = process_file(f_i_1);
    board_lst2, goal_lst2, move_lst_2, fn_lst_2, num_explored_2, d_2 = process_file(f_i_2);
    board_lst3, goal_lst3, move_lst_3, fn_lst_3, num_explored_3, d_3 = process_file(f_i_3);
    board_lst4, goal_lst4, move_lst_4, fn_lst_4, num_explored_4, d_4 = process_file(f_i_4); 

    f_o_1 = open("Output1.txt","w+");
    f_o_2 = open("Output2.txt","w+");
    f_o_3 = open("Output3.txt","w+");
    f_o_4 = open("Output4.txt","w+");

    write_out(f_o_1, board_lst1, goal_lst1, d_1, num_explored_1, move_lst_1, fn_lst_1);
    write_out(f_o_2, board_lst2, goal_lst2, d_2, num_explored_2, move_lst_2, fn_lst_2);
    write_out(f_o_3, board_lst3, goal_lst3, d_3, num_explored_3, move_lst_3, fn_lst_3);
    write_out(f_o_4, board_lst4, goal_lst4, d_4, num_explored_4, move_lst_4, fn_lst_4);

main(); # call main
