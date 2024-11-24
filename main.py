# Example file showing a basic pygame "game loop" with bouncing text
import pygame
from datetime import datetime
import pytz
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
from datetime import datetime
import pytz
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Globals
message = ""
text = ""
textmode = False
print("Loading timezone...")

# Load timezone
timezonetext = open('timezone.txt', 'rt').read().strip()
timezone = pytz.timezone(timezonetext)

# Update time globally
timenow = datetime.now(timezone).strftime("%m/%d/%Y, %I:%M:%S %p")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global message
        global text
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html_content = """
            <!DOCTYPE html>
            <html>
            <center>
            <h1>Tailsscreen Controller</h1>
            <form action='/post'>
                <input type='textbox' placeholder='Text to add' name='data'>
                <input type='submit' value='Add screensaver text'>
            </form>
            <form action='/clear'>
                <input type='submit' value='Clear screensaver text'>
            </form>
            </center>
            </html>
            """
            self.wfile.write(html_content.encode())
        elif self.path == "/clear":
            message = ""
            self.send_response(200)
            self.send_header("Content-Type", "applicatioyes oin/json")
            self.end_headers()
            response = "Cleared message".encode()
            self.wfile.write(response)
        elif self.path.startswith("/post"):
            # Parse URL parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)

            # Extract the 'data' parameter
            data = query_params.get("data", [None])[0]
            if data:
                message = data
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write("Done!".encode())
            else:
                # Missing 'data' parameter
                self.send_error(400, "Missing 'data' parameter")
        elif self.path.startswith("/clear"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            message = ""
            self.wfile.write("Done!".encode())
        else:
            # Handle unknown endpoints
            self.send_error(404, "Endpoint not found")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    """Run the server."""
    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


def update_time():
    """Continuously update the current time."""
    global timenow
    while True:
        timenow = datetime.now(timezone).strftime("%m/%d/%Y, %I:%M:%S %p")
        time.sleep(1)


def update_text():
    """Update the displayed text."""
    global text
    while True:
        if textmode and message:
            text = message
        else:
            text = timenow
        time.sleep(1)


def toggle_text_mode():
    """Toggle between text modes."""
    global textmode
    while True:
        textmode = not textmode
        time.sleep(5)


# Start threads
server_thread = threading.Thread(target=run, args=(HTTPServer, SimpleHTTPRequestHandler), daemon=True)
server_thread.start()

time_thread = threading.Thread(target=update_time, daemon=True)
time_thread.start()

text_thread = threading.Thread(target=update_text, daemon=True)
text_thread.start()

toggle_thread = threading.Thread(target=toggle_text_mode, daemon=True)
toggle_thread.start()


# pygame setup
pygame.init()
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((800, 600), flags)
clock = pygame.time.Clock()
pygame.display.set_allow_screensaver(False)
running = True

# Text position and velocity
x, y = 400, 300
x_vel, y_vel = 4, 3

# Define font and size
font = pygame.font.Font(None, 100)  # None uses the default system font

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the screen with a color to wipe away anything from the last frame
    screen.fill("black")

    # Update the current date and time
    current_datetime = datetime.now()

    # Create the text surface
    text_surface = font.render(text, True, (255, 255, 255))  # white text
    text_rect = text_surface.get_rect(center=(x, y))

    # Update the text's position
    x += x_vel
    y += y_vel

    # Recalculate the text rectangle for the updated position
    text_rect = text_surface.get_rect(center=(x, y))

    # Bounce the text off the edges
    if text_rect.left <= 0 or text_rect.right >= screen.get_width():
        x_vel = -x_vel
        # Ensure the position is within bounds after bouncing
        x = max(text_rect.width // 2, min(screen.get_width() - text_rect.width // 2, x))

    if text_rect.top <= 0 or text_rect.bottom >= screen.get_height():
        y_vel = -y_vel
        # Ensure the position is within bounds after bouncing
        y = max(text_rect.height // 2, min(screen.get_height() - text_rect.height // 2, y))

    # Draw the updated text
    screen.blit(text_surface, text_rect)


    # Draw the text
    screen.blit(text_surface, text_rect)

    # Flip the display to update the screen
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()
