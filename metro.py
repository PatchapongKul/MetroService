class Customer:
    def __init__(self,name,user,passwd,phone,type):
        self.name = name
        self.user = user
        self.passwd = passwd
        self.phone_num = phone
        self.user_type = type

    def update_email(self,mail):
        self.email = mail

    def describe_user(self):
        print(f'Customer name: {self.name} \nCustomer type = {self.user_type}')
