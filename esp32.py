# import network
# import time
# import socket
# import _thread
# import machine
#
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect('Innovation_Guest', '')
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid="ruson's e-ink", authmode=network.AUTH_WPA_WPA2_PSK, password='yanruisong')
#
# time.sleep(20)
#
# srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# srv.bind(('0.0.0.0', 6868))
# srv.listen(1)
#
#
# def f1(conn, client):
#     while True:
#         buff = conn.recv(1)
#         client.send(buff)
#
#
# def f2(conn, client):
#     while True:
#         buff = client.recv(2048)
#         conn.send(buff)
#
#
# while True:
#     conn, addr = srv.accept()
#
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(("103.45.99.3", 6868))
#
#     _thread.start_new_thread(f1, (conn, client))
#     _thread.start_new_thread(f2, (conn, client))
#     p = machine.Pin(2, machine.Pin.OUT)
#     p.value(1)
