import cv2
import numpy as np

def plot_table(frame, cell_data, num_rows=2, num_columns=2, title="", col_width=400, row_height=60, font=cv2.FONT_HERSHEY_SIMPLEX, font_size=0.7, font_color=(0, 0, 0), border_color=(0, 0, 0), line_thickness=2, background_color=(200,200,200), opacity=0.5, start_x=100, start_y=20):
    if title == "" or title is None:
        end_x = start_x + num_columns * col_width
        end_y = start_y + num_rows * row_height

        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), border_color, line_thickness)
        overlay = frame.copy()
        cv2.rectangle(overlay, (start_x, start_y), (end_x, end_y), background_color, -1)
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        for i in range(1, num_rows):
            y = start_y + i * row_height
            cv2.line(frame, (start_x, y), (end_x, y), border_color, line_thickness)

        for i in range(1, num_columns):
            x = start_x + i * col_width
            cv2.line(frame, (x, start_y), (x, end_y), border_color, line_thickness)

        for i in range(0, num_columns*num_rows):
            row_start_x = start_x + (i % num_columns) * col_width
            row_start_y = start_y + (i // num_columns) * row_height
            text_height = cv2.getTextSize(cell_data[i], font, font_size, line_thickness)[0][1]
            text_width = cv2.getTextSize(cell_data[i], font, font_size, line_thickness)[0][0]
            text_start_x = row_start_x + (col_width - text_width) // 2
            text_start_y = row_start_y + row_height - (row_height - text_height) // 2
            cv2.putText(frame, cell_data[i], (text_start_x, text_start_y), font, font_size, font_color, line_thickness)
    else:
        num_rows = num_rows + 1

        end_x = start_x + num_columns * col_width
        end_y = start_y + num_rows * row_height

        text_width = cv2.getTextSize(title, font, font_size, line_thickness)[0][0]
        text_height = cv2.getTextSize(title, font, font_size, line_thickness)[0][1]

        text_start_x = start_x + (end_x - start_x - text_width) // 2
        text_start_y = start_y + row_height - (row_height - text_height) // 2

        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), border_color, line_thickness)
        overlay = frame.copy()
        cv2.rectangle(overlay, (start_x, start_y), (end_x, end_y), background_color, -1)
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        cv2.putText(frame, title, (text_start_x, text_start_y), font, font_size, font_color, line_thickness)

        for i in range(1, num_rows):
            y = start_y + i * row_height
            cv2.line(frame, (start_x, y), (end_x, y), border_color, line_thickness)

        for i in range(1, num_columns):
            x = start_x + i * col_width
            cv2.line(frame, (x, start_y + row_height), (x, end_y), border_color, line_thickness)

        for i in range(0, num_columns*(num_rows-1)):
            row_start_x = start_x + (i % num_columns) * col_width
            row_start_y = start_y + row_height + (i // num_columns) * row_height
            text_height = cv2.getTextSize(cell_data[i], font, font_size, line_thickness)[0][1]
            text_width = cv2.getTextSize(cell_data[i], font, font_size, line_thickness)[0][0]
            text_start_x = row_start_x + (col_width - text_width) // 2
            text_start_y = row_start_y + row_height - (row_height - text_height) // 2
            cv2.putText(frame, cell_data[i], (text_start_x, text_start_y), font, font_size, font_color, line_thickness)