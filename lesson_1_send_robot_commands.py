
from arduino_car_controller import ArduinoCarController

if __name__ == "__main__":
    car_controller = ArduinoCarController()
    # Move forward for 2 seconds at speed 150
    car_controller.move_forward(2000, 150)
    # Turn left for 1 second at speed 100
    car_controller.turn_left(1000, 100)
    # Move backward for 2 seconds at speed 150
    car_controller.move_backward(2000, 150)
    print("Commands executed successfully.")
