import cv2

def process(image_path: str):
    cv2_image = cv2.imread(image_path)
    cv2_image_gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(cv2_image_gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output = cv2_image.copy()

    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

    centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            area = cv2.contourArea(contour)
            if area > 50:
                centers.append((cx, cy))

    for center in centers:
        cv2.circle(output, center, 5, (0, 0, 255), -1)
    
    number_of_bugs = len(centers)
    cv2.putText(output, f"Number of bugs: {number_of_bugs}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
