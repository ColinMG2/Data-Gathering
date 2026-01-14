import matplotlib.pyplot as plt
import os
import cv2 as cv

def select_axes_and_calibrate(image_path):
    # Open the image
    img = cv.imread(image_path)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    fig, ax = plt.subplots()
    ax.imshow(img_rgb)
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

def extract_line_data(image_path):
    img = cv.imread(image_path)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Threshold the image to get binary image
    _, binary = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    # Find contours in the binary image
    contours, _ = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Extract x, y coordinates of the line
    line_points = []
    for contour in contours:
        for point in contour:
            line_points.append(point[0])

    # Sort the points based on x-coordinate
    line_points = sorted(line_points, key=lambda x: x[0])

    return line_points

# Input the absolute path of the image you want to analyze
image_path = input("Enter the path of the image: ")
(x_pixel_start, x_scale, x_value_start), (y_pixel_start, y_scale, y_value_start) = select_axes_and_calibrate(image_path)
line_points = extract_line_data(image_path)

# Convert pixel coordinates to actual values
x_points = [(point[0] - x_pixel_start) * x_scale + x_value_start for point in line_points]
y_points = [(point[1] - y_pixel_start) * y_scale + y_value_start for point in line_points]

print(f"Extracted x points: {x_points}")
print(f"Extracted y points: {y_points}")

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