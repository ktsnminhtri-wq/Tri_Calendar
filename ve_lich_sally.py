import datetime
import calendar
from PIL import Image, ImageDraw, ImageFont

def tao_hinh_nen_lich_sally():
    # 1. Tên file đích dành riêng cho Sally
    duong_dan_day_du = "sally_wallpaper.png"

    # 2. Khởi tạo Canvas nền tối (Deep Blue/Dark Gray)
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

    # 5. Xử lý ngày tháng (Chuẩn giờ VN)
    now_utc = datetime.datetime.utcnow()
    now_vn = now_utc + datetime.timedelta(hours=7)
    hom_nay = now_vn.date()
    nam_hien_tai = 2026

    # 6. Bảng màu tuỳ biến cho Sally 
    COLOR_PAST = (255, 255, 255, 255)       
    COLOR_TODAY = (255, 110, 150, 255)        # Điểm nhấn: Màu Hồng Cam (Rose/Pastel Pink)
    COLOR_FUTURE_NORMAL = (44, 44, 46, 255) 

    # 7. Vẽ Lưới 365 ngày
    for thang in range(1, 13):
        col_thang = (thang - 1) % 3; row_thang = (thang - 1) // 3
        toa_do_x_thang = margin_x + col_thang * kc_thang_x
        toa_do_y_thang = margin_y + row_thang * kc_thang_y

        ten_thang = calendar.month_abbr[thang]
        bbox_text = draw.textbbox((0, 0), ten_thang, font=font_thang)
        x_text = toa_do_x_thang + w_thang - (bbox_text[2] - bbox_text[0]) + r
        draw.text((x_text, toa_do_y_thang - 60), ten_thang, font=font_thang, fill=(142, 142, 147, 255))

        so_ngay_trong_thang = calendar.monthrange(nam_hien_tai, thang)[1]
        for ngay in range(1, so_ngay_trong_thang + 1):
            ngay_xet = datetime.date(nam_hien_tai, thang, ngay)
            row_hat = (ngay - 1) // 7; col_hat = (ngay - 1) % 7
            x = toa_do_x_thang + col_hat * kc_hat
            y = toa_do_y_thang + row_hat * kc_hat
            bbox = [x - r, y - r, x + r, y + r]

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
    draw.text(((W - (bbox_text[2] - bbox_text[0])) // 2, 2250), text_dem_nguoc, font=font_dem_nguoc, fill=COLOR_TODAY)

    # 9. Xuất file
    img.save(duong_dan_day_du, format="PNG", quality=100)
    print(f"✅ Đã lưu ảnh Sally: {duong_dan_day_du}")

if __name__ == "__main__":
    tao_hinh_nen_lich_sally()
