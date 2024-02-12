import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd

# Define global variables
csv_file_path = "E:/card_ocr/MAHEDI_DS/first.csv"
image_folder_path = "E:/card_ocr/MAHEDI_DS/2000"
df = pd.read_csv(csv_file_path)
image_references = {}  # Dictionary to hold references to images

# Function to display image and annotation text
def display_image_and_annotation(image_path, annotation):
    image = Image.open(image_path)
    image.thumbnail((300, 300))  # Adjust size as needed
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
    annotation_label.config(text=annotation)

# Function to update annotation in CSV file
def update_annotation(file_name, new_annotation):
    global df
    df.loc[df['filename'] == file_name, 'words'] = new_annotation
    df.to_csv(csv_file_path, index=False)

def update_annotation_command():
    if tree_selection:
        new_annotation = new_annotation_entry.get()
        selected_file_name = tree.item(tree_selection, 'text')
        update_annotation(selected_file_name, new_annotation)
        success_label.config(text="Annotation Updated Successfully!")
        success_label.after(3000, clear_success_message)  # Clear success message after 3 seconds
    else:
        messagebox.showerror("Error", "Please select a file.")

def clear_success_message():
    success_label.config(text="")

def on_select(event):
    global tree_selection
    item = tree.focus()
    if item:
        tree_selection = item
        selected_file_name = tree.item(item, 'text')
        selected_row = df[df['filename'] == selected_file_name]
        selected_annotation = selected_row['words'].values[0]
        selected_image_path = f"{image_folder_path}/{selected_file_name}"
        display_image_and_annotation(selected_image_path, selected_annotation)

def main():
    global tree, tree_selection, image_label, annotation_label
    root = tk.Tk()
    root.title("Annotation Recheck App")

    # Frame for image display
    image_frame = tk.Frame(root)
    image_frame.pack()

    # Display image and annotation
    image_label = tk.Label(image_frame)
    image_label.pack()
    annotation_label = tk.Label(image_frame, wraplength=300)  # Adjust wrap length as needed
    annotation_label.pack()

    # Treeview for displaying images, annotations, and editing
    tree = ttk.Treeview(root, columns=("Image", "Annotation", "Edit"), show="headings", selectmode="browse")
    tree.heading("Image", text="Image")
    tree.heading("Annotation", text="Annotation")
    tree.heading("Edit", text="Edit")
    tree.pack(side=tk.LEFT, fill=tk.Y)

    # Populate treeview with data
    for filename in df['filename']:
        image_path = f"{image_folder_path}/{filename}"
        image = Image.open(image_path)
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)
        annotation = df[df['filename'] == filename]['words'].values[0]
        item = tree.insert("", "end", text=filename, values=(photo, annotation, ""))
        image_references[item] = photo  # Store reference to the photo

    # Bind event for selecting a row
    tree.bind("<<TreeviewSelect>>", on_select)

    # User input for annotation correction
    new_annotation_label = tk.Label(root, text="Edit Annotation:")
    new_annotation_label.pack()
    global new_annotation_entry
    new_annotation_entry = tk.Entry(root)
    new_annotation_entry.pack()

    # Update button
    update_button = tk.Button(root, text="Update Annotation", command=update_annotation_command)
    update_button.pack()

    # Success message label
    global success_label
    success_label = tk.Label(root, fg="green")
    success_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()