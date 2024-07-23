# cv2-table-plotter

`cv2-table-plotter` is a simple Python library designed to overlay tables on images or frames using OpenCV. This library helps in drawing and customizing tables, including features like background color, opacity, title, and more.

## Features

- Draw tables on images or video frames using OpenCV.
- Customize the number of rows and columns.
- Set table and cell dimensions.
- Add titles to the tables.
- Adjust font, colors, and opacity.

## Installation

You can install the `cv2-table-plotter` library using pip:

```bash
pip install cv2-table-plotter
```
## Usage
Here is a basic example of how to use `cv2-table-plotter`:
```bash
import cv2
import numpy as np
from cv2_table_plotter import plot_table

# Create a blank image
frame = np.ones((600, 1600, 3), dtype=np.uint8) * 255

# Data to be displayed in the table
cell_data = ["Cell 1", "Cell 2", "Cell 3", "Cell 4"]

# Draw table on the image
plot_table(
    frame,
    cell_data,
    num_rows=2,
    num_columns=2,
    title="Sample Table",
    col_width=400,
    row_height=60,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_size=0.7,
    font_color=(0, 0, 0),
    border_color=(0, 0, 0),
    line_thickness=2,
    background_color=(200, 200, 200),
    opacity=0.5,
    start_x=1100,
    start_y=20
)

# Display the image
cv2.imshow('Table', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
## Function Parameters
### `plot_table`
* `frame`: The image or video frame on which the table will be drawn.
* `cell_data`: List of strings to be displayed in the table cells.
* `num_rows`: Number of rows in the table (default: 2).
* `num_columns`: Number of columns in the table (default: 2).
* `title`: Title of the table (default: "").
* `col_width`: Width of each column (default: 400).
* `row_height`: Height of each row (default: 60).
* `font`: Font type for the text (default: cv2.FONT_HERSHEY_SIMPLEX).
* `font_size`: Font size for the text (default: 0.7).
* `font_color`: Font color in BGR (default: (0, 0, 0)).
* `border_color`: Border color of the table in BGR (default: (0, 0, 0)).
* `line_thickness`: Thickness of the table lines (default: 2).
* `background_color`: Background color of the table in BGR (default: (200, 200, 200)).
* `opacity`: Opacity of the background color (default: 0.5).
* `start_x`: Starting x-coordinate of the table (default: 1100).
* `start_y`: Starting y-coordinate of the table (default: 20).
## License
This project is licensed under the MIT License.

## Author
* Sezin Arseven

## Acknowledgments
* OpenCV for providing an excellent computer vision library.
* The Python community for continuous support and inspiration.