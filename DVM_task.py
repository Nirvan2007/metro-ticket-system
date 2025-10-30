from delhi_metro_lines import * # type: ignore
import csv

class Station:

    def __init__(self,station_name,line = None,position = None,adj = None):
        self.station_name = station_name
        self.line = line
        self.position = position
        self.adj = adj
        self.id = [self.line[0] + "_" + str(self.position[0])]

    def add_line(self,line,position):
        if self.line == None:
            self.line = []
            self.line.append(line)
        else:
            self.line.append(line)
        if self.position == None:
            self.position = []
            self.position.append(position)
        else:
            self.position.append(position)

    def update_id(self,line,position):
        self.id.append(line + "_" + str(position))

    def system(self,Lines,Stations):
        for i in range (0,len(self.line)):
            self.adj = []
            cur_line = self.line[i]
            cur_line_list = getattr(Lines, cur_line)
            for j in range(len(Stations)):
                if Stations[j].id == self.id:
                    if self.position[i] == 1:
                        self.adj.append(Stations[j+1])
                    elif self.position[i] == cur_line_list[-1][2]:
                        self.adj.append(Stations[j-1])
                    else:
                        if j == len(Stations) - 1:
                            self.adj.append(Stations[j-1])
                        else:
                            self.adj.append(Stations[j+1])
                            self.adj.append(Stations[j-1])
                    break
        if len(self.line) > 1:
            for new in Stations:
                if new.station_name == self.station_name and new != self:
                    self.adj.append(new.station_name)

class Line:
    def __init__(self):
        self.red_line = stations_red_line # type: ignore
        self.blue_line_main = stations_blue_line_main # type: ignore
        self.blue_line_branch = stations_blue_line_branch # type: ignore
        self.green_line_main = stations_green_line_main # type: ignore
        self.yellow_line = stations_yellow_line # type: ignore
        self.violet_line = stations_violet_line # type: ignore
        self.green_line_branch = stations_green_line_branch # type: ignore
        self.airport_express_line = stations_airport_express_line # type: ignore
        self.magenta_line = stations_magenta_line # type: ignore
        self.pink_line = stations_pink_line # type: ignore
        self.grey_line = stations_grey_line # type: ignore


class Ticket:
    ticket_id = 0
    price_perstation = 10

    def __init__(self,start,end,path):
        Ticket.ticket_id += 1
        self.ticket_id = Ticket.ticket_id
        self.start = start 
        self.end = end 
        self.path = path

    @classmethod
    def change_price(price):
        Ticket.price = price

    def calc_price(self,path):
        return ((len(self.path)-1)*self.price_perstation)

    def directions(self,path,Stations):
        dirn = [] 
        for i in range(0, len(self.path)-1):
            station1 = get_station_by_name(self.path[i],Stations)
            station2 = get_station_by_name(self.path[i+1],Stations)
            commonline = None
            for line_a in station1.line:
                for line_b in station2.line:
                    if line_a == line_b:
                        commonline = line_a
                        break
                if commonline != None:
                    break
            if i == 0:
                if commonline != None:
                    cur_line = commonline
                else:
                    cur_line = station1.line[0]
                direction = " start from " + cur_line + " from " + station1.station_name
                dirn.append(direction)
            if commonline == None:
                line_new = station2.line[0]
                direction = "change at " + station1.station_name + " from " + cur_line + " to " + line_new
                dirn.append(direction)
            else:
                cur_line = commonline
        direction = "Leave metro at " + path[-1]
        dirn.append(direction)
        return dirn

    def __str__(self):
        return str(self.ticket_id)


def input_data():
    f = open("Station_data.csv","w",newline="")
    writer = csv.writer(f)
    writer.writerows(stations_red_line)# type: ignore
    writer.writerows(stations_blue_line_main)# type: ignore
    writer.writerows(stations_blue_line_branch)# type: ignore
    writer.writerows(stations_green_line_main)# type: ignore
    writer.writerows(stations_yellow_line)# type: ignore
    writer.writerows(stations_violet_line)# type: ignore
    writer.writerows(stations_green_line_branch)# type: ignore
    writer.writerows(stations_pink_line)# type: ignore
    writer.writerows(stations_airport_express_line)# type: ignore
    writer.writerows(stations_magenta_line)# type: ignore
    writer.writerows(stations_grey_line)# type: ignore
    f.close()


def file_exists():
    try:
        f = open("Station_data.csv","r",newline="")
        f.close()
        return True
    except FileNotFoundError:
        return False


def load_data():
    f = open("Station_data.csv","r",newline="")
    reader = csv.reader(f)
    Stations = []
    Stations_name = []
    for data in reader:
        if data[0] not in Stations_name:
            Stations_name.append(data[0])
            cls = Station(data[0],[data[1],],[data[2],])
            Stations.append(cls)
        else:
            for i in Stations:
                if i.station_name == data[0]:
                    i.add_line(data[1],data[2])
                    i.update_id(data[1],data[2])
    f.close()
    return Stations,Stations_name


def get_station(id,Stations):
        for i in Stations:
            if id in i.id:
                return i


def get_station_by_name(name, Stations):
    for st in Stations:
        if st.station_name == name:
            return st
    return None         


def shortest_path(start, stop, Stations):
    L = [(start, [start.station_name])]  
    visited = {start.station_name}         

    while L:
        current, path = L.pop(0)
        if current.station_name == stop.station_name:
            return path      
        for adj_name in current.adj:
            if adj_name.station_name not in visited:
                neighbor = adj_name
                visited.add(adj_name.station_name)
                L.append((neighbor, path + [adj_name.station_name]))
    return None


def main():
    Lines = Line()
    Tickets_purchased = []
    input_data()
    Stations,Stations_name = load_data()
    for st in Stations:
        st.system(Lines,Stations)
    while True:
        print("Enter 1 to see all stations, Enter 2 to Purchase Ticket, Enter 3 to see purchased tickets, Enter anything else to exit")
        ch = int(input("Enter choice: "))
        if ch == 1:
            for st in Stations:
                print(st.station_name)
        elif ch == 2:
            for i in range(0,len(Stations)):
                print(i+1,Stations[i].station_name)
            start_n = int(input("Enter start station serial number: "))
            end_n = int(input("Enter end station serial number: "))
            start = Stations[start_n-1]
            end = Stations[end_n -1]
            path = shortest_path(start,end,Stations)
            ticket = Ticket(start,end,path)
            Tickets_purchased.append(ticket)
            ticket.price = ticket.calc_price(path)
            directions = ticket.directions(path,Stations)
            print("Ticket price is: ",ticket.price)
            print("Path is : ")
            for i in path:
                print(i," - ",end ="")
            for i in directions:
                print(i,"\n")
        elif ch == 3:
            print("Ticket_id of purchased tickets: " )
            for i in Tickets_purchased:
                print(i,"(Start : ",i.start.station_name,"and end = ", i.end.station_name,") Price:", i.price)               
        else:
            break

main()
