import random
import math
from customtkinter import *
from PIL import Image, ImageDraw


# Начальное окно
class App(CTk):
    header = """
                                   888                                              888               
                                   888                                              888               
                                   888                                              888               
 .d8888b 888d888 888  888 88888b.  888888 .d88b.   .d88b.  888d888 8888b.  88888b.  88888b.  888  888 
d88P"    888P"   888  888 888 "88b 888   d88""88b d88P"88b 888P"      "88b 888 "88b 888 "88b 888  888 
888      888     888  888 888  888 888   888  888 888  888 888    .d888888 888  888 888  888 888  888 
Y88b.    888     Y88b 888 888 d88P Y88b. Y88..88P Y88b 888 888    888  888 888 d88P 888  888 Y88b 888 
 "Y8888P 888      "Y88888 88888P"   "Y888 "Y88P"   "Y88888 888    "Y888888 88888P"  888  888  "Y88888 
                      888 888                          888                 888                    888 
                 Y8b d88P 888                     Y8b d88P                 888               Y8b d88P 
                  "Y88P"  888                      "Y88P"                  888                "Y88P"  
 
"""

    def __init__(self):
        super().__init__()

        self.title("Шифры")
        self.geometry("640x300")
        self.resizable(width=False, height=False)
        self.after(50, self.iconbitmap('logo.ico'))
        

        label = CTkLabel(self, text=self.header, justify="left", font=("Courier", 9))

        sh_Gronsfeld = CTkButton(self, text='Шифр Гронсфельда', font=("Sans Serif", 20), command=self.open_sh_Gronsfeld, border_spacing=5)
        sh_Grille = CTkButton(self, text='Шифр решётка', font=("Sans Serif", 20), border_spacing=5, command=self.open_sh_Grille)

        label.grid(row=0, column=0, columnspan=2, padx=60, pady=30)
        sh_Gronsfeld .grid(row=1, column=0)
        sh_Grille.grid(row=1, column=1)

        self.toplevel_window = None


    def open_sh_Gronsfeld(self):
        self.toplevel_window = Gronsfeld()
        self.withdraw()


    def open_sh_Grille(self):
        self.toplevel_window = Grille()
        self.withdraw()


