import cv2

def detect_ground(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    height, width = edges.shape
    # bottom_part = edges[int(0.9 * height):, :]  

    #
    # ground_contours, _ = cv2.findContours(bottom_part, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # # if len(ground_contours) == 0:
    # #     return None  # No ground detected

    # ground_y = height - (bottom_part.shape[0] - np.max([pt[0][1] for contour in ground_contours for pt in contour]))

    return height

def detect_object_and_measure(image):


    ground_y = detect_ground(image)
    if ground_y is None:
        print("Ground level not detected in the image. Please provide an image that shows the ground surface.")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest_contour)

        object_bottom_y = y + h
        distance_in_pixels = ground_y - object_bottom_y

        print(f"Distance from object to ground in pixels: {distance_in_pixels}")
        cv2.putText(image, f"Distance: {distance_in_pixels}", 
            (30, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)

        final_height = distance_in_pixels

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.line(image, (0, ground_y), (image.shape[1], ground_y), (255, 0, 255), 2)  
        cv2.imshow('Object Detection', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('outpt3.jpg', image)
    else:
        print("No object detected.")


image = cv2.imread('ht3.jpg')

detect_object_and_measure(image) 


