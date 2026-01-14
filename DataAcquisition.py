import matplotlib.pyplot as plt
import os

def select_axes_and_calibrate(image_path):
    # Open the image
    img = plt.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    plt.title("Click on the start and end of the x-axis")

    # Get x-axis points
    x_axis_points = plt.ginput(2)
    x_pixel_start, x_pixel_end = x_axis_points[0][0], x_axis_points[1][0]

    plt.title("Enter the start and end values of the x-axis")
    x_value_start = float(input("Enter the start value of the x-axis: "))
    x_value_end = float(input("Enter the end value of the x-axis: "))

    plt.title("Click on the start and end of the y-axis")

    # Get y-axis points
    y_axis_points = plt.ginput(2)
    y_pixel_start, y_pixel_end = y_axis_points[0][1], y_axis_points[1][1]

    plt.title("Enter the start and end values of the y-axis (log scale)")
    y_value_start = float(input("Enter the start value of the y-axis: "))
    y_value_end = float(input("Enter the end value of the y-axis: "))

    # Calculate the scaling factors
    x_scale = (x_value_end - x_value_start) / (x_pixel_end - x_pixel_start)
    # y_scale = (np.log10(y_value_end) - np.log10(y_value_start)) / (y_pixel_end - y_pixel_start)
    # return (x_pixel_start, x_scale, x_value_start), (y_pixel_start, y_scale, np.log10(y_value_start))
    y_scale = (y_value_end - y_value_start) / (y_pixel_end - y_pixel_start)
    return (x_pixel_start, x_scale, x_value_start), (y_pixel_start, y_scale, y_value_start)

def select_data_points(image_path):
    # (x_pixel_start, x_scale, x_value_start), (y_pixel_start, y_scale, y_log_value_start) = select_axes_and_calibrate(image_path)
    (x_pixel_start, x_scale, x_value_start), (y_pixel_start, y_scale, y_value_start) = select_axes_and_calibrate(image_path)


    img = plt.imread(image_path)
    fig, ax = plt.subplots()
    ax.imshow(img)

    plt.title("Click to select data points, middle click to stop")

    # Select data points
    points = plt.ginput(n=-1, timeout=0)

    # Calibrate selected points
    x_points = [(point[0] - x_pixel_start) * x_scale + x_value_start for point in points]
    # y_points = [10 ** ((point[1] - y_pixel_start) * y_scale + y_log_value_start) for point in points]
    y_points = [(point[1] - y_pixel_start) * y_scale + y_value_start for point in points]


    plt.show()

    return x_points, y_points

# Input the absolute path of the image you want to analyze
image_path = input("Enter the path of the image: ")

x_points, y_points = select_data_points(image_path)

print(f"Calibrated x points:\n, {x_points}\n")
print(f"Calibrated y points:\n, {y_points}\n")

# generate .csv file with the same name as the image file
image_name = os.path.basename(image_path)
csv_filename = os.path.splitext(image_name)[0] + ".csv"
output_dir_name = "output_data_csv_files"
output_csv_path = os.path.join(output_dir_name, csv_filename)

with open(output_csv_path, "w") as f:
    f.write("x,y\n")  # optional header
    for x, y in zip(x_points, y_points):
        f.write(f"{x},{y}\n")

print(f"Data saved to {output_csv_path}")