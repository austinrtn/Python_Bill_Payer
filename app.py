import os 
import sys
import math
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
max_items_in_page = 9

def clr():
    os.system("clear")

def hotkey(key: str, desc: str, key_style="black on white", desc_style=""):
    text = Text.assemble(
        (" " + key + " ", key_style),
        (" " + desc, desc_style)
    )
    return text

def main_menu():
    while True:
        clr()
        console.print("[b][grey]BILL MANAGER[/grey][/b]")
        console.print("[b][cyan][1]VIEW BILLS[/cyan][/b]")
        console.print("[b][green][2]ADD BILL[/green][/b]")
        console.print("[b][red][Q]EXIT[/red][/b]")

        key = readchar.readkey().lower()
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
        global page_index, show_all_bills
        if not show_all_bills: bills = Bill.get_unpaid_bills()
        else: bills = Bill.get_all_bills()

        bills_in_page = pagify(bills, page_index, max_items_in_page)

        table = get_bill_table(bills_in_page, len(bills))
        amount_of_pages = math.ceil(len(bills) / max_items_in_page)-1
        console.print(table)
        print_table_bindings()
        console.print("\n[bold red]Remember not to overdraft[/bold red]")
        key = readchar.readkey().lower()

        if key == "l": 
            page_index += 1
            if page_index > amount_of_pages:
                page_index = 0

        elif key == "j": 
            page_index -=1 
            if page_index < 0:
                page_index = amount_of_pages

        elif key == "f":
            if show_all_bills: show_all_bills = False
            else: show_all_bills = True

        elif key == "r":
            clr()
            console.print("[bold][yellow]Are you sure you want to mark all bills as unpaid?[/yellow] [cyan]Y[/cyan]/[red]N[/red][/bold]")
            confirm = readchar.readkey()
            if confirm == "y": 
                Bill.mark_all_as_unpaid() 
            elif confirm == "n":
                continue

        elif key.isdigit():
            i = int(key)
            if i > len(bills_in_page)-1: continue 
            selected_bill = bills_in_page[i]
            select_bill(selected_bill)

        elif key == "q": break
    
def get_bill_table(bills, total_bill_count):
    total_pages = math.ceil(total_bill_count / max_items_in_page)
    current_page = page_index + 1  # assuming page_index starts at 0
    title = f"BILLS [{current_page}/{total_pages}]"
    col_color = "cyan"

    table = Table(title=title)
    table.add_column("#")
    table.add_column("Name", style=col_color)
    table.add_column("Amount", style=col_color)
    table.add_column("Due", style=col_color)
    table.add_column("Paid", style=col_color)

    total_amount = 0
    for i, bill in enumerate(bills):
        if bill.paid: paid = "✅ " 
        else: paid = "❌ "
        table.add_row(str(i), bill.name, str(bill.amount), str(bill.due_date), paid)
        total_amount += bill.amount
    table.add_row("", "[b][red]Total Amount[/red][/b]", "[b][red]" + str(total_amount) + "[/b][/red]", "", "")

    num_cols = len(table.columns)
    if num_cols > max_items_in_page: 
        empty_row = [""] * num_cols
        for _ in range(max_items_in_page - len(bills)):
            table.add_row(*empty_row)

    
    return table

def print_table_bindings():
    console.print(f"\n\nLast Page / Next Page [J/L]")
    if show_all_bills:
        console.print("Show Unpaid Bills [F]")
    else:
        console.print("Show All Bills [F]")
    console.print("Mark All As Unpaid [R]") 
    console.print("Main Menu [Q]")

def select_bill(bill):
    while True:
        clr()

        bill_status = "Unpaid" if bill.paid  else "Paid"
        
        console.print(f"[bold]{bill.name} | ${bill.amount}[/bold]")
        console.print(f"[green][1]Mark {bill_status}[/green]")
        console.print(f"[yellow][2]Edit Bill[/yellow]")
        console.print(f"[cyan][3]Open Website[/cyan]")
        console.print(f"[red][4]Delete[/red]")
        console.print(f"[Q]Back")
        key = readchar.readkey()

        if key == "1":
            if bill.paid:
                bill.paid = False
            else: bill.paid = True
            Bill.edit_bill(bill)
            break
        elif key == "2":
            edit_bill(bill)
        elif key == "3":
            bill.open_website()
        elif key == "4": 
            while True:
                clr()
                console.print("[bold]Do you really want to delete bill? [cyan]Y[/cyan]/[red]N[/red][/bold]")
                confirm = readchar.readkey()

                if confirm == "y":
                    Bill.delete_bill(bill)
                    return
                elif confirm == "n":
                    break

        elif key == "q":
            break

def edit_bill(bill):
    while True:
        clr()
        console.print("[bold]Select to edit[/bold]")
        console.print("[1]Name")
        console.print("[2]Amount")
        console.print("[3]Due Date")
        console.print("[4]Website")
        console.print("[Q]Back")
        key = readchar.readkey()

        if key == "q":
            return

        clr()
        console.print("[bold]Enter New Value:[/bold]")
        value = input()

        if key == "1":
            bill.name = value

        elif key == "2":
            try: 
                value = float(value)
                bill.amount =  value   
            except ValueError:
                console.print("[bold red]Error: Non-numeric value entered.[/bold red]")
                readchar.readkey()

        elif key == "3":
            value = format_date(value)
            if not value: 
                readchar.readkey()
                continue
            bill.due_date = value
                
        elif key == "4": 
            bill.website = value


        Bill.edit_bill(bill)

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
            console.print("[bold red]Error: Non-numeric value entered.[/bold red]")
            readchar.readkey()
            continue

        clr()

        console.print("Day of the month bill is due: ")
        due_date = input()
        due_date = format_date(due_date)

        if due_date is None:
            readchar.readkey()
            continue
        clr()

        console.print("Website: ")
        website = input().strip()
        clr()

        console.print(f"Name: [bold]{name}[/bold]")
        console.print(f"Amount: [bold]{amount}[/bold]")
        console.print(f"Due Date: [bold]{due_date}")
        console.print(f"Website: [bold]{website}[/bold]")
        console.print("Does this look correct? [bold green]Y[/bold green]/[bold red]N[/bold red]")

        while True:
            key = readchar.readkey()
            k = key.lower()
            if k == "y":
                bill = Bill(name, amount, due_date, website)
                Bill.add_bill(bill)
                return True
            elif k == "n":
                break

def format_date(date):
    try:
        int_date = int(date)
        if not 1 <= int_date <= 31:
            raise ValueError
        if int_date < 10:
            date = "0" + date
        return date

    except ValueError:
        console.print("[bold red]Error:Inccorect data entered.[/bold red]") 
        return None 

def exit_program():
    print("Thank you come again :3")
    sys.exit()

if __name__ == "__main__":
    try: 
        main_menu()
    except KeyboardInterrupt:
        exit_program()
    exit_program()


