from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from metrobot import find_route, calculate_fare # Importing the function from metrochatbot.py
from metrobot import metro_chatbot

BG_COLOR = "#1E1E1E"  
TEXT_COLOR = "#FFFFFF" 
USER_BUBBLE = "#4d7de2" 
BOT_BUBBLE = "#3A3A3A"  
ENTRY_BG = "#333333"  
BUTTON_BG = "#444444"  
FONT = ("Helvetica", "12")
BOT_NAME = "Cairo Metro Bot"

class MetroChatbotGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Cairo Metro Chatbot")
        self.window.geometry("550x600")
        self.window.configure(bg=BG_COLOR)
        self._load_images()
        self._setup_main_window()
        self.interchange_buttons = [] 
    
    def run(self):
        self.window.mainloop()
    
    def _load_images(self):
        self.user_img = Image.open(r"C:\Users\Mai\Downloads\user.png")
        self.user_img = self.user_img.resize((40, 40), Image.LANCZOS)
        self.user_img = ImageTk.PhotoImage(self.user_img)
        
        self.bot_img = Image.open(r"C:\Users\Mai\Downloads\bot.png")
        self.bot_img = self.bot_img.resize((40, 40), Image.LANCZOS)
        self.bot_img = ImageTk.PhotoImage(self.bot_img)
    
    def _setup_main_window(self):
        
        header = Label(self.window, text="🤖 Route Scout 🔎\nFinds your track, no looking back!", font=("Arial", "20", "bold italic"), fg=TEXT_COLOR, bg=BG_COLOR, pady=10)
        header.pack(fill=X)
        

        self.chat_frame = Frame(self.window, bg=BG_COLOR, borderwidth=3, relief="sunken")
        self.chat_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)
        
        self.canvas = Canvas(self.chat_frame, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, command=self.canvas.yview, style="TScrollbar")
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.message_frame = Frame(self.canvas, bg=BG_COLOR)
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.message_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        

        input_frame = Frame(self.window, bg=BG_COLOR)
        input_frame.pack(fill=X, padx=10, pady=10)
        
        self.msg_entry = Entry(input_frame, font=FONT, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR, bd=2, relief=FLAT)
        self.msg_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10), pady=5)
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        send_button = Button(input_frame, text="➤", font=("Segoe UI", 14), bg=BUTTON_BG, fg=TEXT_COLOR, bd=0, relief=FLAT, command=lambda: self._on_enter_pressed(None))
        send_button.pack(side=RIGHT)
        

        self._insert_message("🤖 Welcome to the Route Scout! How can I help you today?", BOT_NAME, BOT_BUBBLE, "w", self.bot_img, rate=False)
    
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get().strip()
        if msg:
            self._insert_message(msg, "You", USER_BUBBLE, "e", self.user_img)
            self._process_user_input(msg)
    

    def _process_user_input(self, msg):
        msg_lower = msg.lower()

        if any(word in msg_lower for word in ["bye", "exit", "quit"]):
            response = "Goodbye! Have a great day! 👋"
        elif any(word in msg_lower for word in ["thank", "thanks"]):
            response = "You're welcome! 😊 Let me know if you need anything else."

        elif "how many lines" in msg_lower:
            response = "The Cairo Metro has 3 lines:\n🚆 Line 1 (Blue)\n🚆 Line 2 (Red)\n🚆 Line 3 (Green)"
        elif "ticket price" in msg_lower or "fare" in msg_lower:
            response = "🎟️ Ticket Prices:\n📍 1-9 stops = 8 EGP\n📍 10-16 stops = 10 EGP\n📍 17-23 stops = 15 EGP\n📍 24+ stops = 20 EGP\n♿ People of Determination = 5 EGP"


        elif "route" in msg_lower or ("from" in msg_lower and "to" in msg_lower):
            stations = msg.split("from")[-1].split("to")
            if len(stations) == 2:
                start = stations[0].strip().title()
                end = stations[1].strip().title()
                self._insert_message(f"Finding route from {start} to {end}...", BOT_NAME, BOT_BUBBLE, "w", self.bot_img)

   
                route_info, stop_count_or_routes = find_route(start, end)
                self._insert_message(route_info, BOT_NAME, BOT_BUBBLE, "w", self.bot_img)

                if isinstance(stop_count_or_routes, list):  
                    self._show_interchange_buttons(stop_count_or_routes)
                else:

                    ticket_price = calculate_fare(stop_count_or_routes)
                    self._insert_message(f"🎫 Ticket Price: {ticket_price} EGP", BOT_NAME, BOT_BUBBLE, "w", self.bot_img)
            return

        else:
            response = "I didn't quite understand. Try asking about routes, ticket prices, or metro lines."


        self._insert_message(response, BOT_NAME, BOT_BUBBLE, "w", self.bot_img)

    def _show_interchange_buttons(self, possible_routes):
        for button in self.interchange_buttons:
            button.destroy()

        self.interchange_buttons = []

        for i, (interchange, stops_to, stops_from, total) in enumerate(possible_routes):
            btn = Button(self.window, text=f"🔄 {interchange} - {total} stops", font=FONT, bg=BUTTON_BG, fg=TEXT_COLOR, command=lambda i=i: self._handle_route_choice(i, possible_routes))
            btn.pack(pady=5)
            self.interchange_buttons.append(btn)  
    
    def _handle_route_choice(self, index, possible_routes):
        for button in self.interchange_buttons:
            button.destroy()

        self.interchange_buttons = []


        best_option = possible_routes[index]
        interchange_station = best_option[0]
        start_to_interchange_stops = best_option[1]  
        interchange_to_end_stops = best_option[2]    
        total_stops = best_option[3]                 

        
        ticket_price = calculate_fare(total_stops)

        route_message = (
            f"🚆 Take {interchange_station} from your starting station to {interchange_station} ({start_to_interchange_stops} stops).\n"
            f"🔄 Switch at {interchange_station}.\n"
            f"🚆 Continue to your destination ({interchange_to_end_stops} stops).\n"
            f"🎫 Total stops: {total_stops}.\n"
            f"💰 Ticket Price: {ticket_price} EGP"
        )


        self._insert_message(route_message, BOT_NAME, BOT_BUBBLE, "w", self.bot_img)


    def _insert_message(self, msg, sender, bubble_color, align, img, rate=True):
        self.msg_entry.delete(0, END)
        
        msg_frame = Frame(self.message_frame, bg=BG_COLOR)
        
        if align == "e":
            Label(msg_frame, image=img, bg=BG_COLOR).pack(side=RIGHT, padx=5)
            Label(msg_frame, text=msg, font=FONT, bg=bubble_color, fg=TEXT_COLOR, wraplength=400, padx=10, pady=5).pack(side=RIGHT, ipadx=10, ipady=5)
        else:
            Label(msg_frame, image=img, bg=BG_COLOR).pack(side=LEFT, padx=5)
            Label(msg_frame, text=msg, font=FONT, bg=bubble_color, fg=TEXT_COLOR, wraplength=400, padx=10, pady=5).pack(side=LEFT, ipadx=10, ipady=5)
        
        msg_frame.pack(anchor=align, padx=10, pady=5)

        self.window.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = MetroChatbotGUI()
    app.run()
