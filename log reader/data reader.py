import codecs


def read_file(file_name):
    lines = []
    all_data = []
    error_data = []

    with codecs.open(file_name, 'rb', 'utf-8', errors='replace') as f:
        for line in f:
            lines.append(line.strip())

    for i in range(len(lines)):
        try:
            #print(i, lines[i])
            lines[i] = lines[i].split(" - - ")  #get the host name
            data = lines[i][1].split()
            new_data = [lines[i][0]]        #split the time, object, response_code, transfer_size
            for j in data:
                new_data.append(j)
            all_data.append(new_data)
        except IndexError:                  #some requests were malformed, save it as error
            error_data.append(lines[i][0])
            continue

    return all_data, error_data  #return two lists, one is error


def get_total_bytes(data_list):
    total = 0
    for data in data_list:              #read one line of log file
        # get the last item then convert to integer, if it is "-" then it's not convertable
        try:
            int_transfer = int(data[-1])

            total += int_transfer

        except ValueError:
            continue
    return total


def get_list_response_code(data_list):      #get the response code, store in a dictionary
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


if __name__ == "__main__":
    available = read_file("access_log.txt")[0]

    print("total bytes: ", get_total_bytes(available) / 1000000)
    print("average bytes: ", get_total_bytes(available) / 352 / 1000000)
    print('response code: ', get_list_response_code(available))
    print('clients number: ', get_local_remote_number(available))
    print("total request by host: ", total_data_transfer_by_host(available))
