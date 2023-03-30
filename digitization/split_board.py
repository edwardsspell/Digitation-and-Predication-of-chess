
import cv2

def split_square_board_image(board_image, output_name, out_dir):
    img = cv2.imread(board_image)
    if img.shape[0] != img.shape[1]:
        raise ValueError("Image must be a square in size")
    square_size = img.shape[0] // 8  # 1200 / 8
    for row_start in range(0, img.shape[0], square_size):
        i = row_start // square_size
        for col_start in range(0, img.shape[1], square_size):
            j = col_start // square_size
            
            out_loc = str(out_dir) + "/" + str(output_name) + "_" + str(
                i) + "_" + str(j) + ".jpg"

            cv2.imwrite(out_loc, img[row_start:row_start + square_size,
                                     col_start:col_start + square_size])


