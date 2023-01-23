class Node:
    def __init__(self, initial_data = None):
        self.data = initial_data
        self.neighbors = [None] * 8

    def get_topleft(self):
        return self.neighbors[0]

    def set_topleft(self, new):
        self.set_neighbor(new, 0)

    def get_top(self):
        return self.neighbors[1]

    def set_top(self, new):
        self.set_neighbor(new, 1)

    def get_topright(self):
        return self.neighbors[2]

    def set_topright(self, new):
        self.set_neighbor(new, 2)

    def get_right(self):
        return self.neighbors[3]

    def set_right(self, new):
        self.set_neighbor(new, 3)

    def get_bottomright(self):
        return self.neighbors[4]

    def set_bottomright(self, new):
        self.set_neighbor(new, 4)

    def get_bottom(self):
        return self.neighbors[5]

    def set_bottom(self, new):
        self.set_neighbor(new, 5)

    def get_bottomleft(self):
        return self.neighbors[6]

    def set_bottomleft(self, new):
        self.set_neighbor(new, 6)

    def get_left(self):
        return self.neighbors[7]

    def set_left(self, new):
        self.set_neighbor(new, 7)

    def get_neighbors(self):
        return self.neighbors

    def get_nonNone_neighbors(self):
        out = []
        for neighbor in self.neighbors:
            if neighbor is not None:
                out.append(neighbor)

        return out

    def set_neighbors(self, new_neighbors):
        for item in new_neighbors:
            if type(item) != type(Node()) and type(item) != None:
                raise Exception('Neighbors must be an instance of the Node class or None')

        if len(new_neighbors) != 8:
            raise Exception('len(new_neighbors) must be 8')

        self.neighbors = new_neighbors


    def set_neighbor(self, new_neighbor, pos):
        if type(new_neighbor) != type(Node()) and type(new_neighbor) != None:
            raise Exception('Neighbors must be an instance of the Node class or None')

        if pos not in range(0, 8):
            raise Exception('pos value must be between 0-7')

        self.neighbors[pos] = new_neighbor

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data

    def __str__(self):
        return self.data.__str__()

    def get_position(self):
        x = 0
        cur_node = self
        while cur_node.get_left() != None:
            x += 1
            cur_node = cur_node.get_left()
        
        y = 0
        cur_node = self
        while cur_node.get_top() != None:
            y += 1
            cur_node = cur_node.get_top()

        return (x, y)

    

    
class LinkedArray:
    def __init__(self, width, height, assign_diagonal_neighbors = True):
        self.width = width
        self.height = height
        self.top_left = self.create_lattice(width, height, assign_diagonal_neighbors)

    def create_lattice(self, width, height, diag_flag):

        def new_node_list(length):
            cur_node = Node()
            out = [cur_node]
            for i in range(length - 1):
                new_node = Node()
                cur_node.set_right(new_node)
                new_node.set_left(cur_node)
                out.append(new_node)
                cur_node = new_node

            return out

        def fuse_lists(upper_list, lower_list):
            for index in range(len(upper_list)):
                upper_list[index].set_bottom(lower_list[index])
                lower_list[index].set_top(upper_list[index])

            if diag_flag:
                for index in range(len(upper_list) - 1):
                    upper_list[index].set_bottomright(lower_list[index + 1])
                    upper_list[index + 1].set_bottomleft(lower_list[index])
                    lower_list[index].set_topright(upper_list[index + 1])
                    lower_list[index + 1].set_topleft(upper_list[index])

            return lower_list


        cur_list = new_node_list(width)
        top_left = cur_list[0]
        for i in range(height - 1):
            new_list = new_node_list(width)
            cur_list = fuse_lists(cur_list, new_list)

        return top_left


    def get_node(self, x, y):
        if not 0 <= x < self.width:
            raise Exception(f'x out of bounds with value {x}')
        if not 0 <= y < self.height:
            raise Exception(f'y out of bounds with value {y}')

        cur_node = self.top_left
        for i in range(x):
            cur_node = cur_node.get_right()
        for i in range(y):
            cur_node = cur_node.get_bottom()

        return cur_node

    def get_data(self, x, y):
        node = self.get_node(x, y)
        return node.get_data()


    def set_data(self, x, y, new_data):
        node = self.get_node(x, y)
        node.set_data(new_data)


    def __str__(self):
        
        def row_to_text(cur_node):
            txt = ''
            while cur_node is not None:
                txt += cur_node.__str__() + ' '
                cur_node = cur_node.get_right()
            return txt

        cur_node = self.top_left
        out = '\n'
        while cur_node is not None:
            out += row_to_text(cur_node) + '\n'
            cur_node = cur_node.get_bottom()

        return out


    def visit_nodes(self, func):
        anchor_node = self.top_left
        while anchor_node != None:
            cur_node = anchor_node
            while cur_node != None:
                func(cur_node)
                cur_node = cur_node.get_right()
            anchor_node = anchor_node.get_bottom()




if __name__ == '__main__':
    linked_array = LinkedArray(5, 5)
