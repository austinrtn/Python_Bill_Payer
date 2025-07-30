import os 
import time
import json
import readchar
from rich import print 
from rich.console import Console
from rich.table import Table 
from Bill import Bill 

filename = "bill_data.json"
console = Console()
show_all_bills = False
page_index = 0
max_items_in_page = 3

def clr():
    os.system("clear")

def main_menu():
    while True:
        clr()
        console.print("[bold cyan][1] view bills")
        console.print("[bold green][2] add bill")
        console.print("[bold red][[q]] exit")

        key = readchar.readkey()
        if key == "1":
            view_bills()
        elif key == "2":
            add_bill()
        elif key == "q":
            exit(0)

def pagify(items, page_number, page_size):
    start = page_number * page_size
    end = start + page_size
    return items[start:end]

def view_bills():
    if not os.path.exists(filename):
        clr()
        console.print("[bold cyan]You haven't added any bills yet!")
        readchar.readkey()
        return 

    while True:
        clr()
        global page_index
        bills = []
        with open(filename, "r") as f: 
            try: 
                json_bills = json.load(f)
                for bill in json_bills:
                    bills.append(Bill(bill["name"], bill["amount"], bill["due_date"], bill['website'], uid=bill["uid"]))
            except json.JSONDecodeError:
                bills = []
        
        bills_in_page = pagify(bills, page_index, max_items_in_page)

        table = get_bill_table(bills_in_page)
        console.print(table)

        key = readchar.readkey()
        if key == readchar.key.RIGHT: page_index += 1
        elif key == readchar.key.LEFT: page_index -=1 
        elif key.isdigit():
            i = int(key)
            selected_bill = bills_in_page[i]
            select_bill(selected_bill)
        elif key == "q": break
    
def get_bill_table(bills):
    table = Table(title="Bills")
    col_color = "cyan"

    table.add_column("#")
    table.add_column("Name", style=col_color)
    table.add_column("Amount", style=col_color)
    table.add_column("Due", style=col_color)

    for i, bill in enumerate(bills):
        if bill.paid and not show_all_bills: continue
        table.add_row(str(i), bill.name, str(bill.amount), str(bill.due_date))

    num_cols = len(table.columns)
    if num_cols > max_items_in_page: 
        empty_row = [""] * num_cols
        for _ in range(max_items_in_page - len(bills)):
            table.add_row(*empty_row)
    
    return table

def select_bill(bill):
    while True:
        clr()
        console.print(f"[bold]{bill.name} | ${bill.amount}[/bold]")
        console.print(f"[yellow][1]Mark Paid[/yellow]")
        console.print(f"[green][2]Open Website[/yellow]")
        console.print(f"[red][3]Delete[/yellow]")
        readchar.readkey()

def add_bill():
    while True:
        clr()
        name = None
        amount = None
        due_date = None
        website = None

        console.print("Bill Name/Company: ")
        name = input().strip()
        clr()

        console.print("Amount: ")
        amount = input().strip()
        try:
            amount = float(amount)
        except ValueError:
            console.print("[bold red]Input cannot contain non-numeric characters.[/bold red]")
            readchar.readkey()
            continue

        clr()

        console.print("Day of the month bill is due: ")
        due_date = input()

        try:
            int_date = int(due_date)
            if not 1 <= int_date <= 31:
                raise ValueError
            if int_date < 10:
                due_date = "0" + due_date


        except ValueError:
            console.print("[bold red]Incorrect Date[/bold red]") 
            readchar.readkey()
            continue

        clr()

        console.print("Website: ")
        website = input().strip()
        clr()

        console.print("Does this look correct? [bold green]Y[/bold green]/[bold red]N[/bold red]")
        console.print(f"Name: [bold]{name}[/bold]")
        console.print(f"Amount: [bold]{amount}[/bold]")
        console.print(f"Due Date: [bold]{due_date}")
        console.print(f"Website: [bold]{website}[/bold]")

        while True:
            key = readchar.readkey()
            k = key.lower()
            if k == "y":
                bill = Bill(name, amount, due_date, website)
                append_bill_to_file(bill)
                return True
            elif k == "n":
                break

def append_bill_to_file(bill):
    data = bill.get_json()
    bills = []


    bills.append(data)

    with open(filename, "w") as f:
        json.dump(bills, f, indent=2)

    console.print("[bold green] Bill saved successfully!  Press any key to continue...")
    readchar.readkey()

if __name__ == "__main__":
    main_menu()
