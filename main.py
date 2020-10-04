import sys, datetime, copy

class Flight:
    def __init__(self, source, destination, departure, arrival, flight_number, price, bags_allowed, bag_price):
        self.source = source
        self.destination = destination
        self.departure = datetime.datetime.strptime(departure, '%Y-%m-%dT%H:%M:%S')
        self.arrival = datetime.datetime.strptime(arrival, '%Y-%m-%dT%H:%M:%S')
        self.flight_number = flight_number
        self.price = float(price)
        self.bags_allowed = int(bags_allowed)
        self.bag_price = float(bag_price)

class Trip:
    def __init__(self, flights, number_of_bags, bag_price, price):
        self.flights = flights
        self.number_of_bags = int(number_of_bags)
        self.bag_price = float(bag_price)
        self.price = float(price)

def matching(first_flight, second_flight, needed_bags):
    difference = second_flight.departure - first_flight.arrival
    hours = abs(difference.total_seconds()) / 3600
    if first_flight.destination == second_flight.source and second_flight.bags_allowed >= needed_bags and hours >= 1 and hours <= 4:
        return True
    else:
        return False

def findTrip(last_index, flights, trip, result, visited, needed_bags):
    last_flight = flights[last_index]

    # only appends the flight_number, can be changed to include the flight object
    trip.flights.append(last_flight.flight_number)
    trip.price = trip.price + last_flight.price
    trip.bag_price = trip.bag_price + needed_bags * last_flight.bag_price
    result.append(copy.deepcopy(trip))
    visited[last_flight.destination] = True

    for index in range(last_index + 1, len(flights)):
        current_flight = flights[index]
        if matching(last_flight, current_flight, needed_bags) and not visited[current_flight.destination]:
            findTrip(index, flights, trip, result, visited, needed_bags)
            visited[current_flight.destination] = False
            trip.price = trip.price - current_flight.price
            del trip.flights[-1]
    return result

def main():
    flights = []
    visited = {}

    # CSV INPUT
    try:
        for line in sys.stdin.readlines()[1:]:
            if 'Exit' == line.rstrip():
                break
            line = line.split(',')
            flights.append(Flight(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))
            visited[line[0]] = False
            visited[line[1]] = False
    except:
        print("ERROR: Bad input file formatting", file=sys.stderr)
        return

    # DEBUGGING INPUT
    # input_array = [
    #     "USM,HKT,2017-02-11T06:25:00,2017-02-11T07:25:00,A,24,1,9",
    #     "HKT,USM,2017-02-11T08:35:00,2017-02-11T11:30:00,B,23,1,15",
    #     "HKT,USM,2017-02-11T08:35:00,2017-02-11T21:30:00,C,23,1,15",
    #     "HKT,USM,2017-02-11T08:35:00,2017-02-11T21:30:00,D,23,1,15"
    # ]
    # for line in input_array:
    #     line = line.split(',')
    #     flights.append(Flight(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))
    #     visited[line[0]] = False
    #     visited[line[1]] = False

    flights.sort(key=lambda f : f.arrival)

    for number_of_bags in range(0, 3):
        print("NUMBER OF BAGS: ", number_of_bags)
        print("-------------------------------------")
        visited = {key: False for key, value in visited.items()}
        for index in range(len(flights)):
            if number_of_bags <= flights[index].bags_allowed:
                result = findTrip(index, flights, Trip([], number_of_bags, 0, 0), [], visited, number_of_bags)
                for t in result:
                    print('Flights Numbers: {} Total Price: {}$ Total Bag Price: {}$'.format(t.flights, t.price, t.bag_price))
        print("-------------------------------------")

if __name__ == "__main__":
    main()
