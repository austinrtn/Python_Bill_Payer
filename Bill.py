import uuid

filename = "bill_data.json"
bills = None
unpaid_bills = None

class Bill:
    def get_all_bills():
        bills = []
        if os.path.exists(filename):
            with open(filename, "r") as f: 
                try: 
                    bills = json.load(f)
                except json.JSONDecodeError:
                    bills = []

                return bills
                
    def get_unpaid_bills
        if unpaid_bills is not None: return unpaid_bills   

    def add_bill(bill):

    def delete_bill(bill):
        #delete

    def __init__(self, name, amount, due_date, website, uid=None):
        self.name = name 
        self.amount = amount
        self.due_date = due_date
        self.website = website 

        self.paid= False
        if uid is None: self.uid = str(uuid.uuid4()) 
        else: self.uid = uid 

    def get_json(self):
        return {
                "name": self.name,
                "amount": self.amount,
                "due_date": self.due_date,
                "website": self.website,
                "paid": self.paid,
                "uid": self.uid,
                }


