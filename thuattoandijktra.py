import tkinter as tk
from tkinter import messagebox
import networkx as nx 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

def dijkstra(dothi, nutbd, nutkt):
    khoangcach = {nut: float('inf') for nut in dothi}
    khoangcach[nutbd] = 0
    nuttruoc = {nut: None for nut in dothi}
    nutchuaden = set(dothi.nodes)
    while nutchuaden:
        nutkcminhientai = min(nutchuaden, key=lambda nut: khoangcach[nut])
        nutchuaden.remove(nutkcminhientai)
        if nutkcminhientai == nutkt:
            break  
        for ke in dothi[nutkcminhientai]:
            kctam = khoangcach[nutkcminhientai] + dothi[nutkcminhientai][ke]['weight']
            if kctam < khoangcach[ke]:
                khoangcach[ke] = kctam
                nuttruoc[ke] = nutkcminhientai
    ddnn = []
    nutkcminhientai = nutkt
    while nutkcminhientai is not None:
        ddnn.append(nutkcminhientai)
        nutkcminhientai = nuttruoc[nutkcminhientai]
    ddnn.reverse()

    return khoangcach[nutkt], ddnn

def tinh():
    try:
        if not nhapmt.get("1.0", tk.END):
            raise ValueError("Vui lòng nhập ma trận trọng số.")
        sld = int(nhapsld.get())
        if sld <= 0:
            raise ValueError("Số lượng đỉnh phải là số nguyên dương.")
        tendinh = nhaptendinh.get().split(',')
        if len(tendinh) != sld:
            raise ValueError("Số lượng tên đỉnh không khớp với số lượng đỉnh.")
        luumt = nhapmt.get("1.0", tk.END)
        mt = []
        for hang in luumt.split('\n'):
            if hang.strip():
                gthang = [int(value) for value in hang.split()]
                mt.append(gthang)
        if len(mt) != sld or any(len(hang) != sld for hang in mt):
            raise ValueError("Kích thước ma trận không hợp lệ.")
        nutbd = nhapnutbd.get()
        nutkt = nhapnutkt.get()
        if nutbd not in tendinh or nutkt not in tendinh:
            raise ValueError("Nút bắt đầu hoặc nút kết thúc không hợp lệ.")
        dothi = nx.Graph()
        for i in range(sld):
            for j in range(sld):
                if mt[i][j] != 0:
                    dothi.add_edge(tendinh[i], tendinh[j], weight=mt[i][j])
        khoang, ddnn = dijkstra(dothi, nutbd, nutkt)
        kq.delete("1.0", tk.END)
        kq.insert(tk.END, f"Khoảng cách từ {nutbd} đến {nutkt}: {khoang}\n")
        kq.insert(tk.END, f"Đường đi ngắn nhất: {ddnn}\n")
        hiendt(dothi, nutbd, nutkt, ddnn)
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))
canvas = None
def hiendt(dothi, start_node, end_node, ddnn):
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()

    
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    vtrinut = nx.spring_layout(dothi)
    nx.draw(dothi, vtrinut, with_labels=True, font_weight='bold', ax=ax)
    labels = nx.get_edge_attributes(dothi, 'weight')
    nx.draw_networkx_edge_labels(dothi, vtrinut, edge_labels=labels, ax=ax)
    canhddnn = list(zip(ddnn, ddnn[1:]))
    nx.draw_networkx_edges(dothi, vtrinut, edgelist=canhddnn, edge_color='r', width=2, ax=ax)
    nx.draw_networkx_nodes(dothi, vtrinut, nodelist=[start_node], node_color='g', node_size=500, ax=ax)
    nx.draw_networkx_nodes(dothi, vtrinut, nodelist=[end_node], node_color='b', node_size=500, ax=ax)
    canvas = FigureCanvasTkAgg(fig, master=bientk)
    canvas.draw()
    canvas.get_tk_widget().pack()
bientk = tk.Tk()
bientk.title("Mô phỏng thuật toán Dijkstra")
sld = tk.Label(bientk, text="Số lượng đỉnh:")
sld.pack()
nhapsld = tk.Entry(bientk)
nhapsld.pack()
tendinh = tk.Label(bientk, text="Tên các đỉnh (cách nhau bởi dấu phẩy):")
tendinh.pack()
nhaptendinh = tk.Entry(bientk)
nhaptendinh.pack()
matran = tk.Label(bientk, text="Ma trận trọng số (mỗi hàng cách nhau bởi dấu xuống dòng):")
matran.pack()
nhapmt = tk.Text(bientk, height=10, width=30)
nhapmt.pack()
nutbd = tk.Label(bientk, text="Nút bắt đầu:")
nutbd.pack()
nhapnutbd = tk.Entry(bientk)
nhapnutbd.pack()
nutkt = tk.Label(bientk, text="Nút kết thúc:")
nutkt.pack()
nhapnutkt = tk.Entry(bientk)
nhapnutkt.pack()
nuttinh = tk.Button(bientk, text="Tính toán", command=tinh)
nuttinh.pack()
kq = tk.Text(bientk, height=10, width=30)
kq.pack()
bientk.mainloop()
