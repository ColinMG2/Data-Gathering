import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import cv2 as cv

def select_axes_and_calibrate(image_path):
    # Open the image
    img = cv.imread(image_path)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    fig, ax = plt.subplots()
    ax.imshow(img_rgb)

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
    # Return pixel start/end so we can crop to plot area later
    return (x_pixel_start, x_pixel_end, x_scale, x_value_start), (y_pixel_start, y_pixel_end, y_scale, y_value_start)


def extract_line_data(image_path, x_pixel_start, x_pixel_end, y_pixel_start, y_pixel_end):
    img = cv.imread(image_path)

    # Define a region of interest slightly inside the axes to avoid
    # picking up the axis lines and labels.
    x_min = int(min(x_pixel_start, x_pixel_end))
    x_max = int(max(x_pixel_start, x_pixel_end))
    y_min = int(min(y_pixel_start, y_pixel_end))
    y_max = int(max(y_pixel_start, y_pixel_end))

    # Shrink inward by a couple of pixels to stay inside the plot box
    margin = 2
    x_min_roi = max(x_min + margin, 0)
    y_min_roi = max(y_min + margin, 0)
    x_max_roi = min(x_max - margin, img.shape[1])
    y_max_roi = min(y_max - margin, img.shape[0])

    roi_bgr = img[y_min_roi:y_max_roi, x_min_roi:x_max_roi]

    # --- Branch 1: try color-based extraction (for colored curves) ---
    roi_hsv = cv.cvtColor(roi_bgr, cv.COLOR_BGR2HSV)

    sat_thresh = 50  # 0-255; increase if you still see gray features
    val_min = 50
    val_max = 255
    lower = (0, sat_thresh, val_min)
    upper = (179, 255, val_max)
    color_mask = cv.inRange(roi_hsv, lower, upper)

    kernel = np.ones((3, 3), np.uint8)
    color_mask = cv.morphologyEx(color_mask, cv.MORPH_OPEN, kernel)

    contours_color, _ = cv.findContours(color_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    min_area_color = 10.0
    filtered_color = [c for c in contours_color if cv.contourArea(c) >= min_area_color]

    color_points = []
    for contour in filtered_color:
        for point in contour:
            px = point[0][0] + x_min_roi
            py = point[0][1] + y_min_roi
            color_points.append((px, py))

    # If we found enough colored points, use them; otherwise
    # fall back to a grayscale-based method for non-colored curves.
    min_points_for_color = 50
    if len(color_points) >= min_points_for_color:
        line_points = color_points
    else:
        # --- Branch 2: grayscale extraction (for black/gray curves) ---
        roi_gray = cv.cvtColor(roi_bgr, cv.COLOR_BGR2GRAY)
        # Invert threshold so dark line on light background becomes white
        _, binary = cv.threshold(roi_gray, 0, 255,
                                 cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

        contours_gray, _ = cv.findContours(binary, cv.RETR_TREE,
                                           cv.CHAIN_APPROX_SIMPLE)
        min_area_gray = 10.0
        filtered_gray = [c for c in contours_gray
                         if cv.contourArea(c) >= min_area_gray]

        line_points = []
        for contour in filtered_gray:
            for point in contour:
                px = point[0][0] + x_min_roi
                py = point[0][1] + y_min_roi
                line_points.append((px, py))

    # Sort the points based on x-coordinate
    line_points = sorted(line_points, key=lambda x: x[0])

    return line_points

# Input the absolute path of the image you want to analyze
image_path = input("Enter the path of the image: ")
(x_pixel_start, x_pixel_end, x_scale, x_value_start), (y_pixel_start, y_pixel_end, y_scale, y_value_start) = select_axes_and_calibrate(image_path)
line_points = extract_line_data(image_path, x_pixel_start, x_pixel_end, y_pixel_start, y_pixel_end)

# Convert pixel coordinates to actual values
x_points = [(point[0] - x_pixel_start) * x_scale + x_value_start for point in line_points]
y_points = [(point[1] - y_pixel_start) * y_scale + y_value_start for point in line_points]

x_points = pd.Series(x_points)
y_points = pd.Series(y_points)

print(f"Extracted x points: {x_points}")
print(f"x points size: {x_points.shape}")
print(f"Extracted y points: {y_points}")
print(f"y points size: {y_points.size}")

# plot extracted data quickly to see preview
plt.figure()
plt.scatter(x_points, y_points, color='r', label='data')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.grid()
plt.legend()

# clean data to exclude points 2*std outside of overall trend
rolling_std = x_points.rolling(window=10, center=True).std().dropna()
rolling_median = x_points.rolling(window=10, center=True).median().dropna()
lower_bound = rolling_median - (2 * rolling_std)
upper_bound = rolling_median + (2 * rolling_std)
outliers = x_points[(x_points < lower_bound) & (x_points > upper_bound)]
outlier_indexes = x_points[outliers].index
cleaned_x_points = x_points.drop(outlier_indexes, axis=0)
cleaned_y_points = y_points.drop(outlier_indexes, axis=0)

# plot cleaned x and y points
plt.figure()
plt.plot(cleaned_x_points, cleaned_y_points, color='r')
plt.grid()
plt.show()

# # generate .csv file with the same name as the image file
# image_name = os.path.basename(image_path)
# csv_filename = os.path.splitext(image_name)[0] + ".csv"
# output_dir_name = "output_data_csv_files"
# output_csv_path = os.path.join(output_dir_name, csv_filename)

# with open(output_csv_path, "w") as f:
#     f.write("x,y\n")  # optional header
#     for x, y in zip(x_points, y_points):
#         f.write(f"{x},{y}\n")

# print(f"Data saved to {output_csv_path}")