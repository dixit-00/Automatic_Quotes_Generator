from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "9F8iRH7ZI9nsT+hXXuwfLA==r8a3LWJeTq4OydZB"  # Replace with your actual API key

def get_quote():
    """Fetches a new Kanye quote and updates the UI."""
    response = requests.get("https://api.kanye.rest")
    response.raise_for_status()
    data = response.json()
    quote = data["quote"]
    canvas.itemconfig(quote_text, text=quote)

    # Fetch and update the Kanye button image dynamically
    get_kanye_image()

def get_kanye_image():
    """Fetches a random profile image and updates the Kanye button."""
    url = "https://avatar.iran.liara.run/public"  # Random avatar image API
    response = requests.get(url)

    if response.status_code == 200:
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        
        # ✅ Resize fetched image to match button (50x100 pixels)
        img = img.resize((50, 100), Image.LANCZOS)
        
        new_kanye_img = ImageTk.PhotoImage(img)

        # ✅ Update button image
        kanye_button.config(image=new_kanye_img)
        kanye_button.image = new_kanye_img  # Prevent garbage collection
    else:
        print("Error fetching image:", response.status_code)

# Create window
window = Tk()
window.title("Kanye Says...")
window.geometry("400x500")
window.config(padx=50, pady=50)

# Canvas for background
canvas = Canvas(window, width=300, height=414)
canvas.grid(row=0, column=0)

# Load default background image
initial_img = Image.open("background.png")
initial_img = initial_img.resize((300, 414), Image.LANCZOS)
background_img = ImageTk.PhotoImage(initial_img)
bg_image = canvas.create_image(150, 207, image=background_img)

# Add quote text to canvas
quote_text = canvas.create_text(150, 207, text="Kanye Quote Goes HERE", width=250, font=("Arial", 20, "bold"), fill="white")

# Like Button
like_button = Button(window, text="❤️ Like Quote", font=("Arial", 14, "bold"))
like_button.grid(row=1, column=0, pady=10)

# Exit Button
exit_button = Button(window, text="Exit", font=("Arial", 14, "bold"), command=window.destroy)
exit_button.grid(row=2, column=0, pady=10)

# Default placeholder image for Kanye button
default_kanye_img = Image.open("kanye.png")  # Local fallback
default_kanye_img = default_kanye_img.resize((50, 100), Image.LANCZOS)
kanye_img = ImageTk.PhotoImage(default_kanye_img)

# Kanye Button (Updates Quote and Kanye Image)
kanye_button = Button(window, image=kanye_img, highlightthickness=0, command=get_quote)
kanye_button.grid(row=3, column=0, pady=10)

# Fetch initial Kanye image
get_kanye_image()

# Run the application
window.mainloop()
