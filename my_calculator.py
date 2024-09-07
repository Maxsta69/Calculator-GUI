import tkinter as tk

class Calculator:
    def __init__(self, main_font=("Arial", 40, "bold"), sub_font=("Arial", 16),
                 num_font=("Arial", 24, "bold"), general_font=("Arial", 20),
                 background="#1C1C1C", button_color="#4CAF50", highlight_color="#F39C12",
                 screen_color="#333333", text_color="#F5F5F5", operator_color="#E74C3C"):
        # Store customization parameters
        self.main_font = main_font
        self.sub_font = sub_font
        self.num_font = num_font
        self.general_font = general_font
        self.background = background
        self.button_color = button_color
        self.highlight_color = highlight_color
        self.screen_color = screen_color
        self.text_color = text_color
        self.operator_color = operator_color

        # Initialize the main window
        self.root = tk.Tk()
        self.root.geometry("375x667")
        self.root.resizable(False, False)
        self.root.title("Max Bui's Calculator")

        # Store expressions
        self.full_expression = ""
        self.current_input = ""
        self.screen_frame = self.setup_screen_frame()
        self.full_label, self.input_label = self.setup_screen_labels()

        # Define number positions on grid
        self.numbers = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.ops = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.button_frame = self.create_button_area()
        self.configure_button_grid()

        # Set up buttons and key bindings
        self.add_number_buttons()
        self.add_operation_buttons()
        self.add_functional_buttons()
        self.bind_key_inputs()

    def bind_key_inputs(self):
        # Link keyboard presses to calculator functions
        self.root.bind("<Return>", lambda event: self.calculate_result())
        self.root.bind("<=>", lambda event: self.calculate_result())
        for key in self.numbers:
            self.root.bind(str(key), lambda event, num=key: self.update_input(num))
        for key in self.ops:
            self.root.bind(key, lambda event, op=key: self.add_operation(op))

    def setup_screen_frame(self):
        # Create the frame for displaying input/output
        frame = tk.Frame(self.root, height=221, bg=self.screen_color)
        frame.pack(expand=True, fill="both")
        return frame

    def setup_screen_labels(self):
        # Create and configure labels to show expressions and results
        full_label = tk.Label(self.screen_frame, text=self.full_expression, anchor=tk.E, 
                              bg=self.screen_color, fg=self.text_color, padx=24, font=self.sub_font)
        full_label.pack(expand=True, fill="both")

        input_label = tk.Label(self.screen_frame, text=self.current_input, anchor=tk.E, 
                               bg=self.screen_color, fg=self.text_color, padx=24, font=self.main_font)
        input_label.pack(expand=True, fill="both")

        return full_label, input_label

    def update_input(self, value):
        # Append new input value to the current expression
        self.current_input += str(value)
        self.refresh_input_display()

    def refresh_input_display(self):
        # Update the current input label with a slice to limit the number of characters shown
        self.input_label.config(text=self.current_input[:11])

    def refresh_full_expression_display(self):
        # Update the full expression label with correct symbols for operations
        expression = self.full_expression
        for op, symbol in self.ops.items():
            expression = expression.replace(op, f' {symbol} ')
        self.full_label.config(text=expression)

    def create_button_area(self):
        # Create the main button area for the calculator
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")
        return frame

    def configure_button_grid(self):
        # Configure the button grid layout for even distribution
        self.button_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)

    def add_number_buttons(self):
        # Create buttons for digits and position them on the grid
        for num, position in self.numbers.items():
            button = tk.Button(self.button_frame, text=str(num), bg=self.button_color, 
                               fg=self.text_color, font=self.num_font, borderwidth=0, 
                               command=lambda x=num: self.update_input(x))
            button.grid(row=position[0], column=position[1], sticky=tk.NSEW)

    def add_operation(self, operator):
        # Add an operator to the current expression
        self.current_input += operator
        self.full_expression += self.current_input
        self.current_input = ""
        self.refresh_full_expression_display()
        self.refresh_input_display()

    def add_operation_buttons(self):
        # Create buttons for operations and position them
        i = 0
        for operator, symbol in self.ops.items():
            button = tk.Button(self.button_frame, text=symbol, bg=self.operator_color, 
                               fg=self.text_color, font=self.general_font, borderwidth=0, 
                               command=lambda op=operator: self.add_operation(op))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def reset(self):
        # Clear both the full and current expressions
        self.current_input = ""
        self.full_expression = ""
        self.refresh_input_display()
        self.refresh_full_expression_display()

    def calculate_result(self):
        # Perform calculation based on the full expression
        self.full_expression += self.current_input
        self.refresh_full_expression_display()
        try:
            self.current_input = str(eval(self.full_expression))
            self.full_expression = ""
        except Exception:
            self.current_input = "ERROR"
        finally:
            self.refresh_input_display()

    def add_functional_buttons(self):
        # Add buttons for clear, equals, square, and square root
        self.add_clear_button()
        self.add_equals_button()
        self.add_square_button()
        self.add_sqrt_button()

    def add_clear_button(self):
        button = tk.Button(self.button_frame, text="C", bg=self.operator_color, 
                           fg=self.text_color, font=self.general_font, borderwidth=0, 
                           command=self.reset)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square_value(self):
        # Square the current input
        self.current_input = str(eval(f"{self.current_input}**2"))
        self.refresh_input_display()

    def add_square_button(self):
        button = tk.Button(self.button_frame, text="x²", bg=self.operator_color, 
                           fg=self.text_color, font=self.general_font, borderwidth=0, 
                           command=self.square_value)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def square_root_value(self):
        # Compute the square root of the current input
        self.current_input = str(eval(f"{self.current_input}**0.5"))
        self.refresh_input_display()

    def add_sqrt_button(self):
        button = tk.Button(self.button_frame, text="√x", bg=self.operator_color, 
                           fg=self.text_color, font=self.general_font, borderwidth=0, 
                           command=self.square_root_value)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def add_equals_button(self):
        button = tk.Button(self.button_frame, text="=", bg=self.highlight_color, 
                           fg=self.text_color, font=self.general_font, borderwidth=0, 
                           command=self.calculate_result)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def run(self):
        # Start the main loop of the Tkinter window
        self.root.mainloop()

# Example usage with a dark and colorful theme
if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
