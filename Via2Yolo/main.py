import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from via2yolo import extract_dimension, extract_bbox, normalize_bbox
from utils import create_dir

class ViaToYoloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VIA to YOLO Converter")
        
        # Labels and Entry for Image Directory
        tk.Label(root, text="Image Folder:").grid(row=0, column=0, sticky=tk.W)
        self.image_dir_entry = tk.Entry(root, width=50)
        self.image_dir_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.select_image_folder).grid(row=0, column=2)

        # Labels and Entry for VIA Project File
        tk.Label(root, text="VIA Project File:").grid(row=1, column=0, sticky=tk.W)
        self.via_project_entry = tk.Entry(root, width=50)
        self.via_project_entry.grid(row=1, column=1)
        tk.Button(root, text="Browse", command=self.select_via_project).grid(row=1, column=2)

        # Labels and Entry for Image Format
        tk.Label(root, text="Image Formats (comma seperate. default .jpg, .png):").grid(row=2, column=0, sticky=tk.W)
        self.image_format_entry = tk.Entry(root, width=50)
        self.image_format_entry.grid(row=2, column=1)

        # Convert Button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_via_to_yolo)
        self.convert_button.grid(row=3, column=1, pady=10)

    def select_image_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.image_dir_entry.delete(0, tk.END)
            self.image_dir_entry.insert(0, folder)

    def select_via_project(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            self.via_project_entry.delete(0, tk.END)
            self.via_project_entry.insert(0, file)

    def convert_via_to_yolo(self):
        image_dir = self.image_dir_entry.get()
        via_project_path = self.via_project_entry.get()
        image_format_input = self.image_format_entry.get()

        # Validate input for image directory and VIA project file
        if not image_dir or not via_project_path:
            messagebox.showwarning("Input Required", "Please select both image folder and VIA project file.")
            return

        # Set default formats if no input is provided, else parse the input
        if not image_format_input.strip():
            image_format = ['.jpg', '.png']
        else:
            # Parse the image format input from user
            image_format = [fmt.strip() for fmt in image_format_input.split(",") if fmt.strip()]

        # Set up base directory and output label directory
        label_folder_name = 'labels'
        base_dir = Path(image_dir).parent
        label_dir = create_dir(base_dir, label_folder_name)

        # Perform conversion
        dimensions = extract_dimension(image_dir, image_format)
        image_bboxs_dict = extract_bbox(via_project_path)
        normalize_bbox(image_bboxs_dict, dimensions, label_dir)
        
        # Notify user of successful conversion
        messagebox.showinfo("Conversion Complete", f"YOLO format .txt files have been saved in:\n{label_dir}")


# Set up Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    app = ViaToYoloApp(root)
    root.mainloop()
