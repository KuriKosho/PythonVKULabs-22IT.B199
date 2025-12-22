import cv2
import dlib
import os
import numpy as np

# --- CẤU HÌNH ---
FOLDER_NAME = "dataset"
VECTOR_FILE = "face_vectors.txt"

# Đường dẫn đến 2 file model bạn vừa tải (để cùng thư mục với code)
PREDICTOR_PATH = "models/shape_predictor_68_face_landmarks.dat"
RECOG_MODEL_PATH = "models/dlib_face_recognition_resnet_model_v1.dat"

# Kiểm tra xem file model có tồn tại không
if not os.path.exists(PREDICTOR_PATH) or not os.path.exists(RECOG_MODEL_PATH):
    print("LỖI: Chưa tìm thấy file .dat model!")
    print("Vui lòng tải 'shape_predictor_68_face_landmarks.dat' và 'dlib_face_recognition_resnet_model_v1.dat'")
    exit()

# 1. Tạo thư mục lưu ảnh
if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

# 2. Khởi tạo các model của Dlib
detector = dlib.get_frontal_face_detector()  # Phát hiện khuôn mặt
sp = dlib.shape_predictor(PREDICTOR_PATH)  # Tìm 68 điểm mốc
facerec = dlib.face_recognition_model_v1(RECOG_MODEL_PATH)  # Mã hóa thành vector

# 3. Mở camera
cap = cv2.VideoCapture(0)
count = 0

print("Camera đang chạy...")
print("- Nhấn 's': Lưu ảnh và trích xuất vector")
print("- Nhấn 'q': Thoát")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Lật gương

    # Dlib xử lý tốt hơn trên ảnh RGB (OpenCV mặc định là BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt
    faces = detector(rgb_frame)

    # Vẽ khung chữ nhật
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # (Tùy chọn) Vẽ các điểm mốc landmarks để nhìn cho ngầu
        landmarks = sp(rgb_frame, face)
        for n in range(0, 68):
            lx = landmarks.part(n).x
            ly = landmarks.part(n).y
            cv2.circle(frame, (lx, ly), 1, (0, 0, 255), -1)

    cv2.putText(frame, f"Saved: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow("Vector Extraction - VKU", frame)

    key = cv2.waitKey(1) & 0xFF

    # --- XỬ LÝ LƯU ẢNH VÀ VECTOR ---
    if key == ord('s'):
        if len(faces) > 0:
            # Lấy mặt đầu tiên
            face = faces[0]

            # 1. Xác định landmarks (68 điểm)
            shape = sp(rgb_frame, face)

            # 2. Tính toán vector 128 chiều (Đây là bước quan trọng nhất)
            # compute_face_descriptor trả về object vector
            face_descriptor = facerec.compute_face_descriptor(rgb_frame, shape)

            # Chuyển sang dạng numpy array để dễ lưu
            face_vector = np.array(face_descriptor)

            # --- LƯU DỮ LIỆU ---
            count += 1

            # A. Lưu ảnh cắt khuôn mặt
            x, y = max(0, face.left()), max(0, face.top())
            w, h = face.width(), face.height()
            face_img = frame[y:y + h, x:x + w]

            img_filename = f"{FOLDER_NAME}/user_{count}.jpg"
            if face_img.size > 0:
                cv2.imwrite(img_filename, face_img)

            # B. Lưu vector vào file text (chế độ append 'a')
            # Định dạng lưu: Tên_file | số_thứ_1, số_thứ_2, ...
            vector_str = ",".join(map(str, face_vector))  # Chuyển mảng thành chuỗi phân cách bởi dấu phẩy

            with open(VECTOR_FILE, "a") as f:
                f.write(f"{img_filename}|{vector_str}\n")

            print(f"--> Đã lưu ảnh: {img_filename}")
            print(f"--> Đã trích xuất vector (128 chiều) vào {VECTOR_FILE}")

            # In thử 5 số đầu của vector để kiểm tra
            print(f"    Vector mẫu: {face_vector[:5]} ...")

        else:
            print("Không tìm thấy khuôn mặt!")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()