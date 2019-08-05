from tkinter import *
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

class fortune_teller:
    def __init__ (self, master):
        self.label = ttk.Label(master,text = 'Cross my palm with silver and I will tell you your fortune...')
        self.label.grid(row =0, column = 0, columnspan = 4)
        self.label.config(font = ('Comic sans', 12))
        self.label.config(foreground = 'white', background = 'black')
        self.label.config(wraplength = 150)

        
        ttk.Button (master, text = 'give nothing...',
            command = self.nothing_fortune).grid(row=1, column = 0)

        
        ttk.Button (master, text = 'give 25 cents...',
            command = self.twenty_five_cent_fortune).grid(row=1, column = 1)
        
        
        ttk.Button (master, text = 'give $10...',
            command = self.ten_dollar_fortune).grid(row=1, column = 2)
        
        
        ttk.Button (master, text = 'give $1000...',
            command = self.thousand_dollar_fortune).grid(row=1, column = 3)
    
    def nothing_fortune(self):
        self.label.config(text= 'as I look upon your worthless palm I see suffering and pain. Your house will smell of onions and all the wine that you drink will taste like sweat.')
        self.label.config(foreground = 'blue', background = 'yellow')
        self.label.config(font = ('Courier', 12, 'bold'))
        self.label.config(wraplength = 150)
    def twenty_five_cent_fortune(self):
        self.label.config(text=  'I peer into your skinflinted weary palm and see a future including a studio apartment and a vast amount of tabby cats.')
        self.label.config(wraplength = 150)
        self.label.config(foreground = 'blue', background = 'purple')
    def ten_dollar_fortune(self):
        self.label.config(text= 'Your noble hand tells me a story of future encounters with wise fortune tellers leading to great wealth for one of the involved parties.')
        self.label.config(foreground = 'blue', background = 'orange')
        self.label.config(wraplength = 150)
    def thousand_dollar_fortune(self):
        self.label.config(text= 'Do you really think that I can get you that much angel dust?')
        self.label.config(wraplength = 150)
        self.label.config(foreground = 'blue', background = 'pink')
tk = Tk()
ft = fortune_teller(tk)

tk.mainloop()

