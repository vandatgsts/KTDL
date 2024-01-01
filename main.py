import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import matplotlib
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data_processing as dp  # đảm bảo rằng data_processing.py ở cùng thư mục

matplotlib.use("TkAgg")

file_path = None  # Lưu đường dẫn file được kéo vào
# Hàm xử lý sự kiện khi có sự thay đổi trong việc kéo và thả file
def on_drop(event):
    global file_path
    file_path = event.data
    label_file_path.config(text=f"Đường dẫn file: {file_path}")


# Biến toàn cục để lưu trữ kết quả Apriori
apriori_results = None


def export_to_excel():
    global apriori_results
    if apriori_results is not None:
        # Yêu cầu người dùng chọn vị trí lưu file
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        if filepath:
            # Xuất DataFrame ra Excel
            messagebox.showinfo("Thông báo", "Xuất file Excel thành công!")
    else:
        messagebox.showwarning("Cảnh báo", "Không có kết quả để xuất!")


# Hàm hiển thị luật kết hợp dưới dạng bảng
def display_association_rules():
    global apriori_results
    try:
        df = dp.load_data(filepath=file_path)
        transactions = df.groupby(['Member_number', 'Date'])['itemDescription'].apply(list)
        results = dp.get_association_rules(transactions.values.tolist())

        # Chuyển đổi kết quả thành DataFrame
        apriori_results = pd.DataFrame(results,
                                       columns=["Left Hand Side", "Right Hand Side", "Support", "Confidence", "Lift"])

        # Xóa bảng cũ nếu có
        for i in tree.get_children():
            tree.delete(i)

        # Điền dữ liệu vào bảng
        for row in apriori_results.itertuples():
            tree.insert("", "end", values=row[1:])  # Chú ý rằng row[0] là index mà pandas tự động thêm vào
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Hàm hiển thị biểu đồ
def show_chart():
    try:
        df = dp.load_data(filepath=file_path)
        fig = dp.draw_chart(df)
        chart_window = tk.Toplevel(window)
        chart_window.title("Biểu đồ sản phẩm phổ biến")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Tạo cửa sổ chính
window = TkinterDnD.Tk()
window.title("Ứng dụng Phân Tích Dữ Liệu")

# Tạo Label
label = ttk.Label(window, text="Kéo dữ liệu vào đây hoặc sử dụng các chức năng:")
label.pack(side='top', pady=10, anchor='n')

# Tạo khung để kéo và thả file
frame_drag_drop = ttk.Frame(window, width=150, height=150, relief=tk.RAISED, borderwidth=2)
frame_drag_drop.pack(side='top', pady=20, expand=True, anchor='n')
frame_drag_drop.pack_propagate(False)

# Tạo biểu tượng (icon) cho việc kéo và thả file
icon_path = "img.png"  # Adjust the path to your icon
icon_image = PhotoImage(file=icon_path)
icon_image = icon_image.subsample(6, 6)  # Resize the image

# Label để hiển thị biểu tượng và xử lý sự kiện kéo và thả
label_file_drag_drop = ttk.Label(frame_drag_drop, image=icon_image, relief=tk.SUNKEN, anchor='center')
label_file_drag_drop.image = icon_image
label_file_drag_drop.pack(expand=True, fill='both')

# Đăng ký sự kiện kéo và thả và xử lý sự kiện
label_file_drag_drop.drop_target_register(DND_FILES)
label_file_drag_drop.dnd_bind('<<Drop>>', on_drop)

label_file_path = ttk.Label(window, text="")
label_file_path.pack(pady=10)
# Khung để chứa các nút
buttons_frame = ttk.Frame(window)
buttons_frame.pack(side='top', pady=10)

# Tạo button hiển thị luật kết hợp
display_rules_button = ttk.Button(buttons_frame, text="Hiển thị luật kết hợp", command=display_association_rules)
display_rules_button.pack(side='left', padx=10)

# Tạo button hiển thị biểu đồ
chart_button = ttk.Button(buttons_frame, text="Hiển thị biểu đồ", command=show_chart)
chart_button.pack(side='left', padx=10)

export_excel_button = ttk.Button(buttons_frame, text="Xuất Excel", command=export_to_excel)
export_excel_button.pack(side='left', padx=10)

# Khung để hiển thị kết quả dạng bảng có thể scroll được

results_frame = ttk.Frame(window)
results_frame.pack(side='top', fill='both', expand=True)

# Tạo bảng kết quả
tree = ttk.Treeview(results_frame, columns=("Left Hand Side", "Right Hand Side", "Support", "Confidence", "Lift"),
                    show='headings')
tree.heading("Left Hand Side", text="Left Hand Side")
tree.heading("Right Hand Side", text="Right Hand Side")
tree.heading("Support", text="Support")
tree.heading("Confidence", text="Confidence")
tree.heading("Lift", text="Lift")
tree.pack(side='left', fill='both', expand=True)

# Thêm thanh cuộn cho bảng
scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.configure(yscrollcommand=scrollbar.set)

window.mainloop()
