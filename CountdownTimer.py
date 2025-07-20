# CountdownTimer.py

import time  # Import the time module to add delay

def countdown(start):
    for i in range(start, -1, -1):  # From 'start' to 0 (inclusive), step -1
        print(i)
        time.sleep(1)  # Pause for 1 second

# Example usage
if __name__ == "__main__":
    countdown(10)
    print("🚀 Countdown Complete! Time to Fly High!")
