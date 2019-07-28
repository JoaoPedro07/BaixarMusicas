from __future__ import unicode_literals
from tkinter import Frame, Button, END, Tk, RIGHT, Label, LEFT, BOTTOM
from tkinter.scrolledtext import ScrolledText 
import time
import os
#Por João Pedro
try:
    import youtube_dl
except:
    os.system("pip install youtube-dl")
try:
    from selenium import webdriver
except:
    os.sytem("pip install selenium")

class App:
     def __init__(self, master=None):
             self.root = master
             self.root.title("Musicas")
             self.root.geometry("230x260")

             self.frame = Frame(self.root)

             self.msg = Label(self.frame, text="Insira as músicas que \ndeseja baixar no \ncampo abaixo")
             self.msg["font"] = ("Arial", "10")
             self.msg.grid(row=1, column=1)

             self.scrolled = ScrolledText(self.frame, width=25, height=10)
             self.scrolled.grid(row=2, column=1)

             self.button = Button(self.frame)
             self.button["text"] = "Enviar"
             self.button["command"] = self.sair
             self.button["font"] = ("Arial", "12")
             self.button["width"] = 5
             self.button["height"] = 1 
             self.button.grid(row=3, column=1)

             self.frame.pack()

     def sair(self):
             with open("musicas.txt", "w") as file:
                     file.write(self.scrolled.get(1.0, END))
             self.root.destroy()

class Automacao():
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
    
    def BuscarMusica(self, nome):
        self.nome = nome
        self.driver.get("https://www.youtube.com/results?search_query={}".format(self.nome))
        time.sleep(1)
        video_div = self.driver.find_elements_by_id("contents")
        time.sleep(1)
        video_div[0].find_elements_by_id("dismissable")[0].click()
        time.sleep(1)
        return self.driver.current_url

    def BaixarMusica(self, url):
        self.driver.get("https://www.youtube.com/")
        self.url = url
        print(self.nome)
        outtmpl = self.nome + '.mp3'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
                'preferredquality': '192',
                },
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([str(self.url)])

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
        print(music)
        url = auto.BuscarMusica(nome=music.strip("'\n'"))
        auto.BaixarMusica(url=url)
    auto.Quit()
