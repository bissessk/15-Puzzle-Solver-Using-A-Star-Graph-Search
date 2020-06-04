import copy;
# Copy was imported to utilize the deep copy method

class Board :
    '''
    The Board Class initializes Board States 
    '''
    def __init__ (self, board, goal, blank_tup):
        '''
        Parameters : 
        1) Current Board State Nested List
        2) Goal Board Nested List
        3) A Tuple that contains the position of the blank space
        '''
        self.board = board;
        self.goal = goal;
        self.blank_r = blank_tup[0]; 
        self.blank_c = blank_tup[1];
    
    def move (self, direction):
        '''
        Description : Works by swapping the tile moved with the blank space\n
        Parameters :
        \t1) A String "L", "R", "U", or "D" that represents the direction the player moves the tile
        '''
        if direction == "L":
            if direction in self.available_moves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r][self.blank_c+1] = \
                    self.board[self.blank_r][self.blank_c+1], self.board[self.blank_r][self.blank_c];
                self.blank_c += 1;

        if direction == "R":
            if direction in self.available_moves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r][self.blank_c-1] = \
                    self.board[self.blank_r][self.blank_c-1], self.board[self.blank_r][self.blank_c];
                self.blank_c -= 1;

        if direction == "U":
            if direction in self.available_moves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r-1][self.blank_c] = \
                    self.board[self.blank_r-1][self.blank_c], self.board[self.blank_r][self.blank_c];
                self.blank_r -= 1;

        if direction == "D":
            if direction in self.available_moves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r+1][self.blank_c] = \
                    self.board[self.blank_r+1][self.blank_c], self.board[self.blank_r][self.blank_c];
                self.blank_r += 1;

        return self;

    def available_moves(self):
        '''
        returns what moves are available by accounting for edge cases as a list
        '''
        legal_moves_lst = [];
        if self.blank_c != 3:
            legal_moves_lst.append("L");
        if self.blank_c != 0:
            legal_moves_lst.append("R");
        if self.blank_r != 0:
            legal_moves_lst.append("U");
        if self.blank_r != 3:
            legal_moves_lst.append("D");
        return legal_moves_lst;

    def get_board (self):
        '''
        returns the current board state as a nested list
        '''
        return self.board;

    def get_goal_board (self):
        '''
        returns the goal state of the board as a nested list
        '''
        return self.goal;

    def is_solved (self):
        '''
        method that checks when current state = goal state
        '''
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (self.board[row][col] != self.goal[row][col]):
                    return False;
        return True;

    def potential_board(self, move):
        '''
        returns board object with the states as if the move passed in was played/n

        Parameters:
        \t1) move as a string ("U", "D", "L" or "R")
        '''
        new_board_lst = copy.deepcopy(self.board)
        new_board = Board(new_board_lst, self.goal, (self.blank_r, self.blank_c))
        new_board.move(move);
        return new_board;
    
    def __eq__(self, other):
        '''
        used when the equals coperator is called\n
        iterates through entire nested list to determine if lists are the same
        '''
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (self.board[row][col] != other.board[row][col]):
                    return False;
        return True;
    
    def __repr__(self):
        '''
        Repr to help with debugging
        '''
        string="Board State: "
        for i in range(4):
            string += "[ "
            for j in range(4):
                string += str(self.board[i][j]) +" ";
            if i == 3:
                string +="]"
            else:
                string +="] , "
        return string;




