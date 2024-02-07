import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Indices for upper and lower lips
lips_upper_indices = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
lips_lower_indices = [375, 321, 405, 314, 17, 84, 181, 91, 146, 61]

# Initialize webcam capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Detect facial landmarks using MediaPipe Face Mesh
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw the upper lip in orange
            for idx in range(len(lips_upper_indices) - 1):
                point1 = tuple(
                    [int(face_landmarks.landmark[lips_upper_indices[idx]].x * frame.shape[1]),
                     int(face_landmarks.landmark[lips_upper_indices[idx]].y * frame.shape[0])])
                point2 = tuple(
                    [int(face_landmarks.landmark[lips_upper_indices[idx + 1]].x * frame.shape[1]),
                     int(face_landmarks.landmark[lips_upper_indices[idx + 1]].y * frame.shape[0])])
                cv2.line(frame, point1, point2, (0, 165, 255), 2)  # Orange color

            # Draw the lower lip in orange
            for idx in range(len(lips_lower_indices) - 1):
                point1 = tuple(
                    [int(face_landmarks.landmark[lips_lower_indices[idx]].x * frame.shape[1]),
                     int(face_landmarks.landmark[lips_lower_indices[idx]].y * frame.shape[0])])
                point2 = tuple(
                    [int(face_landmarks.landmark[lips_lower_indices[idx + 1]].x * frame.shape[1]),
                     int(face_landmarks.landmark[lips_lower_indices[idx + 1]].y * frame.shape[0])])
                cv2.line(frame, point1, point2, (0, 165, 255), 2)  # Orange color

    # Display the frame with lip tracking
    cv2.imshow("Lip Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
