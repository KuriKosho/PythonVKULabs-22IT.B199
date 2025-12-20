import pandas as pd
from datetime import datetime


class ExcelExporter:
    @staticmethod
    def export_subscriptions(data, file_path):
        """
        data: List of dictionaries/tuples từ Database
        file_path: Đường dẫn lưu file
        """
        try:
            # 1. Chuẩn bị dữ liệu cho DataFrame
            # data từ DAO là list các sqlite3.Row object, cần chuyển sang dict
            export_data = []
            for row in data:
                export_data.append({
                    "Mã Gói": row['id'],
                    "Khách Hàng": row['full_name'],
                    "Tên Gói": row['plan_name'],
                    "Giá Tiền": row['price'],
                    "Ngày Bắt Đầu": row['start_date'],
                    "Ngày Hết Hạn": row['end_date'],
                    "Trạng Thái": row['status'],
                    "Ghi Chú": row['note']
                })

            # 2. Tạo DataFrame
            df = pd.DataFrame(export_data)

            # 3. Xuất file
            # index=False để không in cột số thứ tự 0,1,2... của pandas
            df.to_excel(file_path, index=False, engine='openpyxl')

            return True, "Xuất file thành công!"
        except Exception as e:
            return False, str(e)