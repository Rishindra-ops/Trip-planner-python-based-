import tkinter as tk
from PIL import Image, ImageTk
import datetime
import random
from tkinter import ttk, messagebox
from typing import List, Dict, Optional
import os


class TripPlanner:
    DEST_FACTS: Dict[str, List[str]] = {
        "tamil nadu": [
            "Did you know? Tamil Nadu is home to over 33,000 ancient temples!",
            "Chennai's Marina Beach is the second longest urban beach in the world.",
        ],
        "kerala": [
            "Kerala is known as 'God's Own Country'.",
            "Kerala has the highest literacy rate among Indian states.",
        ],
        "karnataka": [
            "Karnataka's Hampi is a UNESCO World Heritage Site.",
            "Bangalore is known as the Silicon Valley of India.",
        ],
        "telangana": [
            "Hyderabad, the capital of Telangana, is known as the City of Pearls.",
            "Charminar, an iconic monument, was built in 1591 in Hyderabad.",
        ],
    }

    TRIP_QUOTES: List[str] = [
        "Travel is the only thing you buy that makes you richer.",
        "The journey of a thousand miles begins with a single step.",
        "Adventure is worthwhile.",
        "Jobs fill your pockets, adventures fill your soul."
    ]

    def __init__(self):
        self.destination: str = ""
        self.start_date: Optional[datetime.datetime] = None
        self.end_date: Optional[datetime.datetime] = None
        self.budget: float = 0.0
        self.activities: List[str] = []
        self.suggestions: Dict[str, str] = {}
        self.places: List[str] = []
        self.trip_name: str = ""

    def validate_destination(self, destination: str) -> bool:
        return destination.lower() in self.DEST_FACTS

    def validate_dates(self, start_date: datetime.datetime, end_date: datetime.datetime) -> bool:
        return start_date <= end_date

    def set_destination(self, destination: str) -> bool:
        if self.validate_destination(destination):
            self.destination = destination
            return True
        return False

    def set_dates(self, start_date_str: str, end_date_str: str) -> bool:
        try:
            start = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
            if self.validate_dates(start, end):
                self.start_date = start
                self.end_date = end
                return True
        except ValueError:
            pass
        return False

    def set_budget(self, budget: float) -> bool:
        if budget >= 0:
            self.budget = budget
            return True
        return False

    def add_activity(self, activity: str) -> bool:
        if activity.strip():
            self.activities.append(activity)
            return True
        return False

    def generate_trip_name(self) -> str:
        themes = ["Adventure", "Escape", "Odyssey", "Expedition", "Retreat", "Quest", "Voyage"]
        self.trip_name = f"{random.choice(themes)} to {self.destination.title()}"
        return self.trip_name

    def generate_suggestions(self) -> Dict[str, str]:
        if self.budget < 10000:
            self.suggestions = {
                "Travel": "🚌 Consider using budget transportation options like buses or trains.",
                "Accommodation": "🏠 Opt for budget accommodations like hostels or staying with friends/family.",
                "Activities": "🎯 Focus on free or low-cost activities such as hiking, sightseeing, or local events.",
                "Planning": "⏰ According to the budget, try to complete the trip in 2-3 days."
            }
        elif 10000 <= self.budget <= 20000:
            self.suggestions = {
                "Travel": "🚂 You can explore economy flights or train travel for longer distances.",
                "Accommodation": "🏨 Mid-range hotels or vacation rentals could fit within your budget.",
                "Activities": "🎨 Plan for a mix of free and paid activities, such as museums, local tours, and dining out.",
                "Planning": "📅 As the budget is a little flexible, plan the trip for 4 days."
            }
        else:
            self.suggestions = {
                "Travel": "✈ You have the flexibility to book flights or rent a car for convenience.",
                "Accommodation": "🏰 Consider luxury hotels, resorts, or premium vacation rentals.",
                "Activities": "🎭 Enjoy premium activities like guided tours, adventure sports, or fine dining.",
                "Planning": "🗓 With a generous budget, you can stay for a week!"
            }
        self.add_places()
        return self.suggestions

    def add_places(self) -> List[str]:
        places_dict = {
            "tamil nadu": [
                "Chennai - Marina Beach, Kapaleeshwarar Temple",
                "Madurai - Meenakshi Amman Temple",
                "Ooty - Botanical Gardens, Nilgiri Mountain Railway",
                "Kanyakumari - Vivekananda Rock Memorial"
            ],
            "kerala": [
                "Munnar - Tea Gardens, Eravikulam National Park",
                "Alleppey - Backwaters, Houseboats",
                "Kochi - Fort Kochi, Chinese Fishing Nets",
                "Thekkady - Periyar Wildlife Sanctuary"
            ],
            "karnataka": [
                "Bangalore - Lalbagh, Cubbon Park",
                "Mysore - Mysore Palace, Brindavan Gardens",
                "Hampi - Vijaya Vittala Temple, Stone Chariot",
                "Coorg - Abbey Falls, Coffee Plantations"
            ],
            "telangana": [
                "Hyderabad - Charminar, Golconda Fort, Hussain Sagar Lake",
                "Warangal - Warangal Fort, Thousand Pillar Temple",
                "Nizamabad - Pocharam Wildlife Sanctuary",
                "Nagarjuna Sagar - Nagarjuna Sagar Dam"
            ]
        }
        self.places = places_dict.get(self.destination.lower(), [])
        return self.places

    def get_random_fact(self) -> str:
        facts = self.DEST_FACTS.get(self.destination.lower(), [])
        return random.choice(facts) if facts else "Every journey creates its own story!"

    def get_random_quote(self) -> str:
        return random.choice(self.TRIP_QUOTES)

    def get_trip_summary(self) -> Dict:
        return {
            "trip_name": self.trip_name,
            "destination": self.destination,
            "start_date": self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            "end_date": self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            "duration": (self.end_date - self.start_date).days if self.start_date and self.end_date else 0,
            "budget": self.budget,
            "activities": self.activities,
            "suggestions": self.suggestions,
            "places": self.places,
            "fact": self.get_random_fact(),
            "quote": self.get_random_quote()
        }


class TripPlannerGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Creative Trip Planner")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f0f0f0')

        self.planner = TripPlanner()
        self.activities_list = []

        self.create_widgets()

    def create_widgets(self):
        # Main heading
        heading_label = tk.Label(self.window,
                                 text='🧾 TRIP PLANNER 🧾',
                                 font=("times new roman", 30, "bold"),
                                 bg='gray20',
                                 fg='white',
                                 bd=14,
                                 relief=tk.GROOVE)
        heading_label.pack(fill=tk.X)

        # Main container with background
        main_frame = tk.Frame(self.window, bg='gray20', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Frame for basic details
        left_frame = tk.LabelFrame(main_frame,
                                   text="✈ Trip Details",
                                   font=("times new roman", 15, "bold"),
                                   bg='gray20',
                                   fg='white',
                                   bd=8,
                                   relief=tk.GROOVE,
                                   padx=10,
                                   pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Left frame content
        self.create_left_frame_content(left_frame)

        # Right Frame for activities and results
        right_frame = tk.LabelFrame(main_frame,
                                    text="🎯 Activities & Summary",
                                    font=("times new roman", 15, "bold"),
                                    bg='gray20',
                                    fg='white',
                                    bd=8,
                                    relief=tk.GROOVE,
                                    padx=10,
                                    pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Right frame content
        self.create_right_frame_content(right_frame)

    def create_left_frame_content(self, frame):
        # Destination
        tk.Label(frame,
                 text="Destination:",
                 font=("arial", 12),
                 bg='gray20',
                 fg='white').grid(row=0, column=0, sticky=tk.W, pady=5)

        self.destination_var = tk.StringVar()
        destination_combo = ttk.Combobox(frame,
                                         textvariable=self.destination_var,
                                         font=("arial", 12),
                                         width=25)
        destination_combo['values'] = ('Tamil Nadu', 'Kerala', 'Karnataka', 'Telangana')
        destination_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        # Dates
        tk.Label(frame,
                 text="Start Date (YYYY-MM-DD):",
                 font=("arial", 12),
                 bg='gray20',
                 fg='white').grid(row=1, column=0, sticky=tk.W, pady=5)

        self.start_date_var = tk.StringVar()
        ttk.Entry(frame,
                  textvariable=self.start_date_var,
                  font=("arial", 12),
                  width=25).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        tk.Label(frame,
                 text="End Date (YYYY-MM-DD):",
                 font=("arial", 12),
                 bg='gray20',
                 fg='white').grid(row=2, column=0, sticky=tk.W, pady=5)

        self.end_date_var = tk.StringVar()
        ttk.Entry(frame,
                  textvariable=self.end_date_var,
                  font=("arial", 12),
                  width=25).grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)

        # Budget
        tk.Label(frame,
                 text="Budget (₹):",
                 font=("arial", 12),
                 bg='gray20',
                 fg='white').grid(row=3, column=0, sticky=tk.W, pady=5)

        self.budget_var = tk.StringVar()
        ttk.Entry(frame,
                  textvariable=self.budget_var,
                  font=("arial", 12),
                  width=25).grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)

    def create_right_frame_content(self, frame):
        # Activities section
        tk.Label(frame,
                 text="Add Activities:",
                 font=("arial", 12),
                 bg='gray20',
                 fg='white').grid(row=0, column=0, sticky=tk.W, pady=5)

        self.activity_var = tk.StringVar()
        activity_entry = ttk.Entry(frame,
                                   textvariable=self.activity_var,
                                   font=("arial", 12),
                                   width=30)
        activity_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        add_btn = tk.Button(frame,
                            text="Add Activity",
                            command=self.add_activity,
                            font=("arial", 10, "bold"),
                            bg='#4CAF50',
                            fg='white',
                            bd=5,
                            relief=tk.RAISED)
        add_btn.grid(row=0, column=2, padx=5, pady=5)

        self.activities_text = tk.Text(frame,
                                       height=5,
                                       width=40,
                                       font=("arial", 12),
                                       bg='ivory',
                                       fg='black')
        self.activities_text.grid(row=1, column=0, columnspan=3, pady=10)

        # Generate button
        generate_btn = tk.Button(frame,
                                 text="Generate Trip Plan",
                                 command=self.generate_plan,
                                 font=("arial", 12, "bold"),
                                 bg='#4CAF50',
                                 fg='white',
                                 bd=5,
                                 relief=tk.RAISED,
                                 padx=20)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=10)

        # Results section
        self.results_text = tk.Text(frame,
                                    height=20,
                                    width=60,
                                    font=("arial", 12),
                                    bg='white',
                                    fg='black')
        self.results_text.grid(row=3, column=0, columnspan=3, pady=10)

    def add_activity(self):
        activity = self.activity_var.get().strip()
        if activity:
            self.activities_list.append(activity)
            self.activities_text.delete(1.0, tk.END)
            self.activities_text.insert(tk.END, '\n'.join(self.activities_list))
            self.activity_var.set('')

    def generate_plan(self):
        try:
            if not self.planner.set_destination(self.destination_var.get()):
                messagebox.showerror("Error", "Please select a valid destination")
                return

            if not self.planner.set_dates(self.start_date_var.get(), self.end_date_var.get()):
                messagebox.showerror("Error", "Please enter valid dates")
                return

            try:
                if not self.planner.set_budget(float(self.budget_var.get())):
                    messagebox.showerror("Error", "Please enter a valid budget")
                    return
            except ValueError:
                messagebox.showerror("Error", "Budget must be a number")
                return

            for activity in self.activities_list:
                self.planner.add_activity(activity)

            self.planner.generate_trip_name()
            self.planner.generate_suggestions()

            summary = self.planner.get_trip_summary()
            self.display_summary(summary)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_summary(self, summary):
        self.results_text.delete(1.0, tk.END)

        summary_text = f"""✨ --- Creative Trip Summary --- ✨
🎈 Trip Name: {summary['trip_name']}
🌍 Destination: {summary['destination']}
📅 Start Date: {summary['start_date']}
📅 End Date: {summary['end_date']}
⏱ Trip Duration: {summary['duration']} days
💰 Budget: ₹{summary['budget']:.2f}

🎯 Planned Activities:
"""

        for i, activity in enumerate(summary['activities'], 1):
            summary_text += f"  {i}. {activity}\n"

        summary_text += "\n💡 --- Suggestions Based on Budget ---\n"
        for key, value in summary['suggestions'].items():
            summary_text += f"  {key}: {value}\n"

        summary_text += "\n🗺 --- Places to Visit --- \n"
        for i, place in enumerate(summary['places'], 1):
            summary_text += f"  {i}. {place}\n"

        summary_text += f"\n✨ Fun Fact: {summary['fact']}\n"
        summary_text += f"💫 Quote: {summary['quote']}\n"

        self.results_text.insert(tk.END, summary_text)


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TRIP PLANNER")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Add heading frame
        heading_label = tk.Label(root,
                                 text='✈ TRIP PLANNER ✈',
                                 font=("times new roman", 30, "bold"),
                      bd=14,
                                 relief=tk.GROOVE)
        heading_label.pack(fill=tk.X)

        try:
            image_path = r"C:\Users\Rishindra\OneDrive\Pictures\133859749865613045.jpg"
            image = Image.open(image_path)
            image = image.resize((1200, 700))
            self.photo = ImageTk.PhotoImage(image)
            bg_label = tk.Label(root, image=self.photo)
        except Exception as e:
            print(f"Error loading background: {e}")
            bg_label = tk.Label(root, bg='lightblue')

        bg_label.pack(fill=tk.BOTH, expand=True)

        text_label = tk.Label(bg_label,
                              text="Plan Your Dream Vacation",
                              font=('arial', 24, 'bold'),
                              bg='light green',
                              relief=tk.RAISED,
                              bd=5)
        text_label.pack(pady=20)

        self.next_button = tk.Button(
            bg_label,
            text="Start Planning",
            command=self.open_planner,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            relief=tk.RAISED,
            bd=5,
            padx=20,
            pady=10
        )
        self.next_button.pack(pady=10)

    def open_planner(self):
        planner_window = tk.Toplevel(self.root)
        TripPlannerGUI(planner_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()