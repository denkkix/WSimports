import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Cria uma imagem manualmente
def criar_imagem_teste():
    img = Image.new("RGBA", (300, 300), (255, 255, 255, 0))  # Fundo transparente
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 50, 250, 250), fill=(0, 100, 200, 100))  # Círculo azul com opacidade
    return img

class TesteImagem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Teste com Imagem Gerada")
        self.geometry("600x400")

        # Frame para simular aba
        frame = tk.Frame(self, bg="white")
        frame.pack(expand=True, fill="both")

        # Cria imagem e converte para PhotoImage
        img = criar_imagem_teste()
        self.logo_img = ImageTk.PhotoImage(img)

        # Label com imagem
        label = tk.Label(frame, image=self.logo_img, bg="white")
        label.place(relx=0.5, rely=0.5, anchor="center")
        label.lower()  # Joga pro fundo

app = TesteImagem()
app.mainloop()
