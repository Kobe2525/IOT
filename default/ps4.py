from pyPS4Controller.controller import Controller
import os
import _thread
import time

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        print("Controller initialized.")
        
        self.XButton = 0
        self.TButton = 0
        self.CButton = 0
        self.SButton = 0
        self.L1Button = 0
        self.L2Button = 0
        self.R1Button = 0
        self.R2Button = 0
        self.UpArrow = 0
        self.DownArrow = 0
        self.LeftArrow = 0
        self.RightArrow = 0
        self.L3X = 0
        self.L3Y = 0
        self.R3X = 0
        self.R3Y = 0
        self.L3Button = 0
        self.R3Button = 0
        self.OptionsButton = 0
        self.ShareButton = 0
        self.PSButton = 0

    def on_x_press(self):
        self.XButton = 1
    
    def on_x_release(self):
        self.XButton = 0
    
    def on_triangle_press(self):
        self.TButton = 1
    
    def on_triangle_release(self):
        self.TButton = 0
    
    def on_circle_press(self):
        self.CButton = 1
    
    def on_circle_release(self):
        self.CButton = 0
    
    def on_square_press(self):
        self.SButton = 1
    
    def on_square_release(self):
        self.SButton = 0
    
    def on_L1_press(self):
        self.L1Button = 1
    
    def on_L1_release(self):
        self.L1Button = 0
    
    def on_L2_press(self, value):
        self.L2Button = value
    
    def on_L2_release(self):
        self.L2Button = 0
    
    def on_R1_press(self):
        self.R1Button = 1
    
    def on_R1_release(self):
        self.R1Button = 0
    
    def on_R2_press(self, value):
        self.R2Button = value
    
    def on_R2_release(self):
        self.R2Button = 0
    
    def on_up_arrow_press(self):
        self.UpArrow = 1
    
    def on_up_down_arrow_release(self):
        self.UpArrow = 0
        self.DownArrow = 0
    
    def on_down_arrow_press(self):
        self.DownArrow = 1
    
    def on_left_arrow_press(self):
        self.LeftArrow = 1
    
    def on_left_right_arrow_release(self):
        self.LeftArrow = 0
        self.RightArrow = 0
    
    def on_right_arrow_press(self):
        self.RightArrow = 1
    
    def on_L3_press(self):
        self.L3Button = 1
    
    def on_L3_release(self):
        self.L3Button = 0
    
    def on_R3_press(self):
        self.R3Button = 1
    
    def on_R3_release(self):
        self.R3Button = 0
    
    def on_options_press(self):
        self.OptionsButton = 1
    
    def on_options_release(self):
        self.OptionsButton = 0
    
    def on_share_press(self):
        self.ShareButton = 1
    
    def on_share_release(self):
        self.ShareButton = 0
    
    def on_playstation_button_press(self):
        self.PSButton = 1
    
    def on_playstation_button_release(self):
        self.PSButton = 0
    
    def on_L3_up(self, value):
        ValueB = 100/32767*value
        self.L3Y = -ValueB
    
    def on_L3_down(self, value):
        ValueB = 100/32767*value
        self.L3Y = -ValueB
    
    def on_L3_left(self, value):
        ValueB = 100/32767*value
        self.L3X = ValueB
    
    def on_L3_right(self, value):
        ValueB = 100/32767*value
        self.L3X = ValueB
    
    def on_L3_y_at_rest(self):
        self.L3Y = 0
    
    def on_L3_x_at_rest(self):
        self.L3X = 0
    
    def on_R3_up(self, value):
        ValueB = 100/32767*value
        self.R3Y = -ValueB
    
    def on_R3_down(self, value):
        ValueB = 100/32767*value
        self.R3Y = -ValueB
    
    def on_R3_left(self, value):
        ValueB = 100/32767*value
        self.R3X = ValueB
    
    def on_R3_right(self, value):
        ValueB = 100/32767*value
        self.R3X = ValueB
    
    def on_R3_y_at_rest(self):
        self.R3Y = 0
    
    def on_R3_x_at_rest(self):
        self.R3X = 0
    

def ControllerDef():
    controller.listen(timeout=60)



def Return():
    values=[controller.XButton , controller.TButton , controller.CButton , controller.SButton , 
    controller.L1Button , controller.L2Button , controller.R1Button , controller.R2Button , 
    controller.UpArrow ,controller.DownArrow , controller.LeftArrow , controller.RightArrow , 
    controller.L3Button , controller.R3Button , 
    controller.OptionsButton , controller.ShareButton , controller.PSButton , 
    controller.L3X , controller.L3Y , controller.R3X , controller.R3Y]
    return values

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
_thread.start_new_thread(ControllerDef,())

