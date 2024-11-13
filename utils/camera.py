import cv2
import os
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
last_created_folder_path = os.path.join(current_dir, 'last_created_folder.txt')

def load_last_created_folder():
    if os.path.exists(last_created_folder_path):
        with open(last_created_folder_path, 'r') as file:
            return file.read().strip()
    return None

class CameraApp:
    
    def center_window(self):
        width = 510
        height = 550

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2) 
        y = (screen_height // 2) - (height // 2)

        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def __init__(self):
        self.camera_index = 0
        self.cap = cv2.VideoCapture(self.camera_index)
        self.window = None
        self.camera_label = None
        self.last_created_folder = load_last_created_folder()

    def open_camera_window(self):
        self.window = ctk.CTkToplevel()
        self.window.attributes('-topmost', True)
        self.window.geometry("510x550")
        self.window.title("Kamera")
        self.window.configure(bg="#2E2E2E")

        self.center_window()

        self.camera_label = ctk.CTkLabel(self.window, width=500, height=500, text="", fg_color="#2E2E2E")
        self.camera_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        switch_button = ctk.CTkButton(self.window, text="Kamera Değiştir", command=self.switch_camera)
        switch_button.grid(row=1, column=1, padx=5, pady=5)

        photo_button = ctk.CTkButton(self.window, text="Fotoğraf Çek", command=self.take_photo)
        photo_button.grid(row=1, column=2, padx=5, pady=5)

        self.update_frame()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

    def update_frame(self):
        _, frame = self.cap.read()
        frame = cv2.resize(frame, (500, 500))
        self.draw_center_frame(frame)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

        if self.window:
            self.window.after(10, self.update_frame)

    def draw_center_frame(self, frame):
        center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
        top_left = (center_x - 50, center_y - 50)
        bottom_right = (center_x + 50, center_y + 50)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    def switch_camera(self):
        self.cap.release()
        self.camera_index = 1 - self.camera_index
        self.cap = cv2.VideoCapture(self.camera_index)

    def take_photo(self):
        _, frame = self.cap.read()
        frame = cv2.resize(frame, (500, 500))
        self.draw_center_frame(frame)

        # Görüntüyü camera_label içinde göster
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

        # Kullanıcıdan fotoğrafı kaydetmek isteyip istemediğini sor
        self.ask_to_save_photo(frame)

    def ask_to_save_photo(self, frame):
        # Uyarı penceresi oluştur
        save_prompt = ctk.CTkToplevel(self.window)
        save_prompt.title("Fotoğraf Kaydet")
        save_prompt.geometry("600x600")  # Pencere boyutu ayarlanabilir
        save_prompt.attributes('-topmost', True)

        # Fotoğrafı göster
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        
        photo_label = ctk.CTkLabel(save_prompt, image=imgtk, text="")
        photo_label.image = imgtk  # Referansı sakla
        photo_label.pack(pady=10)

        message = ctk.CTkLabel(save_prompt, text="Fotoğrafı kaydetmek istiyor musunuz?")
        message.pack(pady=10)

        yes_button = ctk.CTkButton(save_prompt, text="Evet", command=lambda: self.save_photo(frame, save_prompt))
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = ctk.CTkButton(save_prompt, text="Hayır", command=lambda: self.retry_camera(save_prompt))
        no_button.pack(side=tk.RIGHT, padx=10)

    def save_photo(self, frame, save_prompt):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_path = os.path.join(self.last_created_folder, f"photo_{timestamp}.jpg")
        
        cv2.imwrite(photo_path, frame)
        
        print(f"Fotoğraf kaydedildi: {photo_path}")
        save_prompt.destroy()  # Uyarı penceresini kapat
        self.window.destroy()
        self.window.after(500, lambda: messagebox.showinfo("Bilgi", f"Fotoğraf kaydedildi: {photo_path}"))
    

    def retry_camera(self, save_prompt):
        save_prompt.destroy()  # Uyarı penceresini kapat
        self.update_frame()  # Yeniden kamerayı aç

    def close_window(self):
        self.cap.release()
        self.window.destroy()
        self.window = None

# button_7 tıklanırsa çağırmak için dışa aktarılan fonksiyon
def launch_camera_app():
    camera_app = CameraApp()
    camera_app.open_camera_window()

# CustomTkinter başlatılır
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
