from customtkinter import *
import binascii


class App(CTk):
    def __init__(self):
        super().__init__()

        self.title('Шифр Магма')
        self.geometry('525x420')
        self.after(200, lambda: self.iconbitmap('logo.ico'))
        self.resizable(width=False, height=False)
        
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
        
        self.text_lbl.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.key_lbl.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.enc_lbl.grid(row=8, column=0, padx=5, pady=5, sticky='w')

        self.ent_text.grid(row=1, column=0,  sticky='nsew', rowspan=2, padx=5)
        self.key_text.grid(row=5, column=0,  sticky='nsew', rowspan=2, padx=5)
        self.res_text.grid(row=9, column=0, padx=5)

        self.enc_btn.grid(row=1, column=1, padx=10)
        self.dec_btn.grid(row=2, column=1)
        self.clear_btn.grid(row=5, column=1, sticky='n')
        
        self.bind_all("<Key>", self._onKeyRelease, "+")


    # Нажатие кнопки зашифровать
    def enc_btn_click(self):
        text = self.ent_text.get("1.0", "end-1c").lower().replace('\n', ' ')
        self.res_text.delete('1.0',END)
        key = self.key_text.get("1.0", "end-1c").lower().replace('\n', ' ')

        
        if len(key) > 0:
            textEncrypt = self.encrypt(text, key)
            self.res_text.insert(END, textEncrypt)
        else:
            print('ERROR')


    # Нажатие кнопки расшифровать
    def dec_btn_click(self):
        self.ent_text.delete('1.0', END)

        key = self.key_text.get("1.0", "end-1c").replace('\n', ' ')
        text = self.res_text.get("1.0", "end-1c").replace('\n', ' ')
        
        if len(key) > 0:
            textDecrypt = self.decrypt(text, key )
            self.ent_text.insert(END, self.hexToUtf8(textDecrypt))
        else:
            print('ERROR')


    # Очистка text
    def clear_btn_click(self):
        self.key_text.delete('1.0', END)
        self.res_text.delete('1.0',END)
        self.ent_text.delete('1.0', END)


    # Текст из шестнадцатеричного формата в кодировку utf8
    @staticmethod
    def hexToUtf8(text):
        text = binascii.unhexlify(text).decode('utf8')
        return text


    # Текст из кодировки utf8 в шестнадцатеричный формат
    @staticmethod
    def utf8ToHex(text):
        text = binascii.hexlify(text.encode('utf8')).decode('utf8')
        return text


    # XOR
    def xor(self, num1, num2, in_code = 2):
        len1 = len(str(num1))
        num1 = int(num1, in_code)
        num2 = int(num2, in_code)

        num = str(bin(num1 ^ num2)[2:])

        num = self.fillZerosBeforeNumber(num, len1)

        return num


    # Добавление нулей в начало
    @staticmethod
    def fillZerosBeforeNumber(num1, length):
        num1 = str(num1)
        if len(str(num1)) != length:
            for i in range(length - len(str(num1))):
                num1 = '0' + num1
        return num1


    # Добавление нулей в конец числа
    @staticmethod
    def fillZerosAfterNumber(num1, length):
        num1 = str(num1)
        if len(str(num1)) != length:
            for i in range(length - len(str(num1))):
                num1 = num1 + '0'
        return num1


    def overwriteMode(self, bitNumberIn):
        bitNumberInOut = ''
        for i in range(8):
            num1 = bitNumberIn[i * 4: i * 4 + 4]
            num2 = bin(self.transformation_table[i][int(bitNumberIn[i * 4: i * 4 + 4], 2)])[2:]
            num2 = self.fillZerosBeforeNumber(num2, 4)

            bitNumberInOut += self.xor(num1, num2, 2)
        return bitNumberInOut


    def transformation(self, numLeft, numRight, key):
        numLeftOut = numRight
        numRightOut = self.xor(numRight, key, 2)
        numRightOut = self.overwriteMode(numRightOut)
        numRightOut = self.xor(numRightOut, numLeft, 2)
        return numLeftOut, numRightOut


    def chainOfTransformations(self, numLeft, numRight, key, move = 'straight'):
        if move == 'reverse':
            start = 31
            stop = 0
            step = -1
            last = 0
        else:
            start = 0
            stop = 31
            step = 1
            last = 31
        for i in range(start, stop, step):
            numLeft, numRight = self.transformation(numLeft, numRight, key[i])
        numRightLast = numRight
        numLeft, numRight = self.transformation(numLeft, numRight, key[last])
        return numRight + numRightLast


    def convertBase(self, num, toBase = 10, fromBase = 10):
        if isinstance(num, str):
            n = int(num, fromBase)
        else:
            n = int(num)
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if n < toBase:
            return alphabet[n]
        else:
            return self.convertBase(n // toBase, toBase) + alphabet[n % toBase]


    # Длина ключа
    @staticmethod
    def transformKey(key):
        key = binascii.hexlify(key.encode('utf8')).decode('utf8')
        count = 64 - len(key) % 64
        while len(key) < 64:
            key += key
        return key[:64]


    def cutKey(self, key):
        key = self.convertBase(key, 2, 16)
        keys = []
        for i in range(3):
            for j in range(8):
                keys.append(key[j * 32 : j * 32 + 32])
        for i in range(7, -1, -1):
            keys.append(key[i * 32 : i * 32 + 32])
        return keys


    # Шифрование
    def encrypt(self, text, key):
        key = self.transformKey(key)
        key = self.cutKey(key)
        text = self.convertBase(self.utf8ToHex(text), toBase = 2, fromBase = 16)
        if len(text) % 8 != 0:
            text = self.fillZerosBeforeNumber(text, (len(text) // 8)  * 8 + 8)
        textArray = []
        textEncrypt = ''
        for i in range(len(text) // 64 + 1):
            textForAppend = text[i * 64 : i * 64 + 64]
            textForAppend = self.fillZerosAfterNumber(textForAppend, 64)
            textArray.append(textForAppend)
        for i in range(len(textArray)):
            textEncrypt += self.chainOfTransformations(textArray[i][:32], textArray[i][32:], key)
        textEncrypt = self.convertBase(textEncrypt, toBase = 16, fromBase = 2)
        return textEncrypt


    # Расшифрование
    def decrypt(self, text, key):
        key = self.transformKey(key)
        key = self.cutKey(key)
        text = self.convertBase(text, toBase = 2, fromBase = 16)
        if len(text) % 8 != 0:
            text = self.fillZerosBeforeNumber(text, (len(text) // 8)  * 8 + 8)
        textArray = []
        textDecrypt = ''
        if (len(text) // 64 * 64) != len(text):
            count = len(text) // 64 + 1
        else:
            count = len(text) // 64
        for i in range(count):
            textForAppend = text[i * 64 : i * 64 + 64]
            textForAppend = self.fillZerosAfterNumber(textForAppend, 64)
            textArray.append(textForAppend)
        for i in range(len(textArray)):
            textDecrypt += self.chainOfTransformations(textArray[i][:32], textArray[i][32:], key, move = 'reverse')
        textDecrypt = self.convertBase(textDecrypt, toBase = 16, fromBase = 2)
        return textDecrypt


    transformation_table = [
        [11, 7, 8, 15, 1, 13, 12, 6, 0, 5, 10, 9, 4, 3, 2, 14],
        [13, 12, 0, 1, 2, 9, 8, 15, 7, 10, 11, 14, 4, 5, 3, 6],
        [7, 5, 13, 6, 10, 14, 0, 1, 9, 2, 15, 8, 3, 4, 12, 11],
        [10, 9, 0, 4, 13, 2, 7, 15, 14, 1, 6, 11, 5, 12, 8, 3],
        [13, 1, 0, 4, 14, 6, 10, 15, 8, 3, 12, 7, 9, 11, 5, 2],
        [9, 4, 14, 2, 7, 13, 1, 8, 5, 15, 0, 11, 12, 6, 10, 3],
        [15, 6, 14, 13, 8, 10, 2, 0, 9, 12, 1, 7, 5, 11, 3, 4],
        [10, 6, 4, 2, 12, 13, 5, 15, 8, 14, 3, 7, 11, 0, 9, 1]
    ]


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


set_appearance_mode('dark')
set_default_color_theme('green')

app = App()
app.mainloop()
