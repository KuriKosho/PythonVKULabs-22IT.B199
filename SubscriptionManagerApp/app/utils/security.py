import bcrypt

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu plain text sang chuỗi hash."""
    # Chuyển string sang bytes
    bytes_password = password.encode('utf-8')
    # Tạo salt và hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_password, salt)
    # Trả về string để lưu vào DB
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiểm tra mật khẩu nhập vào có khớp với hash trong DB không."""
    bytes_plain = plain_password.encode('utf-8')
    bytes_hashed = hashed_password.encode('utf-8')
    return bcrypt.checkpw(bytes_plain, bytes_hashed)