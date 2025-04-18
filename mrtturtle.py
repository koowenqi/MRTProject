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

def generate_coords(route, start_x=-300, y=0, spacing=120):
    coords = {}
    for i, station in enumerate(route):
        coords[station] = (start_x + i * spacing, y)
    return coords

def generate_coords_with_transfers(path, linelist, start_x=-300, start_y=0, spacing=120, scale_factor=0.5):
    coords = {}
    x, y = start_x, start_y
    direction = 'vertical'

    for i in range(len(path)):
        coords[path[i]] = (x * scale_factor, y * scale_factor)

        # Decide if direction should switch after placing current station
        if i < len(path) - 1:
            if linelist[i] != linelist[i - 1] if i > 0 else False:
                direction = 'vertical' if direction == 'horizontal' else 'horizontal'
            if direction == 'horizontal':
                x += spacing
            else:
                y -= spacing
    return coords

def top_left_align_coords(coords, screen_width=1000, screen_height=700, right_panel_width=350, padding=50):
    xs = [x for x, y in coords.values()]
    ys = [y for x, y in coords.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    drawing_width = max_x - min_x
    drawing_height = max_y - min_y

    map_area_width = screen_width - right_panel_width - padding * 2
    map_area_height = screen_height - padding * 2

    # Calculate scale so it fits
    scale_x = map_area_width / drawing_width if drawing_width else 1
    scale_y = map_area_height / drawing_height if drawing_height else 1
    scale = min(scale_x, scale_y, 1)

    # Apply scaling
    scaled_coords = {
        station: ((x - min_x) * scale, (y - max_y) * scale)
        for station, (x, y) in coords.items()
    }

    # Top-left corner of the map area (leave padding from left/top)
    offset_x = -screen_width // 2 + padding
    offset_y = screen_height // 2 - padding

    # Final position: move into map area
    final_coords = {
        station: (x + offset_x, y + offset_y)
        for station, (x, y) in scaled_coords.items()
    }

    return final_coords

def draw_grey_panel(width=350, screen_width=1000, screen_height=700):
    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    panel_left_x = 350  # Keep it where you had it originally
    panel_top_y = 350

    pen.goto(panel_left_x, panel_top_y)
    pen.fillcolor("#D3D3D3")
    pen.begin_fill()
    pen.setheading(0)
    for _ in range(2):
        pen.forward(width)
        pen.right(90)
        pen.forward(screen_height)
        pen.right(90)
    pen.end_fill()

    return {
        "x": panel_left_x + 20,         # Left margin inside box
        "y": panel_top_y - 30,          # Top margin inside box
        "bottom_y": panel_top_y - 700 + 30,  # Bottom margin inside box
        "max_lines": 35
    }

panel_info = draw_grey_panel()

def draw_bestroute(path, linelist):
    screen = T.Screen()
    screen.clear()  # Clears previous drawings (for repeated use)
    screen.title("MRT Project")
    screen.setup(width=1000, height=700)

    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    title_footer()
    draw_grey_panel()

    coords = generate_coords_with_transfers(path, linelist, spacing=80, scale_factor=0.6)
    coords = top_left_align_coords(coords) # Center the entire route drawing
    for i in range(len(path) - 1):
        start = coords[path[i]]
        end = coords[path[i + 1]]
        # Set line color based on current segment
        pen.color(get_line_color(linelist[i]))
        if i == 0:
            pen.penup()
            pen.goto(start)
            pen.dot(1, "red") #This will get overshadowed by the other dot
        pen.pensize(6)
        pen.penup()
        pen.goto(start)
        pen.pendown()
        pen.goto(end)

    count = 0
    # Draw stations
    for i in range(len(path)):
        x, y = coords[path[i]]
        pen.penup()
        pen.goto(x, y)

        # If interchange (line changes from previous or next)
        station = path[i]
        lines_for_station = [linelist[j] for j in range(len(path)) if path[j] == station]
        is_transfer = len(set(lines_for_station)) > 1

        if is_transfer:
            # Outer dot
            pen.dot(18, "white")
            # Inner colored dot
            pen.dot(12, get_line_color(linelist[i]))
            
        else:
            pen.dot(10, get_line_color(linelist[i]))

        pen.color(get_line_color(linelist[i]))

        # Determine direction between current and next station
        if i < len(path) - 1:
            dx = coords[path[i+1]][0] - x
            dy = coords[path[i+1]][1] - y
        else:
            dx = 0
            dy = 0

        label_offset_x = 0
        label_offset_y = 0

        if abs(dx) > abs(dy):
            # Only for horizontal: alternate up/down
            label_offset_y = 12 if i % 2 == 0 else -20
        else:
            label_offset_x = 12
            label_offset_y = -5

        pen.goto(x + label_offset_x, y + label_offset_y)
        pen.write(station, font=("Arial", 8, "normal"))

def write_wrapped(pen, text, start_x, start_y, line_height=20, max_width=310, font=("Arial", 10, "normal"), bottom_limit=-320):
    words = text.split()
    line = ""
    current_y = start_y

    for word in words:
        test_line = f"{line} {word}".strip()
        estimated_width = len(test_line) * 6  # Approx width estimate (adjust if needed)

        if estimated_width > max_width:
            pen.penup()
            pen.goto(start_x, current_y)
            pen.write(line, font=font)
            current_y -= line_height
            if current_y < bottom_limit:
                break
            line = word
        else:
            line = test_line

    if current_y >= bottom_limit:
        pen.penup()
        pen.goto(start_x, current_y)
        pen.write(line, font=font)

def write_route_info(path, linelist, startstation, endstation, time, distance):
    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)

    x = panel_info["x"]
    y = panel_info["y"]
    bottom_limit = panel_info["bottom_y"]
    line_height = 20

    # Heading
    heading = f"{startstation} → {endstation}"
    pen.penup()
    pen.goto(x, y)
    pen.color("black")
    pen.write(heading, font=("Arial", 12, "bold"))
    y -= line_height * 2

    prev_line = linelist[0]

    for i in range(1, len(path)):
        current_line = linelist[i - 1]

        if linelist[i] != prev_line:
            transfer_station = path[i]
            pre_text = "Transfer to"
            line_name = f"{linelist[i]} Line"
            post_text = f" at {transfer_station}"

            if y > bottom_limit:
                pen.penup()
                pen.goto(x, y)

                # Write "Transfer to"
                pen.color("black")
                pen.write(pre_text, font=("Arial", 10, "normal"))

                # Move to end of previous text
                pen.setx(pen.xcor() + len(pre_text) * 6)  # Approx width per char

                # Write colored line name
                line_color = get_line_color(linelist[i])
                pen.color(line_color)
                pen.write(line_name, font=("Arial", 10, "normal"))

                # Move to end of line name
                pen.setx(pen.xcor() + len(line_name) * 6)

                # Write rest
                pen.color("black")
                pen.write(post_text, font=("Arial", 10, "normal"))

                y -= line_height

            prev_line = linelist[i]

    if time and distance:
        if y > bottom_limit:
            y -= line_height
            pen.penup()
            pen.goto(x, y)
            pen.color("black")
            pen.write(f"Total distance: {distance:.2f} km", font=("Arial", 10, "italic"))
            y -= line_height

        if y > bottom_limit:
            pen.penup()
            pen.goto(x, y)
            pen.color("black")
            if time < 60:
                pen.write(f"Estimated travel time: {time:.1f} minutes", font=("Arial", 10, "italic"))
            else:
                hours = int(time // 60)
                minutes = int(time % 60)
                pen.write(f"Estimated travel time: {hours} hour(s) and {minutes} minute(s)", font=("Arial", 10, "italic"))

def draw_limited_route(path, linelist, reachable_index):
    screen = T.Screen()
    screen.clear()
    screen.title("Train Journey Availability")
    screen.setup(width=1000, height=700)

    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()

    title_footer()
    draw_grey_panel()

    coords = generate_coords_with_transfers(path, linelist, spacing=80, scale_factor=0.6)
    coords = top_left_align_coords(coords)

    # Draw lines up to the reachable index
    for i in range(reachable_index):
        start = coords[path[i]]
        end = coords[path[i + 1]]
        pen.color(get_line_color(linelist[i]))
        pen.pensize(6)
        if i == 0:
            pen.penup()
            pen.goto(start)
            pen.dot(1, "red") #This will get overshadowed by the other dot
        pen.penup()
        pen.goto(start)
        pen.pendown()
        pen.goto(end)

    # Draw stations
    for i in range(reachable_index + 1):
        x, y = coords[path[i]]
        pen.penup()
        pen.goto(x, y)
        line_color = get_line_color(linelist[i])

        # Check for transfer station
        station = path[i]
        lines_for_station = [linelist[j] for j in range(len(path)) if path[j] == station]
        is_transfer = len(set(lines_for_station)) > 1

        if is_transfer:
            pen.dot(18, "white")
            pen.dot(12, line_color)
        else:
            pen.dot(10, line_color)

        # Name label (same up-down logic for horizontal)
        if i < len(path) - 1:
            dx = coords[path[i+1]][0] - x
            dy = coords[path[i+1]][1] - y
        else:
            dx = 0
            dy = 0

        label_offset_x = 0
        label_offset_y = 0

        if abs(dx) > abs(dy):
            # Only for horizontal: alternate up/down
            label_offset_y = 12 if i % 2 == 0 else -20
        else:
            label_offset_x = 12
            label_offset_y = -5

        pen.goto(x + label_offset_x, y + label_offset_y)
        pen.color(line_color)
        pen.write(station, font=("Arial", 8, "normal"))

def write_time_check_info(startstation, endstation, projected_arrival_time, lasttrain_dt, cumulative_time, latest_departure, ontime):
    pen = T.Turtle()
    pen.hideturtle()
    pen.speed(0)

    x = panel_info["x"]
    y = panel_info["y"]
    bottom_y = panel_info["bottom_y"]
    line_height = 20

    arrival_str = projected_arrival_time.strftime("%H:%M")
    lasttrain_str = lasttrain_dt.strftime("%H:%M")

    travel_hours = int(cumulative_time // 60)
    travel_minutes = int(cumulative_time % 60)
    travel_msg = (
        f"{travel_hours} hour(s) and {travel_minutes} minute(s)"
        if travel_hours > 0 else
        f"{travel_minutes} minute(s)"
    )

    # Heading
    heading = f"{startstation} → {endstation}"
    pen.penup()
    pen.goto(x, y)
    pen.color("black")
    pen.write(heading, font=("Arial", 12, "bold"))
    y -= line_height * 2

    if ontime:
        info = (
            f"You will reach {endstation} at around {arrival_str},\n"
            f"which is within operating hours.\n"
            f"Total travel time: {travel_msg}"
        )
    else:
        delay = (projected_arrival_time - lasttrain_dt).seconds // 60
        delay_hours = int(delay // 60)
        delay_minutes = int(delay % 60)
        delay_msg = (
            f"{delay_hours} hour(s) and {delay_minutes} minute(s)"
            if delay_hours > 0 else
            f"{delay_minutes} minute(s)"
        )
        latest_departure_str = latest_departure.strftime("%H:%M")

        info = (
            "The journey cannot be completed in time.\n"
            f"You will reach {endstation} at {arrival_str},\n"
            f"but the last train departs at {lasttrain_str}.\n"
            f"Total travel time needed: {travel_msg}\n"
            f"You are {delay_msg} minutes late.\n"
            f"You must depart from {startstation} before {latest_departure_str}"
        )

    write_wrapped(pen, info, x, y, max_width=300, line_height=line_height)