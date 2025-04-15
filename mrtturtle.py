import turtle as T

def title_footer():
    screen = T.Screen()
    screen.clear()  # Clears previous drawings (for repeated use)
    screen.title("MRT Project")
    screen.setup(width=1000, height=700)

    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    # Title at the top
    pen.goto(0, 300)
    pen.color("black")
    pen.write("MRT Project", align="center", font=("Arial", 24, "bold"))

    # Footer at the bottom
    pen.goto(0, -320)
    pen.color("gray")
    pen.write("DO NOT CLOSE THIS PAGE", align="center", font=("Arial", 10, "italic"))

def draw_mrt_line(line_name, station_list):
    screen = T.Screen()
    screen.clear()  # Clears previous drawings (for repeated use)
    screen.title("MRT Project")
    screen.setup(width=1000, height=700)

    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    title_footer()

    # Draw MRT line
    pen.goto(-260, 250)
    pen.setheading(0)
    pen.color(get_line_color(line_name))
    pen.pensize(10)
    x = 0
    pattern1 = True
    pattern2 = False
    pen.dot(20)
    for station in station_list:
        station = ' '.join(station)
        if pattern1:
            pen.dot(20)
            pen.penup()
            pen.forward(10)
            pen.left(90)
            pen.forward(15)
            pen.write(station, font=("Arial", 8, "normal"))
            pen.backward(15)
            pen.right(90)
            pen.backward(10)
            pen.pendown()
            x += 120
            if station_list[-1] == station.split(" ", 1):
                break
            if x % 600 != 0:
                pen.forward(120)
            if x % 600 == 0:
                pen.right(90)
                pen.forward(60)
                pen.right(90)
                pattern1 = False
                pattern2 = True
                continue
        if pattern2:
            pen.dot(20)
            pen.penup()
            pen.backward(10)
            pen.right(90)
            pen.forward(15)
            pen.write(station, font=("Arial", 8, "normal"))
            pen.backward(15)
            pen.left(90)
            pen.forward(10)
            pen.pendown()
            x += 120
            if station_list[-1] == station.split(" ", 1):
                break
            if x % 600 != 0:
                pen.forward(120)
            if x % 600 == 0:
                pen.left(90)
                pen.forward(60)
                pen.left(90)
                pattern2 = False
                pattern1 = True
                continue

def get_line_color(line_name):
    line_colors = {
        "North East": "#9900AA",
        "Circle": "#FFB300",
        "Downtown": "#005EC4",
        "East-West": "#009645",
        "North-South": "#D42E12",
        "Thomson-East Coast": "#8B6508"
    }
    return line_colors.get(line_name, "black")