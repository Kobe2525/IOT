from pyPS4Controller.controller import Controller

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        print("Controller initialized.")

    def on_x_press(self):
        print("X button pressed.")

    def on_x_release(self):
        print("X button released.")

    def on_triangle_press(self):
        print("Triangle button pressed.")

    def on_triangle_release(self):
        print("Triangle button released.")

    def on_circle_press(self):
        print("Circle button pressed.")

    def on_circle_release(self):
        print("Circle button released.")

    def on_square_press(self):
        print("Square button pressed.")

    def on_square_release(self):
        print("Square button released.")

    def on_L1_press(self):
        print("L1 button pressed.")

    def on_L1_release(self):
        print("L1 button released.")

    def on_L2_press(self, value):
        print(f"L2 button pressed with value {value}.")

    def on_L2_release(self):
        print("L2 button released.")

    def on_R1_press(self):
        print("R1 button pressed.")

    def on_R1_release(self):
        print("R1 button released.")

    def on_R2_press(self, value):
        print(f"R2 button pressed with value {value}.")

    def on_R2_release(self):
        print("R2 button released.")

    def on_up_arrow_press(self):
        print("Up arrow pressed.")

    def on_up_down_arrow_release(self):
        print("Up/Down arrow released.")

    def on_down_arrow_press(self):
        print("Down arrow pressed.")

    def on_left_arrow_press(self):
        print("Left arrow pressed.")

    def on_left_right_arrow_release(self):
        print("Left/Right arrow released.")

    def on_right_arrow_press(self):
        print("Right arrow pressed.")

    def on_L3_up(self, value):
        pass

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        pass

    def on_L3_right(self, value):
        pass

    def on_L3_y_at_rest(self):
        print("L3 Y axis is at rest.")

    def on_L3_x_at_rest(self):
        print("L3 X axis is at rest.")

    def on_L3_press(self):
        print("L3 button pressed.")

    def on_L3_release(self):
        print("L3 button released.")

    def on_R3_up(self, value):
        pass

    def on_R3_down(self, value):
        pass

    def on_R3_left(self, value):
        pass

    def on_R3_right(self, value):
        pass

    def on_R3_y_at_rest(self):
        print("R3 Y axis is at rest.")

    def on_R3_x_at_rest(self):
        print("R3 X axis is at rest.")

    def on_R3_press(self):
        print("R3 button pressed.")

    def on_R3_release(self):
        print("R3 button released.")

    def on_options_press(self):
        print("Options button pressed.")

    def on_options_release(self):
        print("Options button released.")

    def on_share_press(self):
        print("Share button pressed.")

    def on_share_release(self):
        print("Share button released.")

    def on_playstation_button_press(self):
        print("PlayStation button pressed.")

    def on_playstation_button_release(self):
        print("PlayStation button released.")

# Create the controller instance and start listening
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen(timeout=60)
