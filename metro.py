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

class Station:
    def __init__(self,name,train_interval_time,train_standby_time,first_run_time,last_run_time):
        self.name = name
        self.train_interval_time = train_interval_time
        self.train_standby_time = train_standby_time
        self.first_run_time = first_run_time
        self.last_run_time = last_run_time

    def describe_station(self):
        print(f'Station: {self.name}\nTrain arrives every {self.train_interval_time} minutes\n'
              f'First train arrive at {self.first_run_time}\nLast train arrives at {self.last_run_time}')

    def station_arrival_time(self):
        def add_time(time, min):
            [h1, m1] = time.split(':')
            h = int(h1);
            m = int(m1)
            new_m = m + min
            if new_m >= 60:
                h += 1
                new_m -= 60
            while len(str(new_m)) != 2:
                new_m = '0' + str(new_m)
            return str(f"{h}:{new_m}")
        all_time = []
        each_time = self.first_run_time

        while each_time != self.last_run_time:
            all_time.append(each_time)
            #print(each_time)
            each_time = add_time(each_time,self.train_interval_time)
            each_time = add_time(each_time, self.train_standby_time)
        all_time.append(self.last_run_time)
        return all_time

    def arrival_time(self,time = 'now'):
        def get_time():
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return current_time[:5]
        if time == 'now':
            time = get_time()

        all_time = self.station_arrival_time()

        [usr_hour,usr_min] = time.split(':')
        near_time = []
        for each_time in all_time:
            [station_hour, station_min] = each_time.split(':')
            if station_hour == usr_hour:
                near_time.append([abs(int(station_min)-int(usr_min)), each_time])
        near_time.sort()
        if len(near_time) >= 2:
            print(f"The nearest time that the train arrives station at {time} are {near_time[0][1]} and {near_time[1][1]} "
                  f"and next {self.train_interval_time} minutes")
        elif len(near_time) == 1:
            print(f"The nearest time that the train arrives station at {time} is {near_time[0][1]}"
                  f"and next {self.train_interval_time} minutes")
        else:
            print("Sorry, no trains are operating at that time")
