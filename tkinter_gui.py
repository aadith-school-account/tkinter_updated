import tkinter as tk
import ttkbootstrap as tb
import requests
import threading, time, random, randfacts
from ttkbootstrap.widgets import DateEntry
from datetime import datetime
from tkinter import messagebox
from database import setup_db, update_score, get_scores, clear_scores  # Corrected function names
import pygame, os
from PIL import Image, ImageTk

##########-MUSIC-###########
#https://www.youtube.com/watch?v=CQeezCdF4mk 
#https://www.youtube.com/watch?v=aAkMkVFwAoo - ALL I WANT FOR CHRISTMAS IS YOU

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def play_music_elevator():
    pygame.mixer.init()
    try:
        music_path = os.path.join(BASE_DIR, "elevator_music.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Could not play music file. Make sure elevator_music.mp3 exists in the project directory.")

def play_music_christmas():
    pygame.mixer.init()
    try:
        music_path = os.path.join(BASE_DIR, "all_i_want_for_christmas_is_you.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Could not play music file. Make sure all_i_want_for_christmas_is_you.mp3 exists in the project directory.")

def sad_trombone():
    pygame.mixer.init()
    sound_path = os.path.join(BASE_DIR, 'trombone_sad.mp3')
    skibidi_sound = pygame.mixer.Sound(sound_path)
    skibidi_sound.play()

