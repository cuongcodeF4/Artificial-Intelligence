import customtkinter
import os
import numpy as np
from tkinter import *
from PIL import ImageTk, Image 
from tkinter import filedialog

from keras.models import load_model
from keras.utils.image_utils import img_to_array 
from keras.utils import load_img 




global bgr
bgr= "Dark"
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tranditional costume.py")
        self.geometry("920x520")

        # set grid layout 1x2
        #Cho phép mở rộng theo 2 hướng
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))

        self.home_bg = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bg.jpg")), size=(720, 500))

        self.large_test_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "khung.jpg")),
                                                      dark_image=Image.open(os.path.join(image_path, "khung_d.jpg")), size=(350, 440))
        self.image_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "images.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "images.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        self.result_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "targets.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "target (1).png")), size=(30, 30))
        self.rs_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "check-circle.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "check-circle (1).png")), size=(30, 30))
        
        self.load_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "loadings.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "loading.png")), size=(60, 60))
        
        self.aodai_icon  = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ad_icon.png")),  size=(50, 70))
        self.tuthan_icon = customtkinter.CTkImage(Image.open(os.path.join(image_path, "tt_icon.png")),  size=(50, 70))
        self.baba_icon   = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bb_icon.png")),  size=(50, 70))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Project final AI", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.Recogniion_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Recogniion",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.Recogniion_button_event)
        self.Recogniion_button.grid(row=2, column=0, sticky="ew")

        self.About_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="About",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.About_button_event)
        self.About_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.home_bg)
        self.home_frame_large_image_label.grid(row=0, column=0)

         # create recognition frame
        self.recognition_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.recognition_frame.grid_columnconfigure(0, weight=1)

        self.recognition_frame_large_image_label = customtkinter.CTkLabel(self.recognition_frame, text="", image=self.large_test_image)
        self.recognition_frame_large_image_label.grid(row=0, column=1, padx=0, pady=15,rowspan=20)

        self.label_result = customtkinter.CTkLabel(self.recognition_frame,image=self.result_image, text="  Kết quả:", compound="left",font=(None, 20))
        self.label_result.grid(row=20, column=1, padx=0, pady=0)


        self.recognition_frame_button_1 = customtkinter.CTkButton(self.recognition_frame, text="Load file", image=self.image_icon_image,command= self.open)
        self.recognition_frame_button_1.grid(row=15, column=2,columnspan=3, padx=20, pady=0)
        self.recognition_frame_button_2 = customtkinter.CTkButton(self.recognition_frame, text="Recognition", compound="left",command=self.recognition)
        self.recognition_frame_button_2.grid(row=16, column=2,columnspan=3, padx=20, pady=0) 
       
       
       
        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)
        
        self.label_about = customtkinter.CTkLabel(self.third_frame,text="Thông tin về trang phục truyền thống",font=("Lobster", 30),text_color="#009999")
        self.label_about.grid(row=0, column=0, padx=0, pady=10)
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.third_frame, width=615,height=270,font=("Times New Roman",16))
        self.textbox.grid(row=1, column=0, padx=(20), pady=(10), sticky="nsew")

                                                   
        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.Recogniion_button.configure(fg_color=("gray75", "gray25") if name == "Recogniion" else "transparent")
        self.About_button.configure(fg_color=("gray75", "gray25") if name == "About" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Recogniion":
            self.recognition_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.recognition_frame.grid_forget()
        if name == "About":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def Recogniion_button_event(self):
        self.select_frame_by_name("Recogniion")

    def About_button_event(self):
        self.select_frame_by_name("About")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        global bgr
        bgr = new_appearance_mode
        if new_appearance_mode == "Light":
            self.label_result.configure(text_color="blue")
        else:
            self.label_result.configure(text_color="yellow")

        

    def open(self):
        self.label_result.configure(image=self.result_image, text="  Kết quả:", compound="left",font=(None, 20))
        if bgr == "Light":
            self.label_result.configure(text_color="black")
        else:
            self.label_result.configure(text_color="white")

        global filename
        self.filename = filedialog.askopenfilename (initialdir="", title ="select A file", filetypes =(("jpg files", "*.jpg"),("all file","*.*")))
        global image
        self.image= Image.open(self.filename)
        self.image = self.image.resize((405,520))
        global my_image
        self.my_image = ImageTk.PhotoImage(self.image)
        global L1
        self.L1 = Label(self.recognition_frame, image=self.my_image)
        self.L1.grid(row=0, column=1, padx=0, pady=20,rowspan=20)
    def recognition(self):
        self.label_result.configure(image=self.load_image,text="")
        self.model = load_model('T_costume.h5')
        self.img = load_img(self.filename,target_size=(64,64))
        self.img= img_to_array(self.img)
        self.img =self.img.reshape(1,64,64,3)
        self.img = self.img.astype('float32')
        self.img = self.img /255
        self.Custom=np.argmax(self.model.predict(self.img),axis=-1)

        if (self.Custom == 0) :
            self.label_result.configure(text="  Kết quả: Áo dài", font=("Arial", 20), image=self.rs_image,text_color="yellow")
            self.label_about.configure(text="  ÁO DÀI",image=self.aodai_icon, compound="left")

            info_ad ='''
        Áo dài là trang phục truyền thống và biểu tượng của Việt Nam. Nó có một lịch sử lâu đời và được
        xem là một biểu tượng của vẻ đẹp, sự trang nhã và sự nữ tính trong văn hóa Việt Nam. Áo dài gồm 
        hai phần chính là: áo và váy. Áo dài có kiểu dáng thon dài và ôm sát cơ thể từ vai xuống gối, tạo 
        nên sự thanh lịch và duyên dáng. Váy áo dài thường rộng và dài đến mắt cá chân, tạo ra cảm giác
        trang nhã và quý phái. Áo dài thường được làm từ vải như lụa, tơ tằm hoặc vải lụa nhân tạo, với 
        các họa tiết và màu sắc phong phú. Trên áo dài thường có các chi tiết thêu, đính đá hoặc các hoa 
        văn truyền thống,mang lại vẻ đẹp tinh tế và sang trọng. Áo dài thường được mặc trong các dịp đặc
        biệt như cưới hỏi, lễ hội và sự kiện trang trọng hoặc trang phục hằng ngày. Nó đã trở thành biểu 
        tượng của phụ nữ Việt Nam, thể hiện sự kiêu sa và duyên dáng của người phụ nữ Việt. Áo dài Việt
        Nam đã trở thành biểu tượng văn hóa và là sự kết hợp hoàn hảo giữa truyền thống và hiện đại. Nó  
        là một phần quan trọng trong di sản văn hóa của Việt Nam và được trân trọng và yêu mến không chỉ
        trong nước mà còn trên toàn thế giới.'''
            self.textbox.delete("1.0", "end") 
            self.textbox.insert("0.0",info_ad)

        if (self.Custom == 1) :
            self.label_result.configure(text="  Kết quả: Áo tứ thân", font=("Arial", 20),image=self.rs_image,text_color="yellow")
            self.label_about.configure(text="  ÁO TỨ THÂN",image=self.tuthan_icon, compound="left")

            info_tt= """
            Áo tứ thân hay còn được gọi là áo ngũ thân, là một trang phục truyền thống của người Việt Nam. 
Nó có một lịch sử lâu đời và được xem như biểu tượng của truyền thống văn hóa dân tộc ta. Áo tứ thân  
gồm bốn mảnh vải riêng rẽ: áo, váy, khăn quấn đầu và khăn thắt lưng. Áo được làm từ các loại vải như 
lụa, tơ tằm hoặc vải lụa nhân tạo, thường có họa tiết và màu sắc phong phú. Áo có kiểu dáng đơn giản,
dài và ôm sát cơ thể, tạo nên vẻ đẹp trang nhã và thanh lịch.Váy áo tứ thân rộng và dài, thường được  
tạo thành từ nhiều lớp vải.Khăn đầu và khăn thắt lưng thường được làm từ cùng loại vải như áo và váy, 
và được thêu hoặc đính đá để tăng thêm vẻ đẹp. Áo tứ thân thường được mặc trong các dịp đặc biệt như
lễ hội, cưới hỏi, sự kiện truyền thống hoặc khi tham gia những hoạt động nghệ thuật quan trọng.Áo tứ 
thân là một biểu tượng quan trọng của truyền thống và là di sản văn hóa dân tộc Việt Nam, mang trong 
mình giá trị lịch sử và nghệ thuật đặc biệt. Nó đã trở thành một phần không thể thiếu trong việc duy 
trì và phát triển văn hóa dân tộc Việt Nam."""
            self.textbox.delete("1.0", "end")
            self.textbox.insert("0.0",info_tt)
        if (self.Custom == 2) :
            self.label_result.configure(text="  Kết quả: Áo bà ba", font=("Arial", 20),image=self.rs_image,text_color="yellow")
            self.label_about.configure(text="  ÁO BÀ BA",image=self.baba_icon, compound="left")

            info_bb= """
            Áo bà ba là một trang phục truyền thống đặc trưng của người phụ nữ Việt Nam, đặc biệt phổ biến 
ở miền Nam. Được xem là biểu tượng văn hóa độc đáo và mang tính chất dân tộc, áo bà ba đã trở thành  
một phần không thể thiếu trong hình ảnh truyền thống và văn hóa Việt Nam.Áo bà ba gồm ba phần chính: 
áo dài, áo yếm và váy bà ba. Áo dài là một loại áo có tay dài và ôm sát người,thường được làm từ vải  
lụa,được coi là biểu tượng của sự nữ tính và thanh lịch trong văn hóa Việt Nam.Áo yếm là một loại áo 
trùm ngực, thể hiện sự dịu dàng và tinh tế của người phụ nữ Việt. Váy bà ba có kiểu dáng xòe và rộng,
thường được làm từ vải mềm mại và nhẹ nhàng,mang lại sự thoải mái và thoải mái trong hoạt động.Trong 
quá khứ, áo bà ba thường được mặc hàng ngày bởi phụ nữ Việt Nam,đặc biệt là trong các công việc nông 
nghiệp và hàng ngày trong gia đình.Trang phục này không chỉ mang tính chất thiết thực mà còn thể hiện
sự giản dị và đẹp tự nhiên của người phụ nữ Việt Nam.Áo bà ba cũng thường được sử dụng trong các dịp 
đặc biệt như cưới hỏi,lễ hội và sự kiện văn hóa,nơi nó thể hiện sự tôn trọng và gìn giữ truyền thống
văn hóa dân tộc. gày nay, áo bà ba không chỉ được coi là một trang  phục truyền thống đơn thuần, mà 
còn là một biểu tượng của sự tự hào dân tộc và văn hóa Việt Nam.Nó thường xuất hiện trong các sự kiện 
quan trọng, từ các buổi biểu diễn nghệ thuật , các cuộc thi hoa hậu cho đến các show diễn thời trang 
quốc tế.Nhiều nhà thiết kế đã mang áo bà ba vào thế giới thời trang hiện đại, tạo nên sự kết hợp giữa
vẻ đẹp truyền thống và sự sáng tạo đương đại.Áo bà ba không chỉ có ý nghĩa về mặt thẩm mỹ và văn hóa, 
mà còn thể hiện một phần trong tư duy và tình yêu quê hương của người Việt Nam. Nó đại diện cho sự tự  
hào về nguồn gốc và truyền thống, là một biểu tượng sâu sắc của lòng yêu nước và nhân dân."""


            self.textbox.delete("1.0", "end")
            self.textbox.insert("0.0",info_bb)
        if bgr == "Light":
            self.label_result.configure(text_color="blue")
        else:
            self.label_result.configure(text_color="yellow")

if __name__ == "__main__":
    app = App()
    app.mainloop()





