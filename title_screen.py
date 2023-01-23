from Minesweeper import Minesweeper
from pgl import GWindow, GRect, GLabel, GCompound, GImage
from math import floor

def main():
    gw = GWindow(500, 400)

    #background image
    image = GImage('background.png')
    image.scale(.5)
    gw.add(image, -20, -20)

    #background rect
    back = GRect(gw.get_width() - 100, gw.get_height() - 50 + 3)
    back.set_filled(True)
    back.set_fill_color('gray')
    back.set_line_width(2)
    gw.add(back, 50, -3)

    #title
    title = GLabel('Welcome to Minesweeper!')
    title.set_font("bold 30px helvetica")
    gw.add(title, gw.get_width() / 2 - title.get_width() / 2, 5 + title.get_ascent())

    #subtitle
    subtitle = GLabel('Choose your difficulty:')
    subtitle.set_font('italic 20px helvetica')
    gw.add(subtitle, (gw.get_width() - subtitle.get_width()) / 2, 50 + subtitle.get_ascent())

    #buttons
    beg_button = make_button('Beginner', 'green')
    gw.add(beg_button, (gw.get_width() - beg_button.get_width()) / 2, 100)
    int_button = make_button('Intermediate', 'yellow')
    gw.add(int_button, (gw.get_width() - int_button.get_width()) / 2, 175)
    exp_button = make_button('Expert', 'red')
    gw.add(exp_button, (gw.get_width() - exp_button.get_width()) / 2, 250)



    def click_action(e):
        x, y = floor(e.get_x()), floor(e.get_y())

        bbox = beg_button.get_bounds()
        ibox = int_button.get_bounds()
        ebox = exp_button.get_bounds()

        if bbox.get_x() < x < bbox.get_x() + bbox.get_width() and bbox.get_y() < y < bbox.get_y() + bbox.get_height():
            Minesweeper(9, 9, 10)
            return

        elif ibox.get_x() < x < ibox.get_x() + ibox.get_width() and ibox.get_y() < y < ibox.get_y() + ibox.get_height():
            Minesweeper(16, 16, 40)
            return

        elif ebox.get_x() < x < ebox.get_x() + ebox.get_width() and ebox.get_y() < y < ebox.get_y() + ebox.get_height():
            Minesweeper(30, 16, 99)
            return

    
    def move_action(e):

        def update(activate, deactivate):
            if activate != None:
                activate.set_line_width(5)

            for target in deactivate:
                target.set_line_width(1)


        x, y = floor(e.get_x()), floor(e.get_y())

        bbox = beg_button.get_bounds()
        ibox = int_button.get_bounds()
        ebox = exp_button.get_bounds()

        if bbox.get_x() < x < bbox.get_x() + bbox.get_width() and bbox.get_y() < y < bbox.get_y() + bbox.get_height():
            update(beg_button.get_element(0), [int_button.get_element(0), exp_button.get_element(0)])

        elif ibox.get_x() < x < ibox.get_x() + ibox.get_width() and ibox.get_y() < y < ibox.get_y() + ibox.get_height():
            update(int_button.get_element(0), [beg_button.get_element(0), exp_button.get_element(0)])
            
        elif ebox.get_x() < x < ebox.get_x() + ebox.get_width() and ebox.get_y() < y < ebox.get_y() + ebox.get_height():
            update(exp_button.get_element(0), [int_button.get_element(0), beg_button.get_element(0)])
        
        else:
            update(None, [beg_button.get_element(0), int_button.get_element(0), exp_button.get_element(0)])

    
    gw.add_event_listener('click', click_action)
    gw.add_event_listener('mousemove', move_action)

        

def make_button(label, color) -> GCompound():
    # button
    button = GCompound()

    rect = GRect(200, 50)
    rect.set_filled(True)
    rect.set_color(color)
    button.add(rect, 0, 0)

    label = GLabel(label)
    label.set_font(' 20px helvetica')
    button.add(label, (button.get_width() - label.get_width()) / 2, button.get_height() / 2 + label.get_ascent() / 2)

    return button


if __name__ == '__main__':
    main()