def play_jumpscare():
    def run_jumpscare():
        # Create popup window (NOT fullscreen, just nearly fullscreen so we can shake it)
        jumpscare_window = tk.Toplevel()
        jumpscare_window.configure(bg="black")

        screen_width = jumpscare_window.winfo_screenwidth()
        screen_height = jumpscare_window.winfo_screenheight()

        # Size the window just a bit smaller than the screen so it can shake
        win_width = screen_width - 100
        win_height = screen_height - 100
        x = 50
        y = 50
        jumpscare_window.geometry(f"{win_width}x{win_height}+{x}+{y}")
        jumpscare_window.overrideredirect(True)  # Hide title bar

        # Load and show scary image
        image_path = os.path.join(BASE_DIR, "scary.png")
        image = Image.open(image_path)
        image = image.resize((win_width, win_height))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(jumpscare_window, image=photo)
        label.image = photo
        label.pack()

        # Play scream sound
        pygame.mixer.init()
        sound_path = os.path.join(BASE_DIR, "jumpscare.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

        # Give window time to show up
        jumpscare_window.update()
        time.sleep(0.2)

        # SHAKING EFFECT!
        def shake():
            for _ in range(30):
                dx = random.randint(-30, 30)
                dy = random.randint(-30, 30)
                jumpscare_window.geometry(f"{win_width}x{win_height}+{x+dx}+{y+dy}")
                jumpscare_window.update()
                time.sleep(0.03)
            # Reset to original position
            jumpscare_window.geometry(f"{win_width}x{win_height}+{x}+{y}")

        shake()

        # Hold for dramatic effect
        time.sleep(1)
        jumpscare_window.destroy()

    threading.Thread(target=run_jumpscare).start()



def choose_music():
    def play_choice():
        choice = var.get()
        if choice == "elevator":
            music_thread = threading.Thread(target=play_music_elevator, daemon=True)
            music_thread.start()
        elif choice == "christmas":
            music_thread = threading.Thread(target=play_music_christmas, daemon=True)
            music_thread.start()
        music_win.destroy()

    music_win = tb.Toplevel()
    music_win.title("🎵 Choose Music")
    music_win.geometry("300x180")
    music_win.resizable(False, False)
    music_win.grab_set()
    music_win.attributes("-topmost", True)

    tk.Label(music_win, text="Do you want to listen to music?", font=("Segoe UI", 12)).pack(pady=10)
    var = tk.StringVar(value="elevator")

    tb.Radiobutton(music_win, text="🎄 Christmas Music", variable=var, value="christmas", bootstyle="info").pack()
    tb.Radiobutton(music_win, text="🛗 Elevator Music", variable=var, value="elevator", bootstyle="secondary").pack()

    tb.Button(music_win, text="Play", bootstyle="success", command=play_choice).pack(pady=10)
    tb.Button(music_win, text="No Thanks", bootstyle="danger-outline", command=lambda: [sad_trombone(), music_win.destroy()]).pack()


##########=SETUP FUNCTIONS-##########
setup_db()
# Modify `highlight_winner()` to save scores
def highlight_winner(cells):
    global current_player
    for row, col in cells:
        board[row][col].config(bootstyle="success")

    # Save score in database
    print(f"DEBUG: Calling update_score() for {current_player}")
    update_score(current_player)
    
    messagebox.showinfo("Tic Tac Toe", f"{current_player} wins!")


def clear_leaderboard(window):
    if messagebox.askyesno("Confirm", "Are you sure you want to clear the leaderboard?"):
        clear_scores()
        messagebox.showinfo("Leaderboard", "Leaderboard cleared.")
        window.destroy()



def show_scores():
    scores = get_scores()

    if not scores:
        messagebox.showinfo("Leaderboard", "No games played yet.")
        return

    leaderboard_window = tb.Toplevel()
    leaderboard_window.title("🏆 Leaderboard")
    leaderboard_window.geometry("300x300")
    leaderboard_window.resizable(False, False)
    leaderboard_window.attributes("-topmost", True)

    title = tb.Label(leaderboard_window, text="Tic Tac Toe Leaderboard", font=("Segoe UI", 16, "bold"), bootstyle="info")
    title.pack(pady=10)

    list_frame = tb.Frame(leaderboard_window)
    list_frame.pack(fill="both", expand=True, padx=20)

    for i, (player, wins) in enumerate(scores, start=1):
        row = f"{i}. {player}: {wins} win{'s' if wins != 1 else ''}"
        label = tb.Label(list_frame, text=row, font=("Segoe UI", 12), anchor="w")
        label.pack(fill="x", pady=2)

    # Buttons Frame
    button_frame = tb.Frame(leaderboard_window)
    button_frame.pack(pady=10)

    close_btn = tb.Button(button_frame, text="Close", bootstyle="secondary", command=leaderboard_window.destroy)
    close_btn.grid(row=0, column=0, padx=5)

    clear_btn = tb.Button(
        button_frame,
        text="Clear Leaderboard",
        bootstyle="danger-outline",
        command=lambda: clear_leaderboard(leaderboard_window)
    )
    clear_btn.grid(row=0, column=1, padx=5)


# Function to fetch real-time weather data
def get_weather():
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = "83fe2b6ef09b46208ef122932250205"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            messagebox.showerror("Error", data["error"]["message"])
        else:
            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            
            weather_output.set(f"🌎 {location}\n⛅ {condition}")
            temp_output.set(f"{temp_c}°C")

    except Exception as e:
        messagebox.showerror("Error", "Could not fetch weather data. Check your internet connection.")

# Function to calculate age
def calculate_age():
    try:
        date_of_birth = date_entry.entry.get().strip()

        if not date_of_birth:
            raise ValueError("Date of birth cannot be empty.")

        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if birth_date > datetime.today():
            raise ValueError("Date of birth cannot be in the future.")

        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
        age_in_days = (today - birth_date).days
        output_text.set(f"✨ You are {age} years, {age_in_months} months\nOr {age_in_days} days old!")

    except ValueError as ve:
        messagebox.showerror("Invalid date", str(ve))
    except Exception:
        messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")


##########-TIC TAC TOE-##########

def reset_game():
    global board, current_player
    current_player = "X"
    for row in range(3):
        for col in range(3):
            board[row][col].config(text="", bootstyle="secondary-outline", state="normal")

def check_winner():
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] and board[row][0]["text"] != "":
            highlight_winner([(row, 0), (row, 1), (row, 2)])
            return True

    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] and board[0][col]["text"] != "":
            highlight_winner([(0, col), (1, col), (2, col)])
            return True

    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] and board[0][0]["text"] != "":
        highlight_winner([(0, 0), (1, 1), (2, 2)])
        return True

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] and board[0][2]["text"] != "":
        highlight_winner([(0, 2), (1, 1), (2, 0)])
        return True

    if all(board[row][col]["text"] != "" for row in range(3) for col in range(3)):
        messagebox.showinfo("Tic Tac Toe", "It's a Tie!")
        return True

    return False

def highlight_winner(cells):
    for row, col in cells:
        board[row][col].config(bg="lightgreen")
    messagebox.showinfo("Tic Tac Toe", f"{current_player} wins!")

def on_click(row, col):
    global current_player
    if board[row][col]["text"] == "":
        board[row][col].config(text=current_player)
        if check_winner():
            for r in range(3):
                for c in range(3):
                    board[r][c].config(state="disabled")
        else:
            current_player = "O" if current_player == "X" else "X"