# Шифр Гронсфельда
class Gronsfeld(CTkToplevel):
    alphabet = [
        'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и',
        'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
        'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
        'э', 'ю', 'я'
    ]
    
    marks = [
        ' ', ',', '.', '-', ':', ';', '!', '?', '(', ')',
        '[', ']', '{', '}', '<', '>', '|', '/', '\', '#',
        '@', '&', '~', '`', '^', '*', '+', '=', '"', "'", 
        '»', '«', '„', '“', '”', '%', '№', '$'
    ]
    
    def __init__(self):
        super().__init__()
        self.title('Шифр Гронсфельда')
        self.geometry('525x420')
        self.after(200, lambda: self.iconbitmap('logo.ico'))
        self.resizable(width=False, height=False)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        f = ("Sans Serif", 16)
        f_b = ("Sans Serif", 16, 'bold')
        
        self.enc_btn = CTkButton(self, text='Зашифровать', font=f, command=self.enc_btn_click)
        self.dec_btn = CTkButton(self, text='Расшифровать', font=f, command=self.dec_btn_click)
        self.clear_btn = CTkButton(self, text='Очистить', font=f, command=self.clear_btn_click, fg_color='#008bba', hover_color='#00698d')

        self.ent_text = CTkTextbox(self, width=350, height=100, font=f)
        self.key_text = CTkTextbox(self, width=350, height=100, font=f)
        self.res_text = CTkTextbox(self, width=350, height=100, font=f)

        self.text_lbl = CTkLabel(self, text='Текст', font=f_b)
        self.key_lbl = CTkLabel(self, text='Ключ', font=f_b)
        self.enc_lbl = CTkLabel(self, text='Шифр', font=f_b)

        self.key_check = CTkCheckBox(self, text='Генерировать ключ', font=("Sans Serif", 12))
        
        self.text_lbl.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.key_lbl.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.enc_lbl.grid(row=8, column=0, padx=5, pady=5, sticky='w')

        self.ent_text.grid(row=1, column=0,  sticky='nsew', rowspan=2, padx=5)
        self.key_text.grid(row=5, column=0,  sticky='nsew', rowspan=2, padx=5)
        self.res_text.grid(row=9, column=0, padx=5)

        self.enc_btn.grid(row=1, column=1, padx=10)
        self.dec_btn.grid(row=2, column=1)
        self.clear_btn.grid(row=6, column=1, sticky='n')

        self.key_check.grid(row=5, column=1)
        
        self.bind_all("<Key>", self._onKeyRelease, "+")
    
    
    # Нажатие кнопки зашифровать
    def enc_btn_click(self):
        text = self.ent_text.get("1.0", "end-1c").lower().replace('\n', ' ')
        self.res_text.delete('1.0',END)
    
        if self.key_check.get() != 0:
            self.key_text.delete('1.0', END)

            key = self.key_generator(text)
            self.key_text.insert(END, key)
            self.res_text.insert(END, self.encrypt(key, text))
        else:
            key = self.key_text.get("1.0", "end-1c").lower().replace('\n', ' ')
            if len(text) == len(key):
                self.res_text.insert(END, self.encrypt(key, text))
            elif key != None:
                repeat = len(text) // len(key) + 1
                key_repeated= key * repeat
                key = key_repeated[:len(text)]

                self.key_text.delete('1.0', END)
                self.key_text.insert(END, key)
                self.res_text.insert(END, self.encrypt(key, text))
    
    
    # Генерация случайного ключа
    def key_generator(self, text):
        key = ''
        for char in text:
            if char not in self.marks:
                n = random.randint(1, 9)
                key += str(n)
            else:
                key += char
        return(key)


    # Шифрование
    def encrypt(self, key, text):
        enc_text = ''
        i = 0
        for char in text:
            if char not in self.marks:
                letter_num = self.alphabet.index(char)
                enc_num = int(key[i]) + letter_num

                if enc_num > len(self.alphabet) - 1:
                    enc_text += self.alphabet[enc_num - len(self.alphabet)]
                else:
                    enc_text += self.alphabet[enc_num]
            else:
                enc_text += char 
            i += 1
        return(enc_text)


    # Расшифрование
    def decipher(self, key, text):
        dec_text = ''
        i = 0
        for char in text:
            if char not in self.marks:
                letter_num = self.alphabet.index(char)
                dec_num = letter_num - int(key[i])
                if dec_num >= 0:
                    dec_text += self.alphabet[dec_num]
                else:
                    dec_text += self.alphabet[len(self.alphabet) + dec_num]
            else:
                dec_text += char
            i += 1
        return(dec_text)
    
    
    # Нажатие кнопки расшифровать
    def dec_btn_click(self):
        self.ent_text.delete('1.0', END)

        key = self.key_text.get("1.0", "end-1c").replace('\n', ' ')
        text = self.res_text.get("1.0", "end-1c").replace('\n', ' ')
        self.ent_text.insert(END, self.decipher(key, text))
    
    
    # Очистка text
    def clear_btn_click(self):
        self.key_text.delete('1.0', END)
        self.res_text.delete('1.0',END)
        self.ent_text.delete('1.0', END)
    
    
    # Комбинации клавиш на русской раскладке
    def _onKeyRelease(self, event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")
    
        if event.keycode == 65 and ctrl:
            event.widget.tag_add("sel", "1.0", "end")
    
    
    # Закрыть окно
    def on_close(self):
        self.destroy()
        self.master.deiconify()


# Шифр решетки
class Grille(CTkToplevel):
    key = []

    def __init__(self):
        super().__init__()
        self.title('Шифр решётки')
        self.geometry('760x290')
        self.after(200, lambda: self.iconbitmap('logo.ico'))
        self.resizable(width=False, height=False)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        f = ("Sans Serif", 16)
        f_b = ("Sans Serif", 16, 'bold')
        
        self.bind_all("<Key>", self._onKeyRelease, "+")

        self.text_lbl = CTkLabel(self, text='Текст', font=f_b)
        self.enc_lbl = CTkLabel(self, text='Шифр', font=f_b)
        self.key_lbl = CTkLabel(self, text='Ключ', font=f_b)

        self.ent_text = CTkTextbox(self, width=350, height=100, font=f)
        self.res_text = CTkTextbox(self, width=350, height=100, font=f)

        self.enc_btn = CTkButton(self, text='Зашифровать', font=f, command=self.enc_btn_click)
        self.dec_btn = CTkButton(self, text='Расшифровать', font=f, command=self.dec_btn_click)
        self.key_btn = CTkButton(self, text='Ключ', font=f, command=self.key_btn_click)
        self.clear_btn = CTkButton(self, text='Очистить', font=f, fg_color='#008bba', hover_color='#00698d', command=self.clear_btn_click)

        self.image = CTkImage(dark_image=Image.open("block.png"), size=(235, 235))
        self.image_lbl = CTkLabel(self, image=self.image, text="")
        
        self.text_lbl.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=3)
        self.enc_lbl.grid(row=3, column=0, padx=5, pady=5, sticky='w', columnspan=3)
        self.key_lbl.grid(row=0, column=4,  padx=5, pady=5, sticky='w')

        self.image_lbl.grid(row=1, column=4, sticky='nsew', rowspan=5,  padx=5)
         
        self.ent_text.grid(row=1, column=0,  sticky='nsew', rowspan=2, padx=5, columnspan=3)
        self.res_text.grid(row=4, column=0,  sticky='nsew', rowspan=2, padx=5, columnspan=3)

        self.enc_btn.grid(row=1, column=5, padx=5, pady=4)
        self.dec_btn.grid(row=2, column=5, padx=5, pady=4)
        self.key_btn.grid(row=3, column=5, padx=5, pady=9)
        self.clear_btn.grid(row=5, column=5, padx=5)


    # Нажатие кнопки расшифровать
    def dec_btn_click(self):
        enc_text = self.res_text.get("1.0", "end-1c").lower().replace('\n', ' ')
        self.ent_text.delete('1.0',END)
        self.ent_text.insert(END, self.decipher(self.key, enc_text))

    # Нажатие кнопки зашифровать
    def enc_btn_click(self):
        text = self.ent_text.get("1.0", "end-1c").lower().replace('\n', ' ')
        self.res_text.delete('1.0',END)
        self.res_text.insert(END, self.encrypt(self.key, text))


    # Нажатие кнопки ключ
    def key_btn_click(self):
        text = self.ent_text.get("1.0", "end-1c").lower().replace('\n', ' ')
        self.key = self.key_generator(text)
        self.draw_table(self.key)

        self.image = CTkImage(dark_image=Image.open("table.png"), size=(235, 235))
        self.image_lbl = CTkLabel(self, image=self.image, text="")

        self.image_lbl.grid(row=1, column=4, sticky='nsew', rowspan=5,  padx=5)


    # Нажатие кнопки очистить
    def clear_btn_click(self):
        self.res_text.delete('1.0',END)
        self.ent_text.delete('1.0', END)

        self.image = CTkImage(dark_image=Image.open("block.png"), size=(235, 235))
        self.image_lbl = CTkLabel(self, image=self.image, text="")

        self.image_lbl.grid(row=1, column=4, sticky='nsew', rowspan=5,  padx=5)

        self.key = []


    # Рисование ключа
    @staticmethod
    def draw_table(block):
        size = len(block)
        min_cell_size = 20
        cell_size = max(min_cell_size, 800 // size)  
        image_size = size * cell_size

        img = Image.new('RGB', (image_size, image_size), color='#3B3B3B')
        draw = ImageDraw.Draw(img)

        # Ячейки таблицы
        for i in range(size):
            for j in range(size):
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                
                draw.rectangle([x0, y0, x1, y1], outline='white')

                if block[i][j] == 1:
                    draw.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill='#171717') 

        img.save('table.png')
        # img.show()


    # Генерация ключа
    def key_generator(self, text):
        table_length = math.ceil(math.sqrt(len(text)))

        # Округление
        if table_length % 2 != 0:
            table_length += 1
        
        table_size = table_length ** 2

        block_size = table_size / 4
        block_size = int(block_size)

        table_block = []
        for i in range(block_size):
            table_block.append(i)

        # Кол-во окон в 1 области 
        block_1 = random.randint(1, block_size // 2 + 1)
        if block_1 != 0:
            if block_1 % 2 != 0:
                block_1 -= 1
        
        # Кол-во окон во 2 области
        block_2 = random.randint(1, block_size - block_1 + 1)
        if block_1 != 0:
            if block_2 % 2 != 0:
                block_2 -= 1
        
        # Кол-во окон в 3 области
        N = block_size - block_1 - block_2 + 1
        if N > 1:
            block_3 = random.randint(1, N)
            if block_3 != 0:
                if block_3 % 2 != 0:
                    block_3 -= 1
        else:
            block_3 = 0
        
        # Кол-во окон в 4 области
        block_4 = block_size - block_1 - block_2 - block_3
        if block_4 < 0:
            block_4 = 0

        # print(block_1, block_2, block_3, block_4)

        key = []
        for i in range(int(table_length)):
            key.append([0] * int(table_length))
        block = []
        block = self.clear_block(table_length)
        key_n = []

        # Заполнение 1 блока в ключе
        if block_1 != 0:
            for i in range(block_1):
                k = random.choice(table_block)
                key_n.append(k)
                table_block.remove(k)
            key_n.sort()
            # print(f'block 1 {key_n}')

            block = self.block_fill(table_length, block, key_n)
            key_n.clear()

            # Добавление в ключ
            for i in range(table_length // 2):
                for j in range(table_length // 2):
                    key[i][j] = block[i][j]
            block = self.clear_block(table_length)

        # Заполнение 2 блока в ключе
        if block_2 != 0:
            for i in range(block_2):
                if table_block:
                    k = random.choice(table_block)
                    key_n.append(k)
                    table_block.remove(k)
            key_n.sort()
            # print(f'block 2 {key_n}')
        
            block = self.block_fill(table_length, block, key_n)
            key_n.clear()
        
            # Поворот блока на 90 градусов и добавление в ключ
            block = [list(row) for row in zip(*block[::-1])]

            for i in range(table_length // 2):
                for j in range(table_length // 2, table_length):
                    key[i][j] = block[i][j - table_length // 2]
            block = self.clear_block(table_length)

        # Заполнение 3 блока в ключе
        if block_3 != 0:
            for i in range(block_3):
                if table_block:
                    k = random.choice(table_block)
                    key_n.append(k)
                    table_block.remove(k)
            key_n.sort()
            # print(f'block 3 {key_n}')

            block = self.block_fill(table_length, block, key_n)
            key_n.clear()

            # Поворот блока на 180 градусов и добавление в ключ
            block = [row[::-1] for row in reversed(block)]

            for i in range(table_length // 2, table_length):
                for j in range(table_length // 2, table_length):
                    key[i][j] = block[i - table_length // 2][j - table_length // 2]
            block = self.clear_block(table_length)

        # Заполнение 4 блока в ключе
        if block_4 != 0:
            for i in range(block_4):
                if table_block:
                    k = random.choice(table_block)
                    key_n.append(k)
                    table_block.remove(k)
            key_n.sort()
            # print(f'block 4 {key_n}')

            block = self.block_fill(table_length, block, key_n)
            key_n.clear()
        
            # Поворот блока на 270 градусов и добавление в ключ
            block = [row[::-1] for row in reversed(block)]
            block = [list(row) for row in zip(*block[::-1])]

            for i in range(table_length // 2, table_length):
                for j in range(table_length // 2):
                    key[i][j] = block[i - table_length // 2][j - table_length // 2]
            block = self.clear_block(table_length)

        print()
        for i in range(int(table_length)):
            print(key[i])
        
        return key


    # Шифрование
    def encrypt(self, key, text):
        table_length = math.ceil(math.sqrt(len(text)))

        if table_length % 2 != 0:
            table_length += 1

        # Добавление пробелов в конец текста
        if table_length ** 2 != len(text):
            for i in range(table_length * 2 - len(text), table_length * 2):
                text += ' '
        
        block = []
        block = self.clear_block(table_length * 2)
        enc_text = ''
        k = 0

        for _ in range(4):
            for i in range(table_length):
                for j in range(table_length):
                    if key[i][j] == 1:
                        block[i][j] = text[k]
                        k += 1
            key = [list(row) for row in zip(*key[::-1])]

        # Форматированный вывод блока
        print('')
        formatted_block = '\n'.join([' '.join(map(str, row)) for row in block])
        print(formatted_block)
        
        for row in block:
            enc_text += ''.join(map(str, row))

        return(enc_text)


    # Расшифрование
    def decipher(self, key, enc_text):
        table_length = math.ceil(math.sqrt(len(enc_text)))

        if table_length % 2 != 0:
            table_length += 1

        # Добавление пробелов в конец текста
        if table_length * 2 != len(enc_text):
            for i in range(table_length * 2 - len(enc_text), table_length * 2):
                enc_text += ' '
    
        text = ''
        k = 0
        block = []
        block = self.clear_block(table_length * 2)

        for i in range(table_length):
            for j in range(table_length):
                block[i][j] = enc_text[k]
                k += 1

        for _ in range(4):
            for i in range(table_length):
                for j in range(table_length):
                    if key[i][j] == 1:
                        text += block[i][j]
            key = [list(row) for row in zip(*key[::-1])]
        

        print(text)
        return text
    

    # Очистка блока
    @staticmethod
    def clear_block(table_length):
        block = []
        for i in range(table_length // 2):
            block_row = []
            for j in range(table_length // 2):
                block_row.append(0)
            block.append(block_row)
        return(block)
    

    # Заполнение блока
    @staticmethod
    def block_fill(table_length, block, key_n):
        for i in range(table_length // 2):
            for j in range(table_length // 2):
                if j in key_n:
                    # print(f'{j} and {key_n}')
                    block[i][j] = 1
                    key_n[key_n.index(j)] = 100000
            for x in range(len(key_n)):
                if key_n[x] > 0:
                    key_n[x] = key_n[x] - table_length // 2
                if key_n[x] < 0:
                        key_n[x] = 100000
        return(block)


    # Комбинации клавиш на русской раскладке
    def _onKeyRelease(self, event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")
    
        if event.keycode == 65 and ctrl:
            event.widget.tag_add("sel", "1.0", "end")


    # Закрыть окно
    def on_close(self):
        self.destroy()
        self.master.deiconify()


set_appearance_mode('dark')
set_default_color_theme('green')    

app = App()
app.mainloop()
