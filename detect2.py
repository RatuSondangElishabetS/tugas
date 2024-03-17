import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Function to resize the image
def resize_image(image, target_width=1000):
    scale_percent = target_width / image.shape[1] * 100
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Function to detect and segment object
def detect_and_segment_object(image_path, target_width=1000, has_damages=True):

    # Menginput gambar dari file
    image = cv2.imread(image_path)
    if image is None:
        print("Gambar tidak dapat dibuka. Pastikan path gambar benar.")
        return

    resized_image = resize_image(image, target_width)

    #mendeteksi objek berdasarkan warna merah, kuning atau orange dalam gambar menggunakan representasi warna HSV (Hue, Saturation, Value)
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

    # Define HSV color range for hot (red, yellow, and orange)
    lower_red = np.array([0, 100, 100])  # red
    upper_red = np.array([30, 255, 255])

    lower_yellow = np.array([20, 100, 100])  # yellow approaching white
    upper_yellow = np.array([40, 50, 255])

    lower_orange = np.array([10, 100, 100])  # orange
    upper_orange = np.array([20, 255, 255])

    # Create masks for each color range
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # Combine masks using bitwise OR operation
    hot_mask = cv2.bitwise_or(yellow_mask, orange_mask)
    hot_mask = cv2.bitwise_or(red_mask, hot_mask)

    # Find contours in the combined mask
    contours, _ = cv2.findContours(hot_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Membuat mask untuk area panas
    hot_mask_image = np.zeros_like(resized_image)

    # Hitung jumlah kerusakan yang terdeteksi berdasarkan kontur
    num_damages = len(contours)

    # Iterasi melalui kontur dan perbarui mask
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.drawContours(hot_mask_image, [contour], -1, (0, 0, 255), thickness=cv2.FILLED)

        # Informasi deteksi gangguan pada bagian yang ditandai panas
        if has_damages:
            cv2.putText(hot_mask_image, "Kabel Panas", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            print("Terdeteksi terdapat kerusakan. Lokasi:", (x, y-10), "Size:", (w, h))

    # Menghasilkan gambar dengan deteksi tepi pada area piksel-piksel berwarna panas (merah, kuning atau orange)
    hot_area_edges = cv2.Canny(hot_mask_image, 100, 200)

    # Print the total number of damages
    print("Deteksi Kabel dengan metode HSV (Panas):", "Ya" if has_damages else "Tidak")

    # Menampilkan gambar menggunakan Matplotlib
    plt.figure(figsize=(16, 6))

    # Menampilkan Gambar Asli
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Gambar Asli')
    plt.axis('off')

    # Menampilkan Gambar dengan deteksi tepi pada area panas
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(hot_mask_image, cv2.COLOR_BGR2RGB))
    plt.title('Area Panas (Merah)')
    plt.axis('off')

    # Menampilkan Gambar dengan area panas
    plt.subplot(1, 3, 3)
    plt.imshow(hot_area_edges, cmap='gray')
    plt.title('Deteksi Tepi pada Area Panas')
    plt.axis('off')

    # Print the total number of damages
    print(f"Total deteksi Kabel dengan metode HSV (Panas):", num_damages)

    # Display the result
    plt.show()

# Membuat fungsi untuk memilih gambar dari folder
def browse_image():
    file_path = filedialog.askopenfilename(initialdir="/", title="Pilih Gambar", filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
    if file_path:
        detect_and_segment_object(file_path, has_damages=True)

# Membuat GUI dengan Tkinter
root = tk.Tk()
root.title("Deteksi Kabel")
root.geometry("300x100")

browse_button = tk.Button(root, text="Pilih Gambar", command=browse_image)
browse_button.pack(pady=20)

root.mainloop()
