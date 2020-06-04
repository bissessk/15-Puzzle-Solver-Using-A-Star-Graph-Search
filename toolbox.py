
class Node :
    '''
    Node class was used to store board object and store f(n)s
    '''
    def __init__ (self, data, parent = None, fn = None):
        '''
        init params : 
        1) data
        2) parent
        3) f(n) 
        '''
        self.data   = data;
        self.parent = parent;
        self.fn     = fn;

    def child(self, data):
        '''
        returns a Node object using the data passed in
        '''
        return Node(data,self);

    def sequence(self):
        '''
        helps determine solution sequence. returns a list of the path from the root to the current node
        '''
        node = self;
        seq_to_node = [];
        while node:
            seq_to_node.append(node);#(node.data);
            node = node.parent;
        return list(reversed(seq_to_node));

    def __repr__(self):
        '''
        repr to help with debugging
        '''
        string = "Node: \n"
        string += "\tData:\n"
        string += str(self.data)
        string += "\tf(n):\n"
        string += str(self.fn)
        return string

    def __eq__(self, other):
        '''
        overloading equals operator
        '''
        if self.data == other.data:
            return True;
        return False;

    def set_fn(self, fn):
        '''
        set new f(n). Relevant in a_star
        '''
        self.fn = fn;
        return;

class PriorityQueue :
    def __init__ (self):
        '''
        contains data and values
        priority - data with lowest corresponding values (f(n))
        '''
        self.data = [];
        self.values = [];
    
    def __find_min_index(self, lst):
        '''
        private method that returns then index of a lst that has the minimum value/n
        - used when popping
        '''
        min = lst[0];
        min_index = 0;
        for i in range(1, len(lst)):
            if (lst[i] < min):
                min = lst[i];
                min_index = i;
        return min_index;

    def __len__(self):
        '''
        returns number of things inside our PriorityQueue
        '''
        return len(self.data);

    def pop(self):
        '''
        pops data with the lowest value. Utilize the find_min_index private function
        '''
        min_index = self.__find_min_index(self.values);
        self.values.pop(min_index);
        data = self.data.pop(min_index);
        return data;

    def add(self, data, value):
        '''
        appends data and its value to its assocated list
        '''
        self.data.append(data);
        self.values.append(value);

    def not_empty(self):
        '''
        returns True if Priority Queue is not empty
        '''
        has_next_bool = (self.data != []);
        return has_next_bool;

    def has(self, data):
        '''
        Checks if there the data exists inside the PriorityQueue. Returns False otherwise.
        Parameters:
        \t1) data
        '''
        has_bool = (data in self.data)
        return has_bool;

    def get_val(self, data):
        '''
        returns the value associated with the data passed in
        '''
        data_index = self.data.index(data);
        return self.values[data_index];

    def remove (self, data):
        '''
        removes the data and associated value from the PriorityQueue
        '''
        rm_index = self.data.index(data);
        self.data.remove(data);
        self.values.pop(rm_index);

    def size(self):
        '''
        returns size of the PriorityQueue. This is probably redundant since I already overwritten the len function.
        '''
        size = len(self.data)
        return size;

    def __repr__(self):
        '''
        repr helps with debugging
        '''
        string = "\nPriorQ :\n"
        if (len(self.data) == 0):
            return string + "\tEmpty\n"
        for i in range(len(self.data)):
            if (i == (len(self.data) -1)):
                string +=  "\tdata: " + str(self.data[i]) + "\n"
                string += "\tvalue: " + str(self.values[i]) + "\n"
            else:
                string +=  "\tdata: " + str(self.data[i]) + "\n"
                string += "\tvalue: " + str(self.values[i]) + "\n\n"

        return string
