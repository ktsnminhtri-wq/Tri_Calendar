import datetime
import calendar
from PIL import Image, ImageDraw, ImageFont

def tao_hinh_nen_lich():
    # 1. Tên file ảnh đích
    duong_dan_day_du = "tri_wallpaper.png"

    # 2. Khởi tạo Canvas nền đen nhám
    W, H = 1170, 2532
    img = Image.new('RGBA', (W, H), color=(18, 18, 18, 255))
    draw = ImageDraw.Draw(img)

    # 3. Nạp Font
    try:
        font_thang = ImageFont.truetype("font.ttf", 32)
        font_dem_nguoc = ImageFont.truetype("font.ttf", 45)
    except:
        font_thang = font_dem_nguoc = ImageFont.load_default()

    # 4. Thông số lưới Lịch
    kc_hat = 38; r = 8
    w_thang = 6 * kc_hat
    kc_thang_x = 340; kc_thang_y = 350
    w_tong_grid = (2 * kc_thang_x) + w_thang
    margin_x = (W - w_tong_grid) // 2
    margin_y = 850

    # 5. XỬ LÝ NGÀY THÁNG (Tự động cập nhật theo giờ Việt Nam UTC+7)
    now_utc = datetime.datetime.utcnow()
    now_vn = now_utc + datetime.timedelta(hours=7)
    hom_nay = now_vn.date()
    nam_hien_tai = 2026

    # Mốc Tử vi
    vung_do = [(datetime.date(2026, 4, 17), datetime.date(2026, 5, 16)), (datetime.date(2026, 11, 9), datetime.date(2026, 12, 8))]
    vung_xanh = [(datetime.date(2026, 3, 19), datetime.date(2026, 4, 16)), (datetime.date(2026, 7, 14), datetime.date(2026, 8, 12))]
    vung_cam = [(datetime.date(2026, 2, 17), datetime.date(2026, 3, 18))]

    # 6. Bảng màu
    COLOR_PAST = (255, 255, 255, 255)       
    COLOR_TODAY = (255, 87, 34, 255)        
    COLOR_FUTURE_NORMAL = (44, 44, 46, 255) 
    COLOR_DIM_RED = (100, 0, 0, 255)    
    COLOR_DIM_GREEN = (25, 105, 0, 255)  
    COLOR_DIM_ORANGE = (110, 110, 0, 255) 

    def lay_mau_tuong_lai(ngay_dang_xet):
        for start, end in vung_do:
            if start <= ngay_dang_xet <= end: return COLOR_DIM_RED
        for start, end in vung_xanh:
            if start <= ngay_dang_xet <= end: return COLOR_DIM_GREEN
        for start, end in vung_cam:
            if start <= ngay_dang_xet <= end: return COLOR_DIM_ORANGE
        return COLOR_FUTURE_NORMAL

    # 7. Vẽ Lưới 365 ngày
    for thang in range(1, 13):
        col_thang = (thang - 1) % 3; row_thang = (thang - 1) // 3
        toa_do_x_thang = margin_x + col_thang * kc_thang_x
        toa_do_y_thang = margin_y + row_thang * kc_thang_y

        ten_thang = calendar.month_abbr[thang]
        bbox_text = draw.textbbox((0, 0), ten_thang, font=font_thang)
        x_text = toa_do_x_thang + w_thang - (bbox_text[2] - bbox_text[0]) + r
        draw.text((x_text, toa_do_y_thang - 60), ten_thang, font=font_thang, fill=(142, 142, 147, 255))

# Lấy thêm thông tin mùng 1 là Thứ mấy (first_weekday)
        first_weekday, so_ngay_trong_thang = calendar.monthrange(nam_hien_tai, thang)
        
        for ngay in range(1, so_ngay_trong_thang + 1):
            ngay_xet = datetime.date(nam_hien_tai, thang, ngay)
            
            # Tính toán lại tọa độ lưới
            vi_tri_tren_luoi = first_weekday + (ngay - 1)
            row_hat = vi_tri_tren_luoi // 7
            col_hat = vi_tri_tren_luoi % 7
            x = toa_do_x_thang + col_hat * kc_hat
            y = toa_do_y_thang + row_hat * kc_hat
            bbox = [x - r, y - r, x + r, y + r]

            if ngay_xet < hom_nay:
                draw.ellipse(bbox, fill=COLOR_PAST) 
            elif ngay_xet == hom_nay:
                draw.ellipse([x-r-2, y-r-2, x+r+2, y+r+2], fill=COLOR_TODAY) 
            else:
                draw.ellipse(bbox, fill=lay_mau_tuong_lai(ngay_xet)) 

    # 8. Vẽ Đếm ngược
    cuoi_nam = datetime.date(nam_hien_tai, 12, 31)
    text_dem_nguoc = f"{(cuoi_nam - hom_nay).days}d left"
    bbox_text = draw.textbbox((0, 0), text_dem_nguoc, font=font_dem_nguoc)
    draw.text(((W - (bbox_text[2] - bbox_text[0])) // 2, 2150), text_dem_nguoc, font=font_dem_nguoc, fill=COLOR_TODAY)

    # 9. Xuất file
    img.save(duong_dan_day_du, format="PNG", quality=100)
    print(f"✅ Đã lưu ảnh thành công: {duong_dan_day_du}")

if __name__ == "__main__":
    tao_hinh_nen_lich()
