# circuit python
import time
import board
import digitalio
import busio  # Import busio module
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode


# Display Init
i2c = busio.I2C(board.GP1, board.GP0)
address = 0x27
lcd = LCD(I2CPCF8574Interface(i2c, address), num_rows=2, num_cols=16)

# KEYPAD Init
# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

keypad_columns = [board.GP15, board.GP14, board.GP13, board.GP12]
keypad_rows = [board.GP16, board.GP17, board.GP18, board.GP19]

# Create two empty lists to set up pins ( Rows output and columns input )
col_pins = []
row_pins = []

# Loop to assign GPIO pins and setup input and outputs
for row_pin in keypad_rows:
    pin = digitalio.DigitalInOut(row_pin)
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = True
    row_pins.append(pin)

for col_pin in keypad_columns:
    pin = digitalio.DigitalInOut(col_pin)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.DOWN
    col_pins.append(pin)


############################## Scan keys ####################

print("Please enter a key from the keypad")
calc = ""

# Function to calculate expression
def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def display_calc(first_row):
    print(first_row)
    lcd.clear()
    lcd.print(first_row)

def display_ans(second_row):
    lcd.set_cursor_pos(1, 0)
    lcd.print(f"Ans: {second_row}")

def handle_number_input(key_pressed):
    global calc
    if key_pressed.isdigit():  # Check if the key pressed is a digit
        calc += key_pressed
        display_calc(calc)

def scankeys():
    global calc
    for row in range(0,4):
        row_pins[row].value = True
        for col in range(0,4):
            if col_pins[col].value:
                key_pressed = matrix_keys[row][col]
                print("You have pressed:", matrix_keys[row][col])
                #*=================================
                #* here you can put your key logics
                
                #! Operations
                if key_pressed == "A":
                    calc += "+"
                    display_calc(calc)
                if key_pressed == "B":
                    calc += "-"
                    display_calc(calc)

                if key_pressed == "C":
                    calc = ""
                    lcd.clear()
                if key_pressed == "D":
                    ans = str(calculate(calc))
                    print(ans)
                    display_ans( ans)

                #! Numbers
                if key_pressed in "0123456789":
                    handle_number_input(key_pressed)
                    
                # if key_pressed  == "1":
                #     calc += "1"
                #     display_calc(calc)
                # if key_pressed == "2":
                #     calc += "2"
                #     display_calc(calc)
                # if key_pressed == "3":
                #     calc += "3"
                #     display_calc(calc)
                # if key_pressed  == "4":
                #     calc += "4"
                #     display_calc(calc)
                # if key_pressed == "5":
                #     calc += "5"
                #     display_calc(calc)
                # if key_pressed == "6":
                #     calc += "6"
                #     display_calc(calc)
                # if key_pressed  == "7":
                #     calc += "7"
                #     display_calc(calc)
                # if key_pressed == "8":
                #     calc += "8"
                #     display_calc(calc)
                # if key_pressed == "9":
                #     calc += "9"
                #     display_calc(calc)
                # if key_pressed == "0":
                #     calc += "0"
                #     display_calc(calc)
                #*=================================

                time.sleep(0.3)
        row_pins[row].value = False

while True:
    scankeys()
