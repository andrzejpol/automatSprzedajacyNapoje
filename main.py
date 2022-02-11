from turtle import bgcolor
import main.Automat.Automat as at
from tkinter.constants import BOTH
import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable

class AutomatHandler():
    """Łączy GUI z obiektem Automat przechwytujac wszystkie eventy"""
    def __init__(self):
        self.automat = at.Automat(5)
        self.numberText: tk.StringVar
        self.coinText: tk.StringVar
        self.item_number_text = ''

    def display_popup(self, text):
        """Pokazuje popup z informacjami"""
        popup = tk.Toplevel()
        popup.geometry('200x120+400+400')
        popup.wm_title("Info")
        popup.grid_columnconfigure(0, pad=3, weight=1)
        popup.grid_rowconfigure(0, pad=3, weight=1)
        popup.grid_rowconfigure(1, pad=3, weight=1)

        label = tk.Label(popup, text=text, background="lightblue")
        label.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        b = ttk.Button(popup, text="OK", command=popup.destroy)
        b.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

    def check_item(self):
        """Sprawdza czy istnieje produkt wybrany przez klienta, wyświetla odpowiednie info"""
        itemNumber = int(self.item_number_text)
        try:
            name, price, amount = self.automat.get_item_details(itemNumber)
        except at.InvalidItemNumberException:
            return
        try:
            change, item = self.automat.pay_for_item(itemNumber)
            for c in change:
                self.automat.insert_coin(c)
            self.update_coins_text()
            self.display_popup(f'Zakupiono: {item.get_name()}\n\nWydano reszte!')
        except at.NotEnoughMoneyException:
            self.display_popup(f'Wybrano napój: {name}\nCena: {price}\nIlość: {amount}')
        except at.ExactChangeOnlyException:
            self.display_popup(f'Tylko odliczona gotówka!')
        except at.NoItemsLeftException:
            self.display_popup('Produkt niedostępny')
        finally:
            self.item_number_text = ''
            self.update_number_text()

    def update_coins_text(self):
        """Ustawia wprowadzoną ilość gotówki jako tekst"""
        amount = self.automat.get_inserted_coins_value()
        self.coinText.set(f'{amount}')

    def update_number_text(self):
        """Ustawia wprowadzony numer napoju jako tekst"""
        self.numberText.set(self.item_number_text)

    def on_coin_btn_click(self, value):
        """Callback na klikniecie przycisku monety"""
        self.automat.insert_coin(at.Coin(value))
        self.update_coins_text()

    def on_number_btn_click(self, value):
        """Callback na klikniecie przycisku wyboru napoju"""
        self.item_number_text += f'{value}'
        self.update_number_text()
        self.check_item()

    def on_clear_number_btn_click(self):
        """Callback na klikniecie przycisku clear"""
        self.item_number_text = ''
        self.update_number_text()

    def on_clear_coins_btn_click(self):
        """Callback na klikniecie clear, wydaje reszte"""
        amount = at.get_coins_value(self.automat.return_inserted_coins())
        self.update_coins_text()
        self.display_popup(f"Zwrócono {amount}zl")

class Application(tk.Frame):
    """Głowne okno aplikacji"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title('Automat sprzedazowy')
        self.master.geometry('800x300+300+300')
        self.handler = AutomatHandler()
        self.create_widgets()
        self.display_beverages()

    def display_beverages(self):
        """Pokazuje liste z napojami"""
        popup = tk.Toplevel()
        popup.wm_title("Dostepne napoje")
        for i in range(30, 51):
            label=tk.Label(popup, text=f"Napój numer {i}")
            label.pack()

    def create_widgets(self):
        """Tworzenie elementów interfejsu"""
        ttk.Style().configure('TButton', padding=(4, 4, 4, 4))
        #tworzenie grida
        for i in range(0, 6):
            self.grid_columnconfigure(i, pad=3, weight=1)

        self.grid_rowconfigure(0, pad=3, weight=0)
        self.grid_rowconfigure(1, pad=3, weight=0)
        for i in range(2, 6):
            self.grid_rowconfigure(i, pad=3, weight=1)

        #tworzenie wyswietlacza numeru produktow
        label = tk.Label(self, text="Wybierz produkt:", background="lightblue")
        label.grid(row=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.numberText = tk.StringVar()
        numberText = tk.Entry(self, justify='right', font=("Arial", 18), state=tk.DISABLED, textvariable=self.handler.numberText)
        numberText.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        #tworzenie wyswietlacza monet
        label = tk.Label(self, text="Monety:", background="lightblue")
        label.grid(row=0, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.coinText = tk.StringVar()
        coinText = tk.Entry(self, justify='right',font=("Arial", 18), state=tk.DISABLED, textvariable=self.handler.coinText)
        coinText.grid(row=1, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #tworzenie przyciskow
        self.create_keypad(2, 0, self.handler.on_number_btn_click, [i for i in range(1, 10)], True)
        self.create_keypad(2, 3, self.handler.on_coin_btn_click, at.coin_values, False)
        button = tk.Button(self, text='CLEAR',background="lightcoral", font=("Arial", 25, "bold"), command=self.handler.on_clear_number_btn_click)
        button.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        button = tk.Button(self, text='CLEAR',background="lightcoral", font=("Arial", 25, "bold"), command=self.handler.on_clear_coins_btn_click)
        button.grid(row=5, column=3, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        self.pack(fill="both", expand=True)

    def create_keypad(self, n_row, n_column, func, values, add_zero):
        """Tworzenie klawiatury numerycznej 0-9"""
        start_row = n_row + 2
        for i in range(0, 9):
            button = tk.Button(self, font=("Arial", 25),text=f'{values[i]}', command=lambda value = values[i]: func(value))
            button.grid(row=start_row - (i // 3), column=i % 3 + n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        if add_zero:
            button = tk.Button(self, font=("Arial", 25), text='0', command=lambda: func(0))
            button.grid(row=n_row + 3, column=n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    app.mainloop()