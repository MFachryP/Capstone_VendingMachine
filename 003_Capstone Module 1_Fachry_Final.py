import os
from prettytable import PrettyTable
import pwinput
from colorama import Fore, Back, Style

# Initialize colorama
from colorama import init
init(autoreset=True)

# Membersihkan layar terminal sesuai OS
os.system('cls' if os.name == 'nt' else 'clear')

class VendingMachine:
    def __init__(self):
        self.items = {
            "soda": {
                "1a": {"name": "Coca Cola", "price": 6000, "stock": 10},
                "2a": {"name": "Pepsi", "price": 4500, "stock": 8},
                "3a": {"name": "Fanta", "price": 6000, "stock": 10},
                "4a": {"name": "Sprite", "price": 6000, "stock": 6},
                "5a": {"name": "Nipis Madu", "price": 3500, "stock": 4},
            },
            "coffee": {
                "1b": {"name": "Golda", "price": 4000, "stock": 10},
                "2b": {"name": "ABC Kopi Susu", "price": 4500, "stock": 5},
                "3b": {"name": "Nescafe Latte", "price": 7500, "stock": 7},
                "4b": {"name": "Good Day Cappucino", "price": 8000, "stock": 6},
                "5b": {"name": "Torabika Susu", "price": 5000, "stock": 8},
            },
            "water": {
                "1c": {"name": "Aqua", "price": 4000, "stock": 15},
                "2c": {"name": "Le Minerale", "price": 4000, "stock": 10},
                "3c": {"name": "Vit", "price": 2500, "stock": 8},
                "4c": {"name": "Nestle", "price": 3500, "stock": 5},
                "5c": {"name": "Ades", "price": 3500, "stock": 7},
            },
        }
        self.balance = 0
        self.transactions = []  # Menyimpan riwayat transaksi

    def insert_money(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            amount = int(input("Masukkan jumlah uang: "))
            if amount > 0:
                self.balance += amount
                print(f"{Fore.GREEN}Saldo saat ini: {self.balance} IDR{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Masukkan jumlah uang yang valid!{Style.RESET_ALL}")
                print("Kembali ke menu login...\n")
                return  # Kembali ke menu login
        except ValueError:
            print(f"{Fore.RED}Input harus berupa angka! Kembali ke menu login...\n{Style.RESET_ALL}")
            return  # Kembali ke menu login

    def display_items(self, max_price=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}\nDaftar Produk:{Style.RESET_ALL}")
        for category, products in self.items.items():
            table = PrettyTable()
            table.title = f"Kategori: {category.capitalize()}"
            table.field_names = ["ID", "Nama Produk", "Harga (IDR)", "Stok"]
            for item_id, item in products.items():
                if max_price is None or item['price'] <= max_price:  # Filter berdasarkan saldo
                    table.add_row([item_id, item['name'], item['price'], item['stock']])
            print(table)

    def return_balance(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.YELLOW}Mengembalikan saldo: {self.balance} IDR{Style.RESET_ALL}")
        self.balance = 0

    def update_item(self, item_id, name=None, price=None, stock=None):
        os.system('cls' if os.name == 'nt' else 'clear')
        for category in self.items:
            if item_id in self.items[category]:
                if name:
                    self.items[category][item_id]["name"] = name
                if price:
                    self.items[category][item_id]["price"] = price
                if stock:
                    self.items[category][item_id]["stock"] = stock
                print(f"{Fore.GREEN}Produk berhasil diperbarui!{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}Produk tidak ditemukan!{Style.RESET_ALL}")

    def buy_item(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_items(max_price=self.balance)  # Hanya tampilkan produk yang bisa dibeli
        item_id = input("Masukkan ID produk yang ingin dibeli: ")
        for category in self.items:
            if item_id in self.items[category]:
                item = self.items[category][item_id]
                if item["stock"] > 0:
                    if self.balance >= item["price"]:
                        self.balance -= item["price"]
                        item["stock"] -= 1
                        self.transactions.append({
                            "Nama Produk": item['name'],
                            "Harga": item['price'],
                            "Sisa Stok": item['stock']
                        })
                        print(f"{Fore.GREEN}Berhasil membeli {item['name']}! Sisa saldo: {self.balance} IDR{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Saldo tidak cukup!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Stok habis!{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}Produk tidak ditemukan!{Style.RESET_ALL}")

    def add_item(self, category, item_id, name, price, stock):
        os.system('cls' if os.name == 'nt' else 'clear')
        if category in self.items:
            if item_id not in self.items[category]:
                self.items[category][item_id] = {"name": name, "price": price, "stock": stock}
                print(f"{Fore.GREEN}Produk berhasil ditambahkan!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}ID produk sudah ada!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Kategori tidak valid!{Style.RESET_ALL}")

    def delete_item(self, item_id):
        os.system('cls' if os.name == 'nt' else 'clear')
        for category in self.items:
            if item_id in self.items[category]:
                del self.items[category][item_id]
                print(f"{Fore.GREEN}Produk berhasil dihapus!{Style.RESET_ALL}")
                return
        print(f"{Fore.RED}Produk tidak ditemukan!{Style.RESET_ALL}")

    def view_items(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}\n📦 Daftar Barang dalam Vending Machine:{Style.RESET_ALL}")
        for category, products in self.items.items():
            table = PrettyTable()
            table.title = f"Kategori: {category.capitalize()}"
            table.field_names = ["ID", "Nama Produk", "Harga (IDR)", "Stok"]
            for item_id, item in products.items():
                table.add_row([item_id, item['name'], item['price'], item['stock']])
            print(table)


def confirm_exit(message):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        confirm = input(f"{message} (y/n): ").strip().lower()
        if confirm == 'y':
            return True
        elif confirm == 'n':
            return False
        else:
            print(f"{Fore.RED}Pilihan tidak valid! Masukkan 'y' atau 'n'.{Style.RESET_ALL}")

def get_required_input(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print(f"{Fore.RED}Input tidak boleh kosong!{Style.RESET_ALL}")

def get_required_int_input(prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            print(f"{Fore.RED}Harus berupa angka yang valid!{Style.RESET_ALL}")

def user_menu(vm):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}\nSilahkan pilih inuman yang ada di vending machine!{Style.RESET_ALL}")
    vm.insert_money()  # User langsung diminta memasukkan uang

    while True:
        print(f"{Fore.CYAN}\nMenu Pengguna:{Style.RESET_ALL}")
        print("1. Beli Produk")
        print("2. Selesaikan Pembelian")

        choice = input("Pilih menu: ").strip()

        if choice == "1":
            vm.buy_item()
        elif choice == "2":
            if confirm_exit("Apakah Anda yakin ingin menyelesaikan pembelian?"):
                vm.return_balance()
                print(f"{Fore.GREEN}Saldo dikembalikan. Terima kasih telah berbelanja!\n{Style.RESET_ALL}")
                print("Silahkan Pilih Tipe Pengguna:\n")
                return  # Kembali ke `main()`, memungkinkan user login ulang
            else:
                print(f"{Fore.YELLOW}Batal menyelesaikan pembelian. Kembali ke menu pengguna.\n{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Pilihan tidak valid! Silakan pilih 1 atau 2.\n{Style.RESET_ALL}")

def admin_menu(vm):
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print(f"{Fore.CYAN}\nMenu Admin:{Style.RESET_ALL}")
        print("1. Lihat Barang")
        print("2. Tambah Produk")
        print("3. Perbarui Produk")
        print("4. Hapus Produk")
        print("5. Lihat Laporan Transaksi")
        print("6. Kembali ke Menu Login")
        choice = get_required_input("Pilih menu: ")
        
        if choice == "1":
            vm.view_items()
        elif choice == "2":
            category = get_required_input("Masukkan kategori produk (soda/coffee/water): ")
            item_id = get_required_input("Masukkan ID produk: ")
            name = get_required_input("Masukkan nama produk: ")
            price = get_required_int_input("Masukkan harga produk: ")
            stock = get_required_int_input("Masukkan stok produk: ")
            vm.add_item(category, item_id, name, price, stock)
        elif choice == "3":
            item_id = get_required_input("Masukkan ID produk yang ingin diperbarui: ")
            name = input("Masukkan nama baru (kosongkan jika tidak ingin mengubah): ").strip() or None
            price = input("Masukkan harga baru (kosongkan jika tidak ingin mengubah): ").strip()
            stock = input("Masukkan stok baru (kosongkan jika tidak ingin mengubah): ").strip()
            price = int(price) if price.isdigit() else None
            stock = int(stock) if stock.isdigit() else None
            vm.update_item(item_id, name, price, stock)
        elif choice == "4":
            item_id = get_required_input("Masukkan ID produk yang ingin dihapus: ")
            if confirm_exit(f"Apakah Anda yakin ingin menghapus produk dengan ID {item_id}?"):
                vm.delete_item(item_id)
            else:
                print(f"{Fore.YELLOW}Penghapusan dibatalkan.{Style.RESET_ALL}")
        elif choice == "5":
            if vm.transactions:
                print(f"{Fore.CYAN}\nLaporan Transaksi:{Style.RESET_ALL}")
                for i, trans in enumerate(vm.transactions, 1):
                    print(f"{i}. {trans['Nama Produk']} - {trans['Harga']} IDR - Sisa Stok: {trans['Sisa Stok']}")
            else:
                print(f"{Fore.YELLOW}Belum ada transaksi.{Style.RESET_ALL}")
        elif choice == "6":
            if confirm_exit("Apakah Anda yakin ingin kembali ke menu login?"):
                print("Silahkan Pilih Tipe Pengguna:")
                break
            else:
                print(f"{Fore.YELLOW}Kembali ke menu admin.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Pilihan tidak valid!{Style.RESET_ALL}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    vm = VendingMachine()
    while True:  # Loop utama untuk kembali ke menu login
        print(f"{Fore.CYAN}\nPilih tipe pengguna:{Style.RESET_ALL}")
        print("1. User")
        print("2. Admin")
        print("3. Keluar")
        user_type = input("Masukkan pilihan (1/2/3): ")
        if user_type == "1":
            user_menu(vm)
        elif user_type == "2":
            password = pwinput.pwinput("Masukkan password admin: ")
            if password == "12345":
                admin_menu(vm)
            else:
                print(f"{Fore.RED}Password salah! Akses ditolak.{Style.RESET_ALL}")
        elif user_type == "3":
            print(f"{Fore.YELLOW}Keluar dari program.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()