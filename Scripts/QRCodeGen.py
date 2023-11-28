import sys
import os
import qrcode


def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    directory_path = r"C:\Users\yusuf\Pictures\QRCODE"
    file_path = os.path.join(directory_path, f"{filename}.png")
    img.save(file_path)
    print(f"QR code generated as '{filename}.png'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Script.py <LINK> <QRNAME>")
    else:
        link = sys.argv[1]
        qr_name = sys.argv[2]
        generate_qr_code(link, qr_name)
