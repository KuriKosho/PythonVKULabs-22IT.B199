# Subscription Manager App - Bao cao du an

## 1. Tong quan du an
- Ung dung desktop PyQt6 quan ly goi dich vu: khach hang (member), goi (plan), dang ky (subscription), thong ke va nhac han qua email.
- Kien truc chia tang: UI (PyQt6), Controller, DAO truy cap SQLite, utils ho tro (bao mat, export, gui email).
- Khoi dong tu `main.py`: khoi tao DB SQLite tai `assets/database/app.db`, nap QSS, hien cua so dang nhap, sau do vao giao dien chinh tabbed (Dashboard, Subscription, Members, Plans, Settings).

## 2. Cong nghe su dung
- Python 3.x, PyQt6 (UI), PyQt6-Charts/matplotlib (bieu do), pandas + openpyxl (xuat Excel), bcrypt (hash mat khau).
- SQLite lam co so du lieu noi bo (file db tao tu dong), smtplib de gui email Gmail SSL.
- Thu vien khac trong `requirements.txt`: numpy, opencv-python, face_recognition (chua duoc su dung trong ma hien tai), python-dateutil.

## 3. Cau truc ma nguon
- main.py: diem vao, set stylesheet, icon, khoi tao DB va AppController.
- app/config.py: hang so du an (duong dan DB, app name, kich thuoc cua so).
- app/controllers/: dieu phoi UI va nghiep vu (dang nhap/dang ky, khoi tao MainWindow, xu ly subscription).
- app/data/: DAO truy van SQLite (users, members, service_plans, subscriptions, system_settings) + db_connection tao bang mac dinh.
- app/ui/: man hinh Login, MainWindow va cac page (dashboard, members, plans, subs, settings) + component the thong ke.
- app/utils/: session dang nhap, hash/verify mat khau, helper tinh ngay/format tien, excel_exporter, notification_service gui email nhac han.
- assets/: styles/main.qss, icons, database/app.db (sau khi tao).

## 4. Cac tinh nang chinh
- Dang nhap/dang ky, luu mat khau hash bcrypt; luu session in-memory.
- Quan ly thanh vien: them/sua/xoa, tim kiem, loc co SĐT/Email.
- Quan ly goi dich vu: them/sua/xoa, tim kiem, loc theo gia min/max, sap xep.
- Quan ly subscription: tao/sua/xoa, auto tinh end_date theo duration goi, cap nhat trang thai Overdue neu het han, loc theo trang thai/plan/keyword, mau sac trang thai, (du kien) xuat Excel.
- Dashboard: the thong ke (tong member, goi active, doanh thu), bieu do pie/bar trang thai subscription, danh sach sap het han, nut gui email nhac nho.
- Settings: luu cau hinh SMTP (Email, app password), doi mat khau.

## 5. Phan tich co so du lieu (SQLite)
- users: id, username (unique), password_hash, role, avatar_path, face_vector (BLOB), created_at.
- members: id, user_id FK->users, full_name, phone, email, address, created_at.
- service_plans: id, user_id FK, name, duration_months, price, description, created_at.
- subscriptions: id, user_id, member_id FK->members, plan_id FK->service_plans, price, start_date, end_date, status (Active/Paused/Overdue/Cancelled), note, created_at.
- system_settings: id, user_id (unique FK), smtp_email, smtp_password, created_at.

## 6. Danh gia ky thuat
- Diem manh: phan lop ro (DAO/Controller/UI), DB tao tu dong, UI co loc/tim kiem, hash mat khau, co thong ke bieu do va nhac han email.
- Rui ro/han che: 
  - Cau hinh SMTP luu plaintext; nen ma hoa hoac an file .env.
  - Chua co kiem tra dau vao chuyen sau (email/phone format, SQL errors), thieu logging.
  - Tich hop face_recognition/opencv chua duoc dung; co the loai khoi deps hoac bo sung tinh nang.
  - SubsPage goi `SubController.export_to_excel` nhung chua ton tai ham; can noi lai voi ExcelExporter hoac thay doi ham goi.
  - Thieu test tu dong va xu ly loi trung tam.

## 7. Huong dan cai dat va chay
1) Cai dat Python 3.11+ (Windows).
2) Tao va kich hoat virtualenv (khuyen nghi):
   - `python -m venv .venv`
   - Windows: `.venv\Scripts\activate`
3) Cai thu vien: `pip install -r requirements.txt`.
4) Chay ung dung tu thu muc goc du an: `python main.py`. DB va bang se tao tu dong o `assets/database/app.db` neu chua co.
5) Tinh nang email: vao tab Settings nhap Gmail va App Password (SMTP SSL 465) truoc khi gui nhac han.
6) Neu muon xuat Excel, dam bao da cai openpyxl; sua ham export o SubsPage neu gap loi do thieu ham controller.
