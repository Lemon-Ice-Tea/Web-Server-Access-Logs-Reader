

def read_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()
    lines = [line.strip() for line in lines]
    all_data = []
    error_data = []

    for i in range(len(lines)):
        try:
            print(i, lines[i])
            lines[i] = lines[i].split(" - - ")  #get the host name
            data = lines[i][1].split()
            new_data = [lines[i][0]]        #split the time, object, response_code, transfer_size
            for j in data:
                new_data.append(j)
            all_data.append(new_data)
        except IndexError:
            error_data.append(lines[i][0])
            continue

    return all_data, error_data


def get_total_bytes(data_list):
    count = 0
    total = 0
    for data in data_list:
        count += 1

        try:
            int_transfer = int(data[-1])

            total += int_transfer

        except ValueError:
            continue
    return total


def get_list_response_code(data_list):
    response_code = {}
    for data in data_list:
        try:
            response = int(data[-2])
            if 400 <= response <= 499:
                response = "4XX"
            elif 500 <= response <= 599:
                response = "5XX"

            if response not in response_code:
                response_code[response] = 1

            else:
                response_code[response] += 1


        except ValueError:
            continue
    return response_code


def get_local_remote_number(data_list):
    host_dict = {}
    for data in data_list:
        host = data[0]
        if host not in host_dict:
            host_dict[host] = 1
        else:
            host_dict[host] += 1
    return host_dict


def total_data_transfer_by_host(data_list):
    host_dict = {}
    for data in data_list:
        try:
            host = data[0]
            bytes_trans = int(data[-1])
            if host not in host_dict:
                host_dict[host] = bytes_trans
            else:
                host_dict[host] += bytes_trans
        except ValueError:
            continue
    return host_dict


def add_data(data_list, error_list):
    global available
    global error
    for i in data_list:
        available.append(i)
    for j in error_list:
        error.append(j)


if __name__ == "__main__":
    #available = []
    #error = []
    count = 0
    """
        for i in range(8):

        file_name = f"log{i}.txt"
        data_list, error_list = read_file(file_name)
        print(i)
        add_data(data_list, error_list)
    """
    available = read_file("test_data")[0]

    print("total bytes: ", get_total_bytes(available) / 1000000)
    print("average bytes: ", get_total_bytes(available) / 352 / 1000000)
    print('response code: ', get_list_response_code(available))
    print('clients number: ', get_local_remote_number(available))
    print("total request by host: ", total_data_transfer_by_host(available))
