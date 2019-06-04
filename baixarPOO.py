from tkinter import Frame, Button, END, Tk, RIGHT, Label, LEFT, BOTTOM
from tkinter.scrolledtext import ScrolledText
from selenium import webdriver 
import time
#Por João Pedro

class App:
     def __init__(self, master=None):
             self.root = master
             self.root.title("Musicas")

             self.frame_msg = Frame(self.root)
             self.frame_msg["pady"] = 20
             self.frame_msg["padx"] = 87
             self.frame_msg.pack()

             self.frame_scroll = Frame(self.root)
             self.frame_scroll["padx"] = 5
             self.frame_scroll["pady"] = 10
             self.frame_scroll.pack()
             
             self.frame_button = Frame(self.root)
             self.frame_button["padx"] = 5
             self.frame_button["pady"] = 5
             self.frame_button.pack(side=RIGHT)

             self.msg = Label(self.frame_msg, text="Insira as músicas que deseja baixar no campo abaixo")
             self.msg["font"] = ("Arial", "14")
             self.msg.pack(side=LEFT)

             self.scrolled = ScrolledText(self.frame_scroll)
             self.scrolled.pack()

             self.button = Button(self.frame_button)
             self.button["text"] = "Ok"
             self.button["command"] = self.sair
             self.button["font"] = ("Arial", "12", "bold")
             self.button["width"] = 8
             self.button["height"] = 1 
             self.button.pack(side=RIGHT)

     def sair(self):
             with open("musicas.txt", "w") as file:
                     file.write(self.scrolled.get(1.0, END))
             self.root.destroy()

class Automacao():
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="C:/chromedriver.exe")
    
    def BuscarMusica(self, nome):
        self.nome = nome
        self.driver.get("https://www.youtube.com/results?search_query={}".format(self.nome))
        video = self.driver.find_elements_by_tag_name("ytd-video-renderer")
        tentativa = 0
        while True:
            try:
                video[tentativa].click()
                break
            except:
                tentativa +=1

        time.sleep(2)
        return self.driver.current_url

    def BaixarMusica(self, url):
        self.driver.get("https://2conv.com/pt/")
        search = self.driver.find_element_by_class_name("url-conv")
        search.send_keys(url)
        button_div = self.driver.find_element_by_class_name("button-group")
        button = button_div.find_element_by_class_name("button")
        button.click()
        while True:
            try:
                download_button_div = self.driver.find_element_by_class_name("text-center")
                download_button = download_button_div.find_element_by_class_name("button")
                download_button.click()
                break
            except:
                pass

    def Quit(self):
        self.driver.quit()


if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()
    auto = Automacao()
    with open("musicas.txt", "r") as file:
        musicas = file.readlines()

    for music in musicas:
        url = auto.BuscarMusica(nome=music)
        auto.BaixarMusica(url=url)
    auto.Quit()
