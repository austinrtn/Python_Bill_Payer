import uuid
import time
import webbrowser
import os 
import json 

filename = "bill_data.json"

class Bill:
    @staticmethod
    def json_to_bill(data):
        bill = Bill(data["name"], data["amount"], data["due_date"], data['website'], paid=data["paid"], uid=data["uid"])
        return bill

    @staticmethod
    def get_all_bills():
        bills = []
        if os.path.exists(filename):
            with open(filename, "r") as f: 
                try: 
                    bill_data = json.load(f)
                    for data in bill_data:
                        bills.append(Bill.json_to_bill(data))

                except json.JSONDecodeError:
                    bills = []

                return bills
                
    @staticmethod
    def get_unpaid_bills():
        unpaid_bills = []
        all_bills = Bill.get_all_bills()
        for bill in all_bills:
            if bill.paid is not True: 
                unpaid_bills.append(bill)

        return unpaid_bills

    @staticmethod
    def add_bill(bill):
        bills = Bill.get_all_bills()
        bills.append(bill)

        Bill.save(bills)


    @staticmethod
    def delete_bill(bill):
        bills = Bill.get_all_bills()

        for i, other in enumerate(bills):
            if bill.uid == other.uid:
                del bills[i]

        Bill.save(bills)

    @staticmethod
    def edit_bill(bill):
        bills = Bill.get_all_bills()
        for other in bills:
            if bill.uid != other.uid: continue
            for attr, value in vars(bill).items():
                setattr(other, attr, value)
            break

        Bill.save(bills)

    @staticmethod
    def mark_all_as_unpaid():
        bills = Bill.get_all_bills()
        for bill in bills:
            bill.paid = False

        Bill.save(bills)

    @staticmethod
    def save(bills):
        bill_data = [bill.get_json() for bill in bills]
        with open(filename, "w") as f:
            json.dump(bill_data, f, indent=2)

    def __init__(self, name, amount, due_date, website, paid=False, uid=None):
        self.name = name 
        self.amount = amount
        self.due_date = due_date
        self.website = website 

        self.paid = paid
        if uid is None: self.uid = str(uuid.uuid4()) 
        else: self.uid = uid 

    def open_website(self):
        webbrowser.open(self.website)

    def get_json(self):
        return {
                "name": self.name,
                "amount": self.amount,
                "due_date": self.due_date,
                "website": self.website,
                "paid": self.paid,
                "uid": self.uid,
                }


