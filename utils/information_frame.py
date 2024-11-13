import os
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

def create_information_frame(self):

        # Part Number label and text box
        part_label = ctk.CTkLabel(self.frame, text="Part Number", font=("Arial", 14))
        part_label.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")

        self.part_entry = ttk.Entry(self.frame, font=("Arial", 12))
        self.part_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Serial Number label and text box
        serial_label = ctk.CTkLabel(self.frame, text="Serial Number", font=("Arial", 14))
        serial_label.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="w")

        self.serial_entry = ttk.Entry(self.frame, font=("Arial", 12))
        self.serial_entry.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="ew")

        # Operation Number label and text box
        operation_label = ctk.CTkLabel(self.frame, text="Operation Number", font=("Arial", 14))
        operation_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.operation_entry = ttk.Entry(self.frame, font=("Arial", 12))
        self.operation_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Inspector label and text box
        inspector_label = ctk.CTkLabel(self.frame, text="Inspector", font=("Arial", 14))
        inspector_label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

        self.inspector_entry = ttk.Entry(self.frame, font=("Arial", 12))
        self.inspector_entry.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Date label and DateEntry with today's date pre-filled
        date_label = ctk.CTkLabel(self.frame, text="Date", font=("Arial", 14))
        date_label.grid(row=3, column=2, padx=10, pady=(10, 0), sticky="w")

        # Get today's date and format it as required
        today = datetime.now()

        self.date_entry = DateEntry(self.frame, font=("Arial", 12), width=12,
                                    background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='mm/dd/yyyy')
        self.date_entry.set_date(today)  # Set today's date
        self.date_entry.grid(row=4, column=2, padx=10, pady=(0, 10), sticky="ew")  # Position for DateEntry

        # Submit button
        self.submit_button = ctk.CTkButton(self.frame, text="Submit", image=self.submit_icon,
                                            compound="left", command=self.submit_button_command,
                                            fg_color="#1E275C", text_color="white", hover_color="gray", width=150, height=50)
        self.submit_button.grid(row=5, column=2, padx=10, pady=(10, 20), sticky="se")  # Position for Submit button

        def load_image(path):
            try:
                img = Image.open(path)
                img_resized = img.resize((400, 300))  # Resize to fit the canvas
                return ImageTk.PhotoImage(img_resized)
            except Exception as e:
                print(f"Error loading image: {e}")
                return None

        # Function to handle combobox selection change
        def on_combobox_change(event):
            # Debug print to confirm the function is triggered
            print("Combobox selection changed!")

            # Get selected value
            selected_value = self.project_combobox.get()
            print(f"Selected value: {selected_value}")  # Print selected value for debugging

            if selected_value:
                # Update image path based on selection
                image_path = base_path + f"\\Project_Images\\{selected_value}.jpg"
                print(f"Loading image from: {image_path}")  # Print image path for debugging

                # Load and display the new image
                new_image = load_image(image_path)
                if new_image:  # Check if image loading was successful
                    canvas.itemconfig(canvas_image, image=new_image)
                    canvas.image = new_image  # Keep a reference to avoid garbage collection
                else:
                    print("Failed to load new image.")

        # Project label and combo box
        project_label = ctk.CTkLabel(self.frame, text="Engine Project", font=("Arial", 14))
        project_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        # List for combobox options
        #projects = ["TS1400", "PD170", "PG50", "TF6000"]
        project_list = sorted(projects)
        self.project_combobox = ttk.Combobox(self.frame, values=project_list, font=("Arial", 12))

        # Set a default initial value
        self.project_combobox.set(projects[0])  # Set to "a" initially
        self.project_combobox.bind("<<ComboboxSelected>>", on_combobox_change)
        self.project_combobox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Canvas for displaying the image
        canvas = tk.Canvas(self.frame, width=400, height=300)
        canvas.grid(row=6, column=0, columnspan=3, pady=(10, 0))

        # Load and display the initial image
        initial_image_path = base_path + f"\\Project_Images\\{projects[0]}.jpg"
        initial_image = load_image(initial_image_path)
        canvas_image = canvas.create_image(200, 150, image=initial_image)
        canvas.image = initial_image  # Keep a reference to avoid garbage collection

    def save_last_created_folder(self, folder_path):
        # last_created_folder.txt dosyasına yazma
        last_created_folder_path = os.path.join(os.path.dirname(__file__), 'data\\last_created_folder.txt')  # Dosya yolunu belirle
        with open(last_created_folder_path, 'w') as file:
            file.write(folder_path)

    def submit_button_command(self):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        report_folder = os.path.join(desktop_path, "Report")

        # "Report" klasörü yoksa oluştur
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        # Part, Operation ve Serial isimlerini al
        part_name = self.part_entry.get()
        operation_name = self.operation_entry.get()
        serial_name = self.serial_entry.get()

        # Klasör yollarını belirle
        part_folder = os.path.join(report_folder, part_name)
        serial_folder = os.path.join(part_folder, serial_name)
        operation_folder = os.path.join(serial_folder, operation_name)  # Düzenleme burada yapıldı

        # Klasörleri oluştur
        if not os.path.exists(part_folder):
            os.makedirs(part_folder)
            
        if not os.path.exists(serial_folder):
            os.makedirs(serial_folder)

        if not os.path.exists(operation_folder):
            os.makedirs(operation_folder)

            # Oluşturulan en son klasör yolunu kaydet
            global last_created_folder
            last_created_folder = operation_folder
            self.save_last_created_folder(last_created_folder)  

            messagebox.showinfo("Bilgi", f"Dosya dizini oluşturuldu: {last_created_folder}")