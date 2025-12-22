import cv2
import dlib
import os
import numpy as np

# --- CẤU HÌNH ---
VECTOR_FILE = "face_vectors.txt"
PREDICTOR_PATH = "models/shape_predictor_68_face_landmarks.dat"
RECOG_MODEL_PATH = "models/dlib_face_recognition_resnet_model_v1.dat"
THRESHOLD = 0.5  # Ngưỡng so sánh (càng nhỏ càng khắt khe, 0.6 là chuẩn của Dlib)

# --- 1. LOAD MODEL DLIB ---
if not os.path.exists(PREDICTOR_PATH) or not os.path.exists(RECOG_MODEL_PATH):
    print("LỖI: Thiếu file model .dat")
    exit()

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(PREDICTOR_PATH)
facerec = dlib.face_recognition_model_v1(RECOG_MODEL_PATH)

# --- 2. LOAD DỮ LIỆU VECTOR ĐÃ LƯU ---
known_face_vectors = []
known_face_names = []

if os.path.exists(VECTOR_FILE):
    with open(VECTOR_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0: continue

            # Tách tên file và chuỗi vector
            parts = line.split("|")
            file_path = parts[0]
            vector_str = parts[1]

            # Chuyển chuỗi số thành mảng numpy
            vector_nums = list(map(float, vector_str.split(",")))
            vector_np = np.array(vector_nums)

            # Lấy tên người từ tên file (vd: dataset/user_1.jpg -> user_1)
            name = os.path.basename(file_path).split('.')[0]

            known_face_vectors.append(vector_np)
            known_face_names.append(name)
    print(f"Đã load thành công {len(known_face_names)} khuôn mặt từ database.")
else:
    print("Cảnh báo: Không tìm thấy file face_vectors.txt! Hãy chạy file trích xuất trước.")
    known_face_vectors = []

# --- 3. BẮT ĐẦU CAMERA CHECK-IN ---
cap = cv2.VideoCapture(0)
print("Hệ thống Check-in đang chạy... Nhấn 'q' để thoát.")

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt
    faces = detector(rgb_frame)

    for face in faces:
        # Lấy landmarks và tính vector cho mặt hiện tại trên cam
        shape = sp(rgb_frame, face)
        face_descriptor = facerec.compute_face_descriptor(rgb_frame, shape)
        current_face_vector = np.array(face_descriptor)

        # Mặc định là người lạ
        name = "Unknown"
        min_dist = 100  # Khởi tạo khoảng cách rất lớn
        color = (0, 0, 255)  # Màu đỏ cho người lạ

        # SO SÁNH VỚI DATABASE
        if len(known_face_vectors) > 0:
            # Tính khoảng cách Euclidean giữa mặt hiện tại và TẤT CẢ mặt trong DB
            # Công thức: dist = sqrt(sum((a-b)^2))
            distances = np.linalg.norm(known_face_vectors - current_face_vector, axis=1)

            # Tìm khoảng cách nhỏ nhất
            min_index = np.argmin(distances)
            min_dist = distances[min_index]

            # Kiểm tra ngưỡng (Threshold)
            if min_dist < THRESHOLD:
                name = known_face_names[min_index]
                color = (0, 255, 0)  # Màu xanh lá cho người quen

        # --- VẼ LÊN MÀN HÌNH ---
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        # Vẽ khung
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Hiển thị tên và độ sai số (distance)
        # Distance càng nhỏ nghĩa là càng giống
        info_text = f"{name} ({min_dist:.2f})"
        cv2.putText(frame, info_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Giả lập check-in
        if name != "Unknown":
            cv2.putText(frame, "ACCESS GRANTED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("He thong Check-in VKU", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()