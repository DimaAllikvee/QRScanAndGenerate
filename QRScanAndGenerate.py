import cv2
from pyzbar.pyzbar import decode
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode
import threading

def generate_qr_code(data, color="black", background="white", size=300):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color=background).convert('RGB')
    img = img.resize((size, size), Image.LANCZOS)
    
    return img


def show_qr_code(img, label):
    img = ImageTk.PhotoImage(img)
    label.configure(image=img)
    label.image = img



def on_generate_qr_code_url():
    url = url_entry.get()
    if url:
        color = selected_color.get()
        qr_img = generate_qr_code(url, color=color, size=300)
        show_qr_code(qr_img, qr_label_url)
    else:
        print("Please enter a URL.")

def on_generate_qr_code_text():
    text = text_entry.get()
    if text:
        color = selected_color.get()
        qr_img = generate_qr_code(text, color=color, size=300)
        show_qr_code(qr_img, qr_label_text)
    else:
        print("Please enter text.")

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Не удалось открыть веб-камеру")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)

        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            print("QR Code detected:", qr_data)

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_scan_qr_code():
    threading.Thread(target=scan_qr_code, daemon=True).start()

# Режим отображения
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x600")
app.title("QR Code Scanner + Generate")

# Главная страница
frame_home = ctk.CTkFrame(app, corner_radius=15)
frame_home.pack(pady=20, padx=20, fill="both", expand=True)


header = ctk.CTkLabel(frame_home, text="QR Code Scanner IVKHK", font=("Arial", 24), corner_radius=15, height=50)
header.pack(pady=10)


button1 = ctk.CTkButton(frame_home, text="Scan QR Code", corner_radius=10, command=start_scan_qr_code)
button1.pack(pady=10)


frame_1 = ctk.CTkFrame(app, corner_radius=15)
frame_2 = ctk.CTkFrame(app, corner_radius=15)
frame_3 = ctk.CTkFrame(app, corner_radius=15)
frame_about = ctk.CTkFrame(app, corner_radius=15)

# Функции для переключения между фреймами
def show_frame_home():
    frame_home.pack(pady=20, padx=20, fill="both", expand=True)
    frame_1.pack_forget()
    frame_2.pack_forget()
    frame_3.pack_forget()
    frame_about.pack_forget()

def show_frame_1():
    frame_home.pack_forget()
    frame_1.pack(pady=20, padx=20, fill="both", expand=True)
    frame_2.pack_forget()
    frame_3.pack_forget()
    frame_about.pack_forget()

def show_frame_2():
    frame_home.pack_forget()
    frame_1.pack_forget()
    frame_2.pack(pady=20, padx=20, fill="both", expand=True)
    frame_3.pack_forget()
    frame_about.pack_forget()

def show_frame_3():
    frame_home.pack_forget()
    frame_1.pack_forget()
    frame_2.pack_forget()
    frame_3.pack(pady=20, padx=20, fill="both", expand=True)
    frame_about.pack_forget()

def show_frame_about():
    frame_home.pack_forget()
    frame_1.pack_forget()
    frame_2.pack_forget()
    frame_3.pack_forget()
    frame_about.pack(pady=20, padx=20, fill="both", expand=True)

# Фреймы
ctk.CTkLabel(frame_1, text="QR Code(URL)", font=("Arial", 24)).pack(pady=20)
ctk.CTkLabel(frame_2, text="QR Code(Text)", font=("Arial", 24)).pack(pady=20)
ctk.CTkLabel(frame_3, text="Change Color", font=("Arial", 24)).pack(pady=20)

# Текстовые поля для фреймов
url_entry = ctk.CTkEntry(frame_1, placeholder_text="Enter URL", width=350)
url_entry.pack(pady=10)

text_entry = ctk.CTkEntry(frame_2, placeholder_text="Enter text", width=350)
text_entry.pack(pady=10)

# Метки для отображения QR-кодов
qr_label_url = ctk.CTkLabel(frame_1, text="")
qr_label_url.pack(pady=10)

qr_label_text = ctk.CTkLabel(frame_2, text="")
qr_label_text.pack(pady=10)


# Кнопки внутри фреймов
button_forframe = ctk.CTkButton(frame_1, text="Generate QR Code from URL", corner_radius=10, command=on_generate_qr_code_url)
button_forframe.pack(pady=10)

button_for = ctk.CTkButton(frame_2, text="Generate QR Code from Text", corner_radius=10, command=on_generate_qr_code_text)
button_for.pack(pady=10)

# Добавление опции для выбора цвета QR-кода
selected_color = ctk.StringVar(value="black")

color_label = ctk.CTkLabel(frame_3, text="Select Color:")
color_label.pack(pady=5)

color_options = ["black", "blue", "green", "red"]
color_menu = ctk.CTkOptionMenu(frame_3, variable=selected_color, values=color_options)
color_menu.pack(pady=10)

# Фрейм "About"
about_label = ctk.CTkLabel(frame_about, text="Developers:\n\nDima Allikvee\nJuri Allikvee\nKirill Kyrve\nNPTV23", font=("Arial", 18), justify="left")
about_label.pack(pady=20, padx=20)

# Навигационная панель
navigation_frame = ctk.CTkFrame(app, width=140, corner_radius=15)
navigation_frame.pack(side="left", fill="y", padx=10, pady=10)
navigation_frame.pack_propagate(False)

home_button = ctk.CTkButton(navigation_frame, text="Home", command=show_frame_home, corner_radius=10)
home_button.pack(pady=10, padx=10, anchor="n")

frame1_button = ctk.CTkButton(navigation_frame, text="QR Code(URL)", command=show_frame_1, corner_radius=10)
frame1_button.pack(pady=10, padx=10, anchor="n")

frame2_button = ctk.CTkButton(navigation_frame, text="QR Code(Text)", command=show_frame_2, corner_radius=10)
frame2_button.pack(pady=10, padx=10, anchor="n")

frame3_button = ctk.CTkButton(navigation_frame, text="Change Colour", command=show_frame_3, corner_radius=10)
frame3_button.pack(pady=10, padx=10, anchor="n")

about_button = ctk.CTkButton(navigation_frame, text="About", command=show_frame_about, corner_radius=10)
about_button.pack(pady=10, padx=10, anchor="n")

# Системное меню
system_menu = ctk.CTkOptionMenu(navigation_frame, values=["System", "Dark", "Light"], command=ctk.set_appearance_mode, corner_radius=10)
system_menu.pack(pady=10, padx=10, anchor="s")
    

show_frame_1()
app.mainloop()
