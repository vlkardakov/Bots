import math

def calculate_mean_wind_direction(wind_directions_degrees):
    wind_directions_radians = [math.radians(angle) for angle in wind_directions_degrees]
    sin_sum = sum(math.sin(angle) for angle in wind_directions_radians)
    cos_sum = sum(math.cos(angle) for angle in wind_directions_radians)

    mean_direction_radians = math.atan2(sin_sum, cos_sum)
    mean_direction_degrees = math.degrees(mean_direction_radians)

    # Ensure the result is in the range [0, 360)
    mean_direction_degrees = (mean_direction_degrees + 360) % 360

    return mean_direction_degrees


if __name__ == "__main__":
    with open("in.txt", "r") as input_file:
        wind_directions_degrees = []
        for line in input_file:
            angle = float(line.strip())
            wind_directions_degrees.append(angle)

    mean_wind_direction = calculate_mean_wind_direction(wind_directions_degrees)

    with open("out.txt", "w") as output_file:
        output_file.write(f"{mean_wind_direction:.6f}")
