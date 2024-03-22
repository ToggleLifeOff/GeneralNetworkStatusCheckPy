import requests
import speedtest
import tkinter as tk

CHECK_INTERVAL = 1  # Check connection every 1 second
UNSTABLE_THRESHOLD = 5  # Unstable connection threshold in seconds

def check_internet_connection():
    try:
        # Check connectivity by making a request to a known IP address
        response = requests.get("http://google.com", timeout=10)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException:
        return False

def measure_network_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed

def update_network_status_label(label, info_label):
    if check_internet_connection():
        label.config(text="Network Status: Connected", fg="green")
        label.config(font=('Verdana', 20))
        download_speed, upload_speed = measure_network_speed()
        speed_label.config(text=f"Download: {download_speed:.2f} Mbps\nUpload: {upload_speed:.2f} Mbps")
        info_label.config(text="")
    else:
        label.config(text="Network Status: Interruption", fg="red")
        label.config(font=('Verdana', 20))
        speed_label.config(text="")
        if check_network_connected():
            info_label.config(text="No Internet Access")
        else:
            info_label.config(text="Network Disconnected")

    label.after(CHECK_INTERVAL * 1000, update_network_status_label, label, info_label)

def check_network_connected():
    try:
        response = requests.get("http://www.google.com", timeout=10)
        return True
    except requests.RequestException:
        return False

# Create the main window
window = tk.Tk()
window.title("Network Status")

# Create a label to display the network status
status_label = tk.Label(window, text="Checking...", fg="black", font=("Arial", 18))
status_label.pack(pady=20)

# Create a label to display the network speed
speed_label = tk.Label(window, text="", fg="black", font=("Arial", 14))
speed_label.pack()

# Create a label to display additional information
info_label = tk.Label(window, text="", fg="black", font=("Arial", 14))
info_label.pack()

# Start updating the network status label, network speed label, and info label
update_network_status_label(status_label, info_label)

# Start the main event loop
window.mainloop()
