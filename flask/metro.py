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
    def __init__(self,name,first_run_time='05:30',last_run_time='22:30'):
        self.name = name
        self.train_interval_time = 5
        self.train_standby_time = 1
        self.first_run_time = first_run_time
        self.last_run_time = last_run_time

    def describe_station(self,printing= False):
        if printing: print(f'Station: {self.name}\nTrain arrives every {self.train_interval_time} minutes\n'
                           f'First train arrive at {self.first_run_time}\nLast train arrives at {self.last_run_time}')
        return {"station name":self.name,
                "train interval time": self.train_interval_time,
                "train_standby_time":self.train_standby_time,
                "first_run_time":self.first_run_time,
                "last_run_time":self.last_run_time}

    def station_arrival_time(self):
        def add_time(time, min):
            [h1, m1] = time.split(':')
            h = int(h1);
            m = int(m1)
            new_m = m + min
            if new_m >= 60:
                h += 1
                new_m -= 60
            if h >= 24:
                h = '00'
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

    def arrival_time(self,time = 'now',printing=False):
        def get_time():
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return current_time[:5]

        def append_diff_time(near_time,each_time,time,offset=0):
            diff_time = int(station_min) - int(usr_min) + offset
            if time == 'now':
                if diff_time > 0:
                    near_time.append([diff_time, each_time])
            else:
                near_time.append([abs(diff_time), each_time])

        if time == 'now':
            focus_time = get_time()
        else:
            focus_time = time

        all_time = self.station_arrival_time()

        [usr_hour,usr_min] = focus_time.split(':')
        near_time = []
        for each_time in all_time:
            [station_hour, station_min] = each_time.split(':')
            if int(station_hour) == int(usr_hour):
                append_diff_time(near_time,each_time,time)
            elif int(station_hour) - int(usr_hour) == 1:
                append_diff_time(near_time, each_time, time,60)
            elif int(station_hour) - int(usr_hour) == -1:
                append_diff_time(near_time, each_time, time, -60)

        near_time.sort()
        if printing:
            if len(near_time) >= 2:
                print(f"The nearest time that the train arrives station at {focus_time} are {near_time[0][1]} and {near_time[1][1]} "
                      f"and next {self.train_interval_time + self.train_standby_time} minutes")
            elif len(near_time) == 1:
                print(f"The nearest time that the train arrives station at {focus_time} is {near_time[0][1]}"
                      f"and next {self.train_interval_time} minutes")
            else:
                print("Sorry, no trains are operating at that time")
        return near_time[0:2]

class Metro_Route:
    def __init__(self):
        self.train_route = {'A1':{'A2':(3,6),'B4':(3,6)},
                            'A2':{'A1':(3,6),'A3':(1,2)},
                            'A3':{'A2':(1,2),'A4':(2,4)},
                            'A4':{'A3':(2,4),'A5':(3,6)},
                            'A5':{'A4':(3,6),'B4':(1,2)},
                            'B1':{'B2':(4,8)},
                            'B2':{'B1':(4,8),'B3':(3,6)},
                            'B3':{'B2':(3,6),'B4':(2,4)},
                            'B4':{'A1':(3,6),'A5':(1,2),'B3':(2,4)},}

    def describe_route(self,printing=False):
        station_list = []
        for station in self.train_route:
            station_list.append(station)
        if printing: print(f"The list of all stations in the route are {' -- '.join(station_list)}")
        return self.train_route

    def get_route(self,stationA,stationB,printing=False):
        def find_all_paths(graph, start, end, path=[]):
            path = path + [start]
            if start == end:
                return [path]
            if start not in graph:
                return []
            paths = []
            for node in graph[start]:
                if node not in path:
                    newpaths = find_all_paths(graph, node, end, path)
                    for newpath in newpaths:
                        paths.append(newpath)
            return paths

        def min_path(graph, start, end):
            paths = find_all_paths(graph, start, end)
            mt = 10 ** 99
            mpath = []
            # print('\tAll paths:', paths)
            for path in paths:
                t = sum(graph[i][j][0] for i, j in zip(path, path[1::]))
                # print('\t\tevaluating:', path, t)
                if t < mt:
                    mt = t
                    mpath = path

            route = ' -> '.join(mpath)
            total_time = sum(graph[i][j][0] for i, j in zip(mpath, mpath[1::])) + max(0,len(mpath)-2)
            ticket_price = sum(graph[i][j][1] for i, j in zip(mpath, mpath[1::]))
            return route,total_time,ticket_price

        route,total_time,ticket_price = min_path(self.train_route,stationA.name, stationB.name)
        if total_time == 0:
            print('Invalid Route')
            return [],0,0
        if printing:
            print(f"The passenger should travel by this route: {route}")
            print(f"It will take {total_time} minutes for the trip and the ticket costs {ticket_price} Baht")
        return route, total_time, ticket_price

    def get_destination_time(self,stationA,stationB,time='now',printing=False):
        def add_time(time, min):
            [h1, m1] = time.split(':')
            h = int(h1);
            m = int(m1)
            new_m = m + min
            if new_m >= 60:
                h += 1
                new_m -= 60
            if h >= 24:
                h = '00'
            while len(str(new_m)) != 2:
                new_m = '0' + str(new_m)
            return str(f"{h}:{new_m}")

        route, total_time, ticket_price = self.get_route(stationA,stationB,printing=False)

        if total_time == 0:
            print('Invalid Route!!!')
            return 1

        arrival_time = stationA.arrival_time(time)
        if len(arrival_time)==2:
            des_time1 = add_time(arrival_time[0][1], total_time)
            des_time2 = add_time(arrival_time[1][1], total_time)
            if printing: print(f"You will get to station {stationB.name} at {des_time1} "
                               f"(if you get on the train at {arrival_time[0][1]})\n"
                               f"or {des_time2} (if you get on the train at {arrival_time[1][1]})")
            return {"get_on_1": arrival_time[0][1], "destinatiion_time_1": des_time1,
                    "get_on_2": arrival_time[1][1], "destinatiion_time_2": des_time2}
        elif len(arrival_time) == 1:
            des_time1 = add_time(arrival_time[0][1], total_time)
            return {"get_on_1": arrival_time[0][1], "destinatiion_time_1": des_time1}
        else:
            return {"get_on_1":"None","destinatiion_time_1":"None"}

    def add_station(self,stationA,stationB,time,ticket_cost):
        if stationA.name in self.train_route.keys():
            if stationB.name in self.train_route[stationA.name].keys():
                print("The stations are already exist")
            else:
                self.train_route[stationA.name][stationB.name] = (time,ticket_cost)
                self.train_route[stationB.name][stationA.name] = (time,ticket_cost)

class Wallet:
    def __init__(self,balance = 0):
        self.balance = balance

    def check_balance(self):
        return {"balance": self.balance}

    def top_up(self,amount):
        self.balance += amount

    def pay_ticket(self,ticket_price):
        self.balance -= ticket_price

# me = Customer('Film','Film555','1234','0812345678','student')
# me.describe_user()
# print()

# A1 = Station('A5','5:30','22:30')
# B3 = Station('B1','5:40','22:40')
# B4 = Station('B4')
#
# print(B4.arrival_time())
# A1.arrival_time(printing=True)
# B3.arrival_time('15:01')
#
# #print(A1.station_arrival_time())
# print()
# Route = Metro_Route()
# Route.get_route(A1,B3)
# Route.get_destination_time(A1,B3)