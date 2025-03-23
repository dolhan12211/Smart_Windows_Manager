import datetime
import random

class Window:
    def __init__(self, name, room):
        self.name = name
        self.room = room
        self.is_open = False
    
    def open_window(self):
        self.is_open = True
        print(f"{self.name} w pokoju {self.room} zostało otwarte.")
    
    def close_window(self):
        self.is_open = False
        print(f"{self.name} w pokoju {self.room} zostało zamknięte.")
    
    def get_status(self):
        return "otwarte" if self.is_open else "zamknięte"

class Room:
    def __init__(self, name):
        self.name = name
        self.windows = []
    
    def add_window(self, window):
        self.windows.append(window)
    
    def set_windows_default(self, default_open=False):
        for window in self.windows:
            if default_open:
                window.open_window()
            else:
                window.close_window()
    
    def night_mode(self, hour):
        if hour >= 22 or hour < 6:
            print(f"Tryb nocny włączony w pokoju {self.name}. Zamykam okna.")
            for window in self.windows:
                window.close_window()

class WindowControlSystem:
    def __init__(self):
        self.rooms = {}
        self.ventilation_stats = {}
    
    def add_room(self, room):
        self.rooms[room.name] = room
    
    def operate_windows(self, hour):
        for room in self.rooms.values():
            room.night_mode(hour)
            self.log_ventilation(room)
    
    def log_ventilation(self, room):
        if room.name not in self.ventilation_stats:
            self.ventilation_stats[room.name] = {'open_count': 0, 'air_quality': []}
        
        open_windows = sum(1 for w in room.windows if w.is_open)
        self.ventilation_stats[room.name]['open_count'] += open_windows
        self.ventilation_stats[room.name]['air_quality'].append(random.uniform(50, 100))  # Symulacja jakości powietrza
    
    def generate_report(self):
        print("\n--- Raport Wentylacji ---")
        for room, stats in self.ventilation_stats.items():
            avg_air_quality = sum(stats['air_quality']) / len(stats['air_quality'])
            print(f"Pokój: {room}, Ilość otwarć: {stats['open_count']}, Średnia jakość powietrza: {avg_air_quality:.2f}")

# Tworzenie systemu sterowania
system = WindowControlSystem()

# Dodawanie pokoi i okien
dom = [Room("Salon"), Room("Sypialnia"), Room("Kuchnia")]
for room in dom:
    system.add_room(room)
    for i in range(2):
        room.add_window(Window(f"Okno {i+1}", room.name))
    room.set_windows_default(default_open=False)

# Symulacja pracy systemu
for hour in range(0, 24, 6):  # Co 6 godzin
    print(f"\nGodzina: {hour}:00")
    system.operate_windows(hour)

# Generowanie raportu
system.generate_report()
