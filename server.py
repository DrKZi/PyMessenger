import socket
import sys
import select

host = '127.0.0.1'
port = 8000
inputs = list()
outputs = list()
datalist = []
new_data = []


def get_non_blocking_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    server.bind((host, port))

    server.listen(10)

    return server


def handle_readables(readables, server):
    """
    Обработка появления событий на входах
    """
    for resource in readables:
        if resource is server:
            connection, client_address = resource.accept()
            connection.setblocking(0)
            inputs.append(connection)
            print("Connection from {address}".format(address=client_address))
        else:
            data = ""
            try:
                data = resource.recv(1024).decode()
            except ConnectionResetError:
                pass

            if data[:2] == "M1":
                datastr = data.split('|')
                datalist.append((datastr[2], datastr[3]))
                new_data.append((datastr[2], datastr[3]))
                print(datalist)
                print("{who} said: {what}".format(who=datastr[2], what=datastr[3]))

                if resource not in outputs:
                    outputs.append(resource)
            else:
                clear_resource(resource)


def clear_resource(resource):
    """
    Метод очистки ресурсов использования сокета
    """
    if resource in outputs:
        outputs.remove(resource)
    if resource in inputs:
        inputs.remove(resource)
    resource.close()
    datalist.clear()

    print('Closing connection ' + str(resource))


def handle_writables(writables):
    for resource in inputs:
        try:
            for i in new_data:
                resource.send(i[0].encode())
                resource.send(i[1].encode())
            new_data.clear()
            outputs.remove(resource)
        except OSError:
            clear_resource(resource)


if __name__ == "__main__":
    server_socket = get_non_blocking_server_socket()
    inputs.append(server_socket)

    print('Server running... Press ctrl+C to stop.')

    try:
        while inputs:
            readables, writables, exceptional = select.select(inputs, outputs, inputs)
            handle_readables(readables, server_socket)
            handle_writables(writables)
    except KeyboardInterrupt:
        clear_resource(server_socket)
        print("Server closed!")
