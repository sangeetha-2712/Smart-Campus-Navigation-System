import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import heapq
import math

class CampusNavigationApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Campus Navigation System")
        root.geometry("1050x680")
        self.graph = {
            "Main Gate": {"Department Block": 4, "Canteen": 2},
            "Department Block": {"Main Gate": 4, "Canteen": 1, "Library": 5},
            "Canteen": {"Main Gate": 2, "Department Block": 1, "Hostel": 7},
            "Library": {"Department Block": 5, "Hostel": 2},
            "Hostel": {"Canteen": 7, "Library": 2}
        }
        self.positions = {
            "Main Gate": (100, 250), "Department Block": (330, 130),
            "Canteen": (330, 390), "Library": (650, 130), "Hostel": (650, 390)
        }
        self.route = []
        self.start = tk.StringVar()
        self.end = tk.StringVar()
        self.build_ui()
        self.refresh()
        self.draw()

    def build_ui(self):
        tk.Label(self.root, text="SMART CAMPUS NAVIGATION SYSTEM",
                 font=("Times New Roman", 20, "bold"), bg="#17365D",
                 fg="white", pady=15).pack(fill="x")
        body = tk.Frame(self.root, padx=12, pady=12)
        body.pack(fill="both", expand=True)
        panel = tk.Frame(body, width=270, padx=12, pady=12, bg="#F1F4F8")
        panel.pack(side="left", fill="y")
        panel.pack_propagate(False)
        tk.Label(panel, text="NAVIGATION", font=("Times New Roman", 14, "bold"),
                 bg="#F1F4F8").pack(anchor="w", pady=8)
        tk.Label(panel, text="Starting location", bg="#F1F4F8").pack(anchor="w")
        self.start_box = ttk.Combobox(panel, textvariable=self.start, state="readonly")
        self.start_box.pack(fill="x", pady=5)
        tk.Label(panel, text="Destination", bg="#F1F4F8").pack(anchor="w")
        self.end_box = ttk.Combobox(panel, textvariable=self.end, state="readonly")
        self.end_box.pack(fill="x", pady=5)
        self.button(panel, "Find Shortest Path", self.find, "#1F6AA5")
        self.button(panel, "Clear Route", self.clear, "#64748B")
        ttk.Separator(panel).pack(fill="x", pady=12)
        tk.Label(panel, text="GRAPH MANAGEMENT", font=("Times New Roman", 14, "bold"),
                 bg="#F1F4F8").pack(anchor="w", pady=6)
        self.button(panel, "Add New Location", self.add_location, "#27864B")
        self.button(panel, "Add Road / Distance", self.add_road, "#27864B")
        tk.Label(panel, text="RESULT", font=("Times New Roman", 14, "bold"),
                 bg="#F1F4F8").pack(anchor="w", pady=(12, 5))
        self.result = tk.Text(panel, height=10, width=29, wrap="word",
                              font=("Times New Roman", 11))
        self.result.pack(fill="x")
        self.show_result("Select a starting location and destination.")
        tk.Label(panel, text="Red = shortest route | Grey = road",
                 bg="#F1F4F8", wraplength=230).pack(anchor="w", pady=10)
        area = tk.Frame(body, bg="white", bd=1, relief="solid")
        area.pack(side="right", fill="both", expand=True, padx=(12, 0))
        tk.Label(area, text="CAMPUS ROAD NETWORK",
                 font=("Times New Roman", 14, "bold"), bg="white").pack(pady=8)
        self.canvas = tk.Canvas(area, bg="#FAFCFF", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)

    def button(self, parent, text, command, color):
        tk.Button(parent, text=text, command=command, bg=color, fg="white",
                  font=("Times New Roman", 11, "bold"), relief="flat",
                  pady=7).pack(fill="x", pady=4)

    def show_result(self, text):
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)

    def refresh(self):
        names = sorted(self.graph)
        self.start_box["values"] = names
        self.end_box["values"] = names
        if self.start.get() not in names:
            self.start.set(names[0])
        if self.end.get() not in names:
            self.end.set(names[-1])

    def draw(self):
        self.canvas.delete("all")
        seen = set()
        for a, neighbours in self.graph.items():
            for b, distance in neighbours.items():
                key = tuple(sorted((a, b)))
                if key in seen:
                    continue
                seen.add(key)
                x1, y1 = self.positions[a]
                x2, y2 = self.positions[b]
                chosen = any({self.route[i], self.route[i+1]} == {a, b}
                             for i in range(len(self.route)-1))
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill="#E53935" if chosen else "#94A3B8",
                                        width=5 if chosen else 2)
                mx, my = (x1+x2)/2, (y1+y2)/2
                self.canvas.create_rectangle(mx-14, my-11, mx+14, my+11,
                                             fill="white", outline="")
                self.canvas.create_text(mx, my, text=str(distance),
                                         font=("Times New Roman", 10, "bold"))
        for name, (x, y) in self.positions.items():
            if name not in self.graph:
                continue
            color = "#E53935" if name in self.route else "#1F6AA5"
            self.canvas.create_oval(x-38, y-30, x+38, y+30,
                                    fill=color, outline="white", width=2)
            self.canvas.create_text(x, y, text=name, fill="white",
                                    font=("Times New Roman", 9, "bold"),
                                    width=70, justify="center")

    def dijkstra(self, source, destination):
        # Min-heap stores (distance, vertex); previous reconstructs the path.
        distances = {v: math.inf for v in self.graph}
        previous = {v: None for v in self.graph}
        distances[source] = 0
        queue = [(0, source)]
        while queue:
            current_distance, current = heapq.heappop(queue)
            if current_distance > distances[current]:
                continue
            if current == destination:
                break
            for neighbour, weight in self.graph[current].items():
                new_distance = current_distance + weight
                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    previous[neighbour] = current
                    heapq.heappush(queue, (new_distance, neighbour))
        if distances[destination] == math.inf:
            return math.inf, []
        path, current = [], destination
        while current is not None:
            path.append(current)
            current = previous[current]
        return distances[destination], list(reversed(path))

    def find(self):
        source, destination = self.start.get(), self.end.get()
        distance, path = self.dijkstra(source, destination)
        self.route = path
        self.draw()
        if not path:
            self.show_result("No route exists between these locations.")
        else:
            self.show_result("START: " + source + "\nDESTINATION: " + destination +
                             "\n\nSHORTEST ROUTE:\n" + "\n  ↓\n".join(path) +
                             f"\n\nTOTAL DISTANCE: {distance:g} units")

    def clear(self):
        self.route = []
        self.draw()
        self.show_result("Select a starting location and destination.")

    def add_location(self):
        name = simpledialog.askstring("Add Location", "Enter location name:")
        if name is None:
            return
        name = name.strip()
        if not name or name in self.graph:
            messagebox.showwarning("Invalid location",
                                   "Enter a non-empty name that is not already used.")
            return
        self.graph[name] = {}
        n = len(self.positions)
        angle = n * 2.4
        self.positions[name] = (int(420 + (170+n//7*60)*math.cos(angle)),
                                int(270 + (170+n//7*60)*math.sin(angle)))
        self.refresh()
        self.draw()
        self.show_result(f"Location '{name}' added. Add a road to connect it.")

    def add_road(self):
        names = sorted(self.graph)
        a = simpledialog.askstring("Add Road", "First location:\n" + ", ".join(names))
        if a is None: return
        b = simpledialog.askstring("Add Road", "Second location:\n" + ", ".join(names))
        if b is None: return
        a, b = a.strip(), b.strip()
        if a not in self.graph or b not in self.graph or a == b:
            messagebox.showerror("Invalid road", "Choose two different existing locations.")
            return
        distance = simpledialog.askfloat("Road Distance",
                                         "Enter positive distance in units:",
                                         minvalue=0.000001)
        if distance is None: return
        self.graph[a][b] = distance
        self.graph[b][a] = distance
        self.route = []
        self.draw()
        self.show_result(f"Road added:\n{a} ↔ {b}\nDistance: {distance:g} units")


if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationApp(root)
    root.mainloop()
