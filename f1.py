from graphviz import Digraph

# Khởi tạo đồ thị
dot = Digraph(comment='Use Case Diagram', format='png')
dot.attr(rankdir='LR', size='8')

# Các tác nhân
dot.node('KhachHang', 'Khách hàng', shape='plaintext')
dot.node('KhachSam', 'Khách vãng lai', shape='plaintext')
dot.node('QuanTri', 'Người quản trị', shape='plaintext')

# Các use case chính
usecases = {
    "TimKiem": "Tìm kiếm sản phẩm",
    "TimTheoTen": "Tìm theo tên sản phẩm",
    "TimTheoGia": "Tìm theo giá sản phẩm",
    "ThemGio": "Thêm sản phẩm vào giỏ hàng",
    "XemGio": "Xem giỏ hàng",
    "BoSPKhoiGio": "Bỏ hàng ra khỏi giỏ",
    "SoLuong": "Số lượng",
    "TongTien": "Tổng tiền",
    "ThanhToan": "Thanh toán",
    "ThanhToanATM": "Thanh toán bằng thẻ ATM",
    "ThanhToanNhan": "Thanh toán khi nhận hàng",
    "DangKy": "Đăng ký",
    "DangNhap": "Đăng nhập",
    "XemSP": "Xem sản phẩm",
    "ThemSP": "Thêm sản phẩm",
    "SuaSP": "Sửa sản phẩm",
    "XoaSP": "Xóa sản phẩm"
}

for key, label in usecases.items():
    dot.node(key, label, shape='ellipse')

# Quan hệ actor - usecase
dot.edge("KhachHang", "TimKiem")
dot.edge("KhachHang", "XemGio")
dot.edge("KhachHang", "ThanhToan")
dot.edge("KhachHang", "DangNhap")
dot.edge("KhachSam", "DangKy")
dot.edge("KhachSam", "XemSP")
dot.edge("QuanTri", "ThemSP")
dot.edge("QuanTri", "SuaSP")
dot.edge("QuanTri", "XoaSP")

# Quan hệ include / extend
dot.edge("TimKiem", "TimTheoTen", label="extend")
dot.edge("TimKiem", "TimTheoGia", label="extend")
dot.edge("XemGio", "ThemGio", label="extend")
dot.edge("XemGio", "BoSPKhoiGio", label="extend")
dot.edge("XemGio", "SoLuong", label="include")
dot.edge("XemGio", "TongTien", label="include")
dot.edge("ThanhToan", "ThanhToanATM", label="extend")
dot.edge("ThanhToan", "ThanhToanNhan", label="extend")

# Xuất file
dot.render('usecase', view=True)