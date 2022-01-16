import tkinter as tk
from tkinter.constants import BOTH
import tkinter.ttk as ttk
from typing import Callable
import classes.vendingMachine as vm

class VendingMachineHandler():
    """Łączy interfejs graficzny z obiektem Vending Machine przechwytując zdarzenia"""
    def __init__(self):
        self.vendingMachine = vm.VendingMachine(5)
        self.numberText =''
        self.coinText = ''
        self.item_number_text = ''

    def display_popover(self, text):
        """Wyświetla dodatkowe okno z informacją przekazaną w zmiennej text"""
        popup = tk.Toplevel()
        popup.geometry('200x120+400+400')
        popup.wm_title("Informacja")
        popup.grid_columnconfigure(0, pad=3, weight=1)
        popup.grid_rowconfigure(0, pad=3, weight=1)
        popup.grid_rowconfigure(1, pad=3, weight=1)

        #tworzenie etykiety
        label = tk.Label(popup, text=text)
        label.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #tworzenie przycisku
        button = ttk.Button(popup, text="OK", command=popup.destroy)
        button.grid(row=1,column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

    def check_item(self):
        """Sprawdza czy dany napój istnieje i próbuje wykonać zakup. Wyświetla odpowiedni komunikat w popupie wrazie braku, lub niepoprawnego numeru produktu"""
        itemNumber = int(self.item_number_text)
        try:
            #pobiera info o napoju
            name, price, amount = self.vendingMachine.get_item_details(itemNumber)
        except vm.BeverageNumberException:
            return
        try:
            #próba kupna
            change, item = self.vendingMachine.pay_for_item(itemNumber)
            for c in change:
                self.vendingMachine.insert_coin(c)
            self.update_coins_text()
            self.display_popover(f'Zakupiono napój: {item.get_name()}\n\nReszta została\nzwrócona')
        except vm.MoneyException:
            self.display_popover(f'Wybrano napój: {name}\nCena: {price}\nPozostało: {amount}')
        except vm.ChangeOnlyException:
            self.display_popover(f'Tylko odliczona kwota')
        except vm.OutOfStorageException:
            self.display_popover('Zapasy się skończyły')
        finally:
            self.item_number_text = ''
            self.update_number_text()

    def update_coins_text(self):
        """Ustawia ile monet zostało wrzuconych"""
        amount = self.vendingMachine.get_inserted_coins_value()
        self.coinText.set(f'{amount}')

    def update_number_text(self):
        self.numberText.set(self.item_number_text)

    def on_coin_btn_click(self, value):
        """Funkcja reagujaca na kliknięcie przycisku monet"""
        self.vendingMachine.insert_coin(vm.Coin(value))
        self.update_coins_text()
    
    def on_number_btn_click(self, value: int):
        """Funkcja reagująca na kliknięcie na przycisk z numerem napoju"""
        self.item_number_text += f'{value}' #dodaje nową cyfrę do stringu nad klawiaturą
        self.update_number_text()
        self.check_item()

    def on_clear_number_btn_click(self):
        """Czyści wyświetlacz na klawiaturą numeryczną gdy klikniemy przycisk clear"""
        self.item_number_text = ''
        self.update_number_text()

    def on_clear_coins_btn_click(self):
        """Czyści wprowadzone monety do automatu i zwraca klientowi."""
        amount = vm.get_coins_value(self.vendingMachine.return_inserted_coins())
        self.update_coins_text()
        self.display_popover(f"Zwrócono {amount}zł")

class Main(tk.Frame):
    """Główna klasa renderująca widok aplikacji za pomoca modułu tkinter"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title('Automat sprzedający napoje')
        self.master.geometry('1300x600+0+0')
        self.handler = VendingMachineHandler()
        self.configure(bg="light blue")
        self.create_widgets()

    def create_widgets(self):
        ttk.Style().configure('TButton', padding=(4,4,4,4))
        #tworzymy siatke widoku
        for i in range(0,6):
            self.grid_columnconfigure(i, pad=3, weight=1)

        self.grid_rowconfigure(0, pad=3, weight=0)
        self.grid_rowconfigure(1, pad=3, weight=0)
        for i in range(2, 6):
            self.grid_rowconfigure(i, pad=3, weight=1)
        
        #Wyświetlacz do numeru produktu
        label = tk.Label(self, text="Wprowadź numer:")
        label.grid(row=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.numberText = tk.StringVar()
        numberText = tk.Entry(self, justify='right', state=tk.DISABLED, textvariable=self.handler.numberText)
        numberText.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #Wyświetlacz z sumą wprowadzonych pieniędzy
        label = tk.Label(self, text="Wprowadź kwotę:")
        label.grid(row=0, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        self.handler.coinText = tk.StringVar()
        coinText = tk.Entry(self, justify='right', state=tk.DISABLED, textvariable=self.handler.coinText)
        coinText.grid(row=1, column=3, columnspan=3, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        #Tworzenie przycisków
        self.create_keypad(2, 0, self.handler.on_number_btn_click, [i for i in range(1, 10)], True)
        self.create_keypad(2, 3, self.handler.on_coin_btn_click, vm.coin_values, False)
        button = tk.Button(self, text='CLEAR NUMBER', bg="red", fg="white", command=self.handler.on_clear_number_btn_click)
        button.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        button = tk.Button(self, text='CLEAR COINS', bg="red", fg="white",command=self.handler.on_clear_coins_btn_click)
        button.grid(row=5, column=3, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

        self.pack(fill="both", expand=True)

    def create_keypad(self, n_row, n_column, func, values, add_zero):
        """Tworzy przyciski od 0-9 i przypisuje im funkcje po wciśnięciu"""
        start_row = n_row + 2
        for i in range(0, 9):
            button = tk.Button(self, text=f'{values[i]}', command=lambda value = values[i]: func(value))
            button.grid(row=start_row - (i // 3), column=i % 3 + n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
        if add_zero:
            button = tk.Button(self, text='0', command=lambda: func(0))
            button.grid(row=n_row + 3, column=n_column, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)

if __name__ == '__main__':
    root=tk.Tk()
    app = Main(root)
    app.mainloop()
