from LinkedArray import LinkedArray
from pgl import GWindow, GRect, GLabel, GCompound, GPolygon, GLine
from math import floor
from random import randint
import json


'''
--todo--
- maybe store local highscores?
'''


class Minesweeper:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.linked_array = LinkedArray(width, height)
        self.running = True
        self.left_to_reveal = width * height - mines
        self.flag_mode = False
        self.flag_num = 0
        self.current_time = 0.0

        #graphical constants
        self.TILE_SIZE = 30
        self.HEADER = 50
        self.FOOTER = 10
        self.MARGIN = 10
        self.FONT_SIZE = self.TILE_SIZE * .8
        self.LABEL_COLORS = {1:'blue', 2:'green', 3:'red', 4:'purple', 5:'maroon', 6:'turquoise', 7:'brown', 8:'pink'}
        self.gw = GWindow(self.TILE_SIZE * self.width + 2 * self.MARGIN, self.TILE_SIZE * self.height + self.HEADER + self.FOOTER)
        
    

        def red_cover(node):
            node.cover.set_fill_color('red')

        def green_cover(node):
            node.cover.set_fill_color('green')


        def click(node):
            if not self.flag_mode:
                if self.left_to_reveal == self.width * self.height - self.mines:
                    self.populate([node] + node.get_nonNone_neighbors())
                    self.timer_interval = self.gw.set_interval(timer_action, 100)
                    
                node.tile.remove(node.cover)
                node.revealed = True
                self.left_to_reveal -= 1

                if node.has_flag:
                    node.tile.remove(node.flag)
                    self.flag_num -= 1
                    self.remaining_mines.set_label(str(self.mines - self.flag_num))

                if node.mine:
                    self.linked_array.visit_nodes(red_cover)
                    self.running = False
                    self.timer_interval.stop()
                
                elif node.neighbor_mines == 0:
                    for node in node.get_nonNone_neighbors():
                        if not node.revealed:
                            click(node)

                elif self.left_to_reveal == 0:
                    self.linked_array.visit_nodes(green_cover)
                    self.running = False
                    self.timer_interval.stop()
                    check_for_highscore(round(self.current_time, 2))

                

            elif self.flag_mode and node.revealed == False: 
                if not node.has_flag:
                    node.tile.add(node.flag)
                    node.has_flag = True
                    self.flag_num += 1
                    self.remaining_mines.set_label(str(self.mines - self.flag_num))
                else:
                    node.tile.remove(node.flag)
                    node.has_flag = False
                    self.flag_num -= 1
                    self.remaining_mines.set_label(str(self.mines - self.flag_num))

            
            
        def click_action(e):
            if self.running:
                x, y = e.get_x(), e.get_y()
                node_pos_x = floor((x - self.MARGIN) / self.TILE_SIZE)
                node_pos_y = floor((y - self.HEADER) / self.TILE_SIZE)
                if 0 <= node_pos_x < self.width and 0 <= node_pos_y < self.height:
                    node = self.linked_array.get_node(node_pos_x, node_pos_y)
                    click(node)

        def add_vars(node):
            node.mine = False
            node.revealed = False
            node.neighbor_mines = 0
            node.tile = GCompound()
            node.has_flag = False

            pos = node.get_position()
            self.gw.add(node.tile, self.TILE_SIZE * pos[0] + self.MARGIN, self.TILE_SIZE * pos[1] + self.HEADER)

        def key_action(e):
            if e.get_key() == '<SPACE>':
                self.flag_mode = not self.flag_mode
                
                if self.flag_mode:
                    self.inner.set_color('green')
                    self.mode_display.remove(self.x)
                    self.mode_display.add(self.flag)
                
                else:
                    self.inner.set_color('red')
                    self.mode_display.remove(self.flag)
                    self.mode_display.add(self.x)

        def timer_action():
            self.current_time += 0.1
            self.timer_label.set_label(str(round(self.current_time, 2)))

        def check_for_highscore(score):
            try:
                file = open(f'{self.width}_{self.height}_{self.mines}.json', 'x')
                file.close()
                file = open(f'{self.width}_{self.height}_{self.mines}.json', 'w')
                file.write(json.dumps({'width': self.width, 'height': self.height, 'mines': self.mines, 'score': 9999}))
                file.close()
            except FileExistsError:
                pass

            file = open(f'{self.width}_{self.height}_{self.mines}.json', 'r')
            best = json.loads(file.readline())['score']
            file.close()

            if score < best:
                file = open(f'{self.width}_{self.height}_{self.mines}.json', 'w')
                file.write(json.dumps({'width': self.width, 'height': self.height, 'mines': self.mines, 'score': score}))
                file.close()

                comp = GCompound()

                rect = GRect(200, 50)
                rect.set_filled(True)
                rect.set_color('black')
                rect.set_fill_color('white')
                comp.add(rect, 0, 0)

                label = GLabel('You got a highscore!')
                label.set_font(' 20px helvetica')
                comp.add(label, (comp.get_width() - label.get_width()) / 2, comp.get_height() / 2 + label.get_ascent() / 2)

                self.gw.add(comp, (self.gw.get_width() - comp.get_width()) / 2, (self.gw.get_height() - comp.get_height()) / 2)


        self.init_nonNode_graphics()
        self.linked_array.visit_nodes(add_vars)
        self.add_tiles()
        self.gw.add_event_listener('click', click_action)
        self.gw.add_event_listener('key', key_action)


    def init_nonNode_graphics(self):
        #mode display
        self.mode_display = GCompound()

        rect = GRect(self.TILE_SIZE, self.TILE_SIZE)
        rect.set_filled(False)
        self.mode_display.add(rect)

        self.inner = GRect(self.TILE_SIZE - 2, self.TILE_SIZE - 2)
        self.inner.set_filled(False)
        self.inner.set_color('red')
        self.mode_display.add(self.inner, 1, 1)

        self.x = GCompound()
        for i in range(2):
            line = GLine(1/6 * self.TILE_SIZE, 1/6 * self.TILE_SIZE, 5/6 * self.TILE_SIZE, 5/6 * self.TILE_SIZE)
            line.set_line_width(4)
            self.x.add(line, 1/6 * self.TILE_SIZE, 1/6 * self.TILE_SIZE)

            if i == 1:
                line.rotate(90)
                line.move(0, 2/3 * self.TILE_SIZE)
        
        self.mode_display.add(self.x)

        self.flag = GPolygon()
        self.flag.add_vertex(self.TILE_SIZE/6, self.TILE_SIZE/6)
        self.flag.add_edge(2/3 * self.TILE_SIZE, 1/3 * self.TILE_SIZE)
        self.flag.add_edge(-2/3 * self.TILE_SIZE, 1/3 * self.TILE_SIZE)
        self.flag.set_filled(True)
        self.flag.set_fill_color('red')

        self.gw.add(self.mode_display, self.MARGIN, self.MARGIN)

        #remaining mines display
        self.remaining_mines = GLabel(str(self.mines - self.flag_num))
        self.remaining_mines.set_font(f" {self.FONT_SIZE}px helvetica")
        self.gw.add(self.remaining_mines, self.gw.get_width() - self.MARGIN - self.remaining_mines.get_width(), self.HEADER / 2 + self.remaining_mines.get_ascent() / 2)

        
        #timer_label
        self.timer_label = GLabel(str(round(self.current_time, 2)))
        self.timer_label.set_font(f" {self.FONT_SIZE}px helvetica")
        self.gw.add(self.timer_label, self.gw.get_width() / 2 - self.timer_label.get_width() / 2, self.HEADER / 2 + self.timer_label.get_ascent() / 2)


    def populate(self, exclude_nodes):
        
        #mines
        if self.mines > self.width * self.height:
            raise Exception(f'Fitting {self.mines} mines into a {self.width} by {self.height} board is impossible')

        for i in range(self.mines):
            node = self.linked_array.get_node(randint(0, self.width - 1), randint(0, self.height - 1))
            while node.mine or node in exclude_nodes:
                node = self.linked_array.get_node(randint(0, self.width - 1), randint(0, self.height - 1))
            node.mine = True

        
        #numbers
        def incr_neighbors(node):
            if node.mine:
                for neighbor in node.get_neighbors():
                    if neighbor != None:
                        if not neighbor.mine:
                            neighbor.neighbor_mines += 1

        self.linked_array.visit_nodes(incr_neighbors)

        self.correct_labels()


    def add_tiles(self):

        def add_tile(node):

            #background rectangle
            rect = GRect(self.TILE_SIZE, self.TILE_SIZE)
            rect.set_filled(True)
            rect.set_color('black')
            rect.set_fill_color('lightgray')
            node.tile.add(rect)
            

            # adding labels for mine / neighbor mine num
            node.label = GLabel('')
            node.label.set_font(f" {self.FONT_SIZE}px helvetica")
            node.tile.add(node.label)

            #covers
            node.cover = GRect(self.TILE_SIZE, self.TILE_SIZE)
            node.cover.set_filled(True)
            node.cover.set_fill_color('gray')
            node.cover.set_color('black')
            node.tile.add(node.cover)

            #flags
            node.flag = GPolygon()
            node.flag.add_vertex(self.TILE_SIZE/6, self.TILE_SIZE/6)
            node.flag.add_edge(2/3 * self.TILE_SIZE, 1/3 * self.TILE_SIZE)
            node.flag.add_edge(-2/3 * self.TILE_SIZE, 1/3 * self.TILE_SIZE)
            node.flag.set_filled(True)
            node.flag.set_fill_color('red')
 
        
        self.linked_array.visit_nodes(add_tile)
    

    def correct_labels(self):

        def correct_label(node):
            if node.mine:
                node.label.set_label('M')

            elif node.neighbor_mines > 0:
                node.label.set_label(str(node.neighbor_mines)) 
                node.label.set_color(self.LABEL_COLORS[node.neighbor_mines])

            label_x = self.TILE_SIZE / 2 - node.label.get_width() / 2
            label_y = self.TILE_SIZE / 2 - node.label.get_ascent() / 2 + node.label.get_ascent()
            node.label.move(label_x, label_y)

        self.linked_array.visit_nodes(correct_label)

    
    def see_tiles(self):

        def row_to_text(cur_node):
            txt = ''
            while cur_node is not None:
                if cur_node.mine:
                    txt += 'm '
                else:
                    txt += str(cur_node.neighbor_mines) + ' '
                
                cur_node = cur_node.get_right()
            return txt

        cur_node = self.linked_array.top_left
        out = '\n'
        while cur_node is not None:
            out += row_to_text(cur_node) + '\n'
            cur_node = cur_node.get_bottom()

        print(out)



if __name__ == '__main__':
    inst = Minesweeper(20, 16, 40)
