# https://www.tra-loi-cau-hoi-phat-trien-web.com/vi/python/tkinter-cach-su-dung-cac-luong-de-ngan-vong-lap-su-kien-chinh-khoi-dong-bang/1073497675/
#https://stackoverflow.com/questions/10847626/program-freezing-during-the-execution-of-a-function-in-tkinter
import sys
import time
from tkinter.ttk import *
import tkinter
import tkinter.messagebox
from tkinter.messagebox import showinfo
from tkinter import PhotoImage, filedialog as fd
from matplotlib.ft2font import HORIZONTAL
from tkintermapview import TkinterMapView
from main2opt import *


class App(tkinter.Tk):

    APP_NAME = "2-OPT"
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        
        # self.resizable(False, False)
        
        # Căn giữa màn hình
        self.update_idletasks()
        width= self.winfo_width()
        height= self.winfo_height()
        x=(self.winfo_screenwidth()//2)-(width//2)
        y=(self.winfo_screenheight()//2)-(height//2)
        self.geometry('{}x{}+{}+{}'.format(width,height,x,y))

        # img=PhotoImage(file='map.png')
        # self.iconphoto(False,img)
        # self.iconbitmap(r"map.ico")
        self.configure(background="gray")
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Return>", self.search)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.search_bar = tkinter.Entry(self, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tkinter.Button(master=self, width=8, text="Tìm kiếm", command=self.search)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tkinter.Button(master=self, width=8, text="Clear", command=self.clear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

        self.listbox_button_frame = tkinter.Frame(master=self)
        self.listbox_button_frame.grid(row=2, column=1, sticky="nsew", columnspan=2)

        self.listbox_button_frame.grid_columnconfigure(0, weight=1)

        self.save_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="Thêm địa chỉ",command=self.save_marker)
        self.save_marker_button.grid(row=0, column=0, pady=5, padx=10)

        self.clear_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="Xóa list marker",command=self.clear_all)
        self.clear_marker_button.grid(row=1, column=0, pady=5, padx=10)

        self.connect_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="Open file data",command=self.select_file)
        self.connect_marker_button.grid(row=2, column=0, pady=5, padx=10)
        
        self.connect_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="Display map",command=self.Display_map)
        self.connect_marker_button.grid(row=3, column=0, pady=5, padx=10)

        self.map_widget.set_address("Hồ Chí Minh")

        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False
        
        self.filename=None   
        self.points=[]
        
    def start_loading(self):
        pass
    
    def search(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False
            
    def save_marker(self):
        if self.search_marker is not None:
            if len(self.points)>1:
                self.clear_marker_list()
                # f" {len(self.marker_list)}. {self.search_marker.text} "
                self.marker_list_box.insert(tkinter.END)
                self.marker_list_box.see(tkinter.END)
                self.marker_list.append(self.search_marker)
                # print(self.search_marker.position)
                self.points.append(self.search_marker.position)
                # print(self.points)
                self.connect_marker()
                self.Display_map()
            else:
                self.marker_list_box.insert(tkinter.END,f" {len(self.marker_list)}. {self.search_marker.text} ")
                self.marker_list_box.see(tkinter.END)
                self.marker_list.append(self.search_marker)
                # print(self.search_marker.position)
                self.points.append(self.search_marker.position)
                self.map_widget.set_polygon(self.points)

    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        
        # self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        # self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
        # self.map_widget.set_address("Hồ Chí Minh")

    def clear_all(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        
        self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.map_widget.set_address("Hồ Chí Minh")
        self.points=[]
        self.route=[]
        self.diachireal=[]
        
        tkinter.messagebox.showinfo("Message", "Xóa toàn bộ dữ liệu thành công!")


        # self.connect_marker()

    def connect_marker(self):
        tkinter.messagebox.showinfo("Message", "Tải dữ liệu lên")
        # self.start_loading()
        self.route=main_xuli(self.points)
        self.diachireal=diachi(self.route)
        tkinter.messagebox.showinfo("Message", "Hoàn tất tải dữ liệu")
        


    def Display_map(self):
        if (len(self.points)!=0):
            self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
            self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
            self.map_widget.set_address("Hồ Chí Minh")

            for i in range(len(self.route)):
                if (i==len(self.route)-1):
                    break
                self.map_widget.set_position(self.route[i][0],self.route[i][1],marker=True,text=str(i+1))
                self.marker_list_box.insert(tkinter.END, f" {i+1}. {self.diachireal[i]} ")
                self.marker_list_box.see(tkinter.END)
            self.map_widget.set_polygon(self.route)
        else:
            tkinter.messagebox.showerror("Message","Không có dữ liệu để hiển thị Map")
        
    def select_file(self):
        filetypes = (('text files', '*.txt'),('All files', '*.*'))

        filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)

        # showinfo(title='Selected File',message=filename)
        self.filename=filename
        if (self.filename!=""):
            self.points=read_point(self.filename)
            self.connect_marker()
        else:
            tkinter.messagebox.showerror("Message", "Kết nối thất bại!")

    
    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