##########-INIT WINDOWS-##########
style = tb.Style(theme="minty")
root = style.master
root.title("Utility App")
root.geometry("450x400")
root.configure(highlightbackground="black", highlightthickness=2)


# Create notebook for tabs
notebook = tb.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Age Calculator Tab
age_frame = tb.Frame(notebook)
notebook.add(age_frame, text="📅 Age Calculator")

title_label = tk.Label(age_frame, text="Age Calculator", font=("Pristina", 30, "bold"))
title_label.pack(pady=10)

date_entry = DateEntry(age_frame, bootstyle="info", dateformat="%Y-%m-%d", width=22)
date_entry.pack(pady=10)

calc_button = tb.Button(age_frame, text="Calculate Age", bootstyle="primary-outline", command=calculate_age)
calc_button.pack(pady=10)

output_text = tk.StringVar()
output_label = tk.Label(age_frame, textvariable=output_text, font=("Comic Sans MS", 12, "bold"))
output_label.pack(fill="both", expand=True, pady=10)

# Weather App Tab
# Weather App Tab
weather_frame = tb.Frame(notebook)
notebook.add(weather_frame, text="☀️ Weather App")

weather_label = tk.Label(weather_frame, text="Weather App", font=("Pristina", 30, "bold"))
weather_label.pack(pady=10)

# 🆕 New Label for clarity
city_prompt = tk.Label(weather_frame, text="Enter your city:", font=("Segoe UI", 12))
city_prompt.pack()

city_entry = tk.Entry(weather_frame, width=30, font=("Helvetica", 12))
city_entry.pack(pady=5)

weather_button = tb.Button(weather_frame, text="Get Weather", bootstyle="success-outline", command=get_weather)
weather_button.pack(pady=10)


weather_output = tk.StringVar()
weather_result_label = tk.Label(weather_frame, textvariable=weather_output, font=("Comic Sans MS", 12, "bold"))
weather_result_label.pack(fill="both", expand=True, pady=5)

temp_output = tk.StringVar()
temp_label = tk.Label(weather_frame, textvariable=temp_output, font=("Elephant", 16, "bold"), fg="red")
temp_label.pack(pady=5)

##########-TIC TAC TOE CONT-###########
tic_tac_toe_frame = tb.Frame(notebook)
notebook.add(tic_tac_toe_frame, text="🎮 Tic Tac Toe")

board = [[None] * 3 for _ in range(3)]
current_player = "X"

# Tic Tac Toe Grid (Using `.grid()` instead of `.pack()`)
for row in range(3):
    for col in range(3):
        board[row][col] = tb.Button(tic_tac_toe_frame, text="", width=6, bootstyle="secondary-outline",
                                    command=lambda r=row, c=col: on_click(r, c))
        board[row][col].grid(row=row, column=col, padx=5, pady=5)  # Places in correct row/column

reset_button = tb.Button(tic_tac_toe_frame, text="Restart Game", bootstyle="danger", command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, pady=10)  # Center reset button below board
# Final winner highlight function — combines correct visuals + DB saving
def highlight_winner(cells):
    global current_player
    for row, col in cells:
        board[row][col].config(bootstyle="success")  # Consistent styling
    update_score(current_player)  # ✅ Save to DB
    messagebox.showinfo("Tic Tac Toe", f"{current_player} wins!")  # ✅ Show winner


leaderboard_button = tb.Button(tic_tac_toe_frame, text="Leaderboard", bootstyle="info-outline", command=show_scores)
leaderboard_button.grid(row=4, column=0, columnspan=3, pady=10)

jumpscare_btn = tk.Button(root, text="Jumpscare!", command=play_jumpscare)
jumpscare_btn.pack(pady=10)


fact_frame = tb.Frame(notebook)
notebook.add(fact_frame, text="🧠 Fun Facts")

fact_label = tk.Label(fact_frame, text="Click the button to get a fun fact!", wraplength=400, justify="center", font=("Comic Sans MS", 12))
fact_label.pack(pady=20)

def generate_fact():
    fact = randfacts.get_fact()
    fact_label.config(text=fact)

fact_button = tb.Button(fact_frame, text="Generate Fact", bootstyle="primary", command=generate_fact)
fact_button.pack(pady=10)

choose_music()


root.mainloop()
