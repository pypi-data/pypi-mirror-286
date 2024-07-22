import os, time, json, platform, threading, netifaces, pythonping, socket
from concurrent.futures import ThreadPoolExecutor


class config:
    VERSION = "1.0.0"
    AUTHOR = "harimtim"
    DOCUMENTION = "https://github.com/harimtim/OurPy"


def showconfig() -> str:
    try:
        output = f"VERSION: {config.VERSION}\nAUTHOR: {config.AUTHOR}\nDOCUMENTATION: {config.DOCUMENTION}"
        return output
    except:
        pass


def start_in_thread(job, args="") -> None:
    try:
        if args:
            thread = threading.Thread(target=job, args=args)
            thread.start()
        else:
            thread = threading.Thread(target=job)
            thread.start()
    except:
        pass


def clear() -> None:
    try:
        os.system("cls")
    except:
        try:
            os.system("clear")
        except:
            pass


def delay(delay_in_sec) -> None:
    try:
        time.sleep(int(delay_in_sec))
    except:
        pass


def mytime() -> str:
    try:
        return time.strftime("%d.%m.%y : %T")
    except:
        raise


def justtime() -> str:
    try:
        return time.strftime("%T")
    except:
        raise


def load_json(json_file_path) -> None:
    with open(json_file_path, "r") as file:
        return json.load(file)


def save_json(data, json_file_path) -> None:
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)


def myinfo() -> dict:
    try:
        info = {}
        info["OS"] = platform.system()
        info["Version"] = platform.version()
        info["Structure"] = platform.machine()
        return info
    except:
        pass


def start_timer() -> None:
    try:
        return time.time()
    except:
        pass


def get_timer(timer: int) -> None:
    try:
        return f"{round(time.time() - timer, 2)}"
    except:
        pass


def get_online_devices_local() -> list:
    try:
        gateway = netifaces.gateways().get("default", {}).get(netifaces.AF_INET, None)
        if not gateway:
            return []

        base_ip = ".".join(gateway[0].split(".")[:-1]) + "."
        online = []

        def ping_ip(ip):
            response = pythonping.ping(ip, count=1, timeout=0.1)
            if response.success():
                online.append(ip)

        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(ping_ip, [base_ip + str(i) for i in range(1, 256)])

        return online
    except:
        pass


def get_hostname_for_ip(ip) -> str:
    try:
        hostname = socket.gethostbyaddr(ip)
        return hostname[0]
    except:
        pass


def start_local_webpage_server(html, client_limit=10, port=80):
    
    html_bytes = html.encode('utf-8')
    response = b"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: """ + str(len(html_bytes)).encode('utf-8') + b"""

""" + html_bytes
    
    addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
    s = socket.socket()
    
    try:
        s.bind(addr)
        s.listen(client_limit)
        
        print(f"OurPy Webserver started!\nListening on: {socket.gethostbyname(socket.gethostname())}")
        
        while True:
                
            cl, addr = s.accept()
            print("Client connection:", addr)
            
            cl.send(response)
            cl.close()
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        s.close()