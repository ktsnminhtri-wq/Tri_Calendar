import datetime
import calendar
from PIL import Image, ImageDraw, ImageFont

def tao_hinh_nen_lich_sally():
    # 1. Tên file đích dành riêng cho Sally
    duong_dan_day_du = "sally_wallpaper.png"

    # 2. Khởi tạo Canvas nền tối
    W, H = 1170, 2532
    img = Image.new('RGBA', (W, H), color=(241, 237, 226, 255))
    draw = ImageDraw.Draw(img)

    # 3. Nạp Font
    try:
        font_thang = ImageFont.truetype("font.ttf", 32)
        font_dem_nguoc = ImageFont.truetype("font.ttf", 45)
        font_thu = ImageFont.truetype("font.ttf", 14) # Font siêu nhỏ cho chữ T2..CN
    except:
        font_thang = font_dem_nguoc = font_thu = ImageFont.load_default()

    # 4. Thông số lưới Lịch
    kc_hat = 38; r = 8
    w_thang = 6 * kc_hat
    kc_thang_x = 340; kc_thang_y = 350
    w_tong_grid = (2 * kc_thang_x) + w_thang
    margin_x = (W - w_tong_grid) // 2
    margin_y = 850

    # 5. Xử lý ngày tháng (Chuẩn giờ VN)
    now_utc = datetime.datetime.utcnow()
    now_vn = now_utc + datetime.timedelta(hours=7)
    hom_nay = now_vn.date()
    nam_hien_tai = 2026

    # 6. Bảng màu tuỳ biến cho Sally 
    COLOR_PAST = (255, 255, 255, 255)       
    COLOR_TODAY = (255, 110, 150, 255)        # Hồng Cam (Rose Gold)
    COLOR_FUTURE_NORMAL = (100, 100, 105, 255) 
    COLOR_WEEKDAY = (100, 100, 105, 255)      # Xám nhạt cho tiêu đề Thứ

    # Dãy ký tự viết tắt của các Thứ (Bắt đầu từ Thứ 2)
    weekdays = ["M", "T", "W", "T", "F", "S", "S"] 

    # 7. Vẽ Lưới 365 ngày theo đúng Cấu trúc Thứ
    for thang in range(1, 13):
        col_thang = (thang - 1) % 3; row_thang = (thang - 1) // 3
        toa_do_x_thang = margin_x + col_thang * kc_thang_x
        toa_do_y_thang = margin_y + row_thang * kc_thang_y

        # Vẽ tên Tháng
        ten_thang = calendar.month_abbr[thang]
        bbox_text = draw.textbbox((0, 0), ten_thang, font=font_thang)
        x_text = toa_do_x_thang + w_thang - (bbox_text[2] - bbox_text[0]) + r
        draw.text((x_text, toa_do_y_thang - 70), ten_thang, font=font_thang, fill=(100, 100, 105, 255))

        # [MỚI] Vẽ hàng tiêu đề Thứ (M T W T F S S) siêu nhỏ trên đầu mỗi tháng
        for i, thu in enumerate(weekdays):
            bbox_thu = draw.textbbox((0, 0), thu, font=font_thu)
            x_thu = toa_do_x_thang + i * kc_hat - (bbox_thu[2] - bbox_thu[0])/2
            draw.text((x_thu, toa_do_y_thang - 35), thu, font=font_thu, fill=COLOR_WEEKDAY)

        # [MỚI] Tìm xem ngày mùng 1 của tháng này là Thứ mấy (0=T2, 6=CN)
        first_weekday, so_ngay_trong_thang = calendar.monthrange(nam_hien_tai, thang)

        for ngay in range(1, so_ngay_trong_thang + 1):
            ngay_xet = datetime.date(nam_hien_tai, thang, ngay)
            
            # [MỚI] Tính tọa độ Hàng và Cột dựa vào Thứ trong tuần
            vi_tri_tren_luoi = first_weekday + (ngay - 1)
            row_hat = vi_tri_tren_luoi // 7  # Tuần thứ mấy trong tháng
            col_hat = vi_tri_tren_luoi % 7   # Cột thứ mấy (0=T2, 6=CN)
            
            x = toa_do_x_thang + col_hat * kc_hat
            y = toa_do_y_thang + row_hat * kc_hat
            bbox = [x - r, y - r, x + r, y + r]

            # Tô màu
            if ngay_xet < hom_nay:
                draw.ellipse(bbox, fill=COLOR_PAST) 
            elif ngay_xet == hom_nay:
                draw.ellipse([x-r-2, y-r-2, x+r+2, y+r+2], fill=COLOR_TODAY) 
            else:
                draw.ellipse(bbox, fill=COLOR_FUTURE_NORMAL) 

    # 8. Vẽ Đếm ngược
    cuoi_nam = datetime.date(nam_hien_tai, 12, 31)
    text_dem_nguoc = f"{(cuoi_nam - hom_nay).days}d left"
    bbox_text = draw.textbbox((0, 0), text_dem_nguoc, font=font_dem_nguoc)
    draw.text(((W - (bbox_text[2] - bbox_text[0])) // 2, 2150), text_dem_nguoc, font=font_dem_nguoc, fill=COLOR_TODAY)

    # 9. Xuất file
    img.save(duong_dan_day_du, format="PNG", quality=100)
    print(f"✅ Đã lưu ảnh Sally: {duong_dan_day_du}")

if __name__ == "__main__":
    tao_hinh_nen_lich_sally()
