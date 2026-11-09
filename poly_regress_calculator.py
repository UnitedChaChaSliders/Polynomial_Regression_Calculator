from tkinter import *
from matplotlib.figure import Figure
import numpy as np
import math as m
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# REGRESSION FUNCTION
def regress(data_input, deg_input):
    data = data_input.strip().replace(" ", "").replace("(","").replace(")","")
    data = data.split(",")
    try:
        data = [float(x) for x in data]
    except ValueError:
        data_error()

    try:
        degree = int(deg_input)
    except ValueError:
        degree = 1

    # Create vector y of y-values and matrix X of x-values.
    y_values = np.array(data[1::2])
    X = np.empty((0, degree+1))

    for index, coordinate in enumerate(data):
        if index % 2 == 0:
            x_row = np.array([])
            for n in range(degree+1):
                x_row = np.append(x_row, coordinate**(degree-n))
            X = np.vstack([X, x_row])
        else:
            pass

    # Apply the formula ((X^T*X)^(-1))*X^T*y to get the polynomial of best fit.
    try: 
        result = (np.matmul(X.T, X))
        result = np.linalg.pinv(result)
        result = result @ X.T
        result = result @ y_values
    except:
        data_error()

    # Resulting equation
    equation = ""
    for index, value in enumerate(result):
        if m.isclose(value, 0, abs_tol=1e-9):
            pass
        elif value > 0:
            equation = equation + f" + {value:.4f}x^{degree-index}"
        else:
            equation = equation + f" - {abs(value):.4f}x^{degree-int(index)}"

    equation = equation.replace("x^1","x").replace("x^0","")
    equation = equation[2:]

    # Plot the data and the polynomial of best fit.
    # Data points
    x_values = np.array(data[::2])
    
    # Polynomial of best fit
    def poly(var):
        f = 0
        for index, value in enumerate(result):
            f += value*var**(degree-index)
        return f

    # R^2 value
    tss = np.sum((y_values - np.mean(y_values))**2)
    rss = np.sum((y_values - poly(x_values))**2)
    rsq = 1 - (rss / tss) if tss != 0 else 0
    
    depvar = np.linspace(min(x_values) - 0.2*(max(x_values) - min(x_values)), max(x_values) + 0.2*(max(x_values) - min(x_values)), 200)
    y = poly(depvar)

    fig = Figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    x_values = np.array(data[::2])
    ax.scatter(x_values, y_values, color="#690d06")
    ax.plot(depvar, y, color='#e0482d')
    ax.set_title(equation, loc="left")
    ax.set_title(f"R^2 = {rsq:.4f}", loc="right")
    ax.legend()
    ax.grid(True)

    return fig

def data_error():
    error.config(text="Error: Invalid data format.")

def doit():
    for widget in window.winfo_children():
            if isinstance(widget, Canvas):
                widget.destroy()
    data_input = data_entry.get()
    deg_input = deg_entry.get()
    fig = regress(data_input, deg_input)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    error.config(text="")

def clear(): 
    for widget in window.winfo_children():
        if isinstance(widget, Canvas):
            widget.destroy()
    data_entry.delete(0, END)
    deg_entry.delete(0, END)
    error.config(text="")

# ACTUAL GUI BEGINS
window = Tk()
window.title("Polynomial Regression Calculator")
window.geometry("800x800")
window.configure(bg="white")

# TITLE AND SUBTITLE
title = Label(window, text="A Simple Regression Calculator.", 
                      font=("Bell MT", 30), 
                      fg="#690d06", 
                      bg="white")
title.pack(pady=10)

subtitle = Label(window, text="Find the polynomial of best fit for your data.", 
                         font=("Bell MT", 15, "bold"), 
                         fg="#690d06",
                         bg="white")
subtitle.pack()

# INPUT SECTION
l1 = Label(window, text="Enter your data as a list of coordinates:", 
                   font=("Bell MT", 12), 
                   fg="#690d06",
                   bg="white")
l1.pack(pady=(30,10))
data_entry = Entry(window, font=("Calibri", 12), 
                           bg="#e6e8eb")
data_entry.pack(pady=10)

l2 = Label(window, text="Enter the degree of the polynomial (defaults to 1):", 
                   font=("Bell MT", 12), 
                   fg="#690d06",
                   bg="white")
l2.pack(pady=10)
deg_entry = Entry(window, font=("Calibri", 12),
                          bg="#e6e8eb")
deg_entry.pack(pady=10)

# RUN BUTTON
run = Button(window, text="Run", font=("Bell MT", 14), command=doit)
run.config(bg="#e0482d")
run.pack(pady=20)

# RESET BUTTON
reset = Button(window, text="Reset", font=("Bell MT", 14), command=clear)
reset.config(bg="#e0482d")
reset.pack(pady=20)

# ERROR SECTION
error = Label(window, text="", font=("Bell MT", 12, "bold"), fg="red", bg="white")
error.pack(pady=10)

window.mainloop()