from playsound import playsound
import time

CLEAR = "\033[2J"
CLEAR_AND_RETURN = "\033[H"

def alarm(seconds):
    time_elapsed = 0
    print(CLEAR)

    while time_elapsed < seconds:
        time.sleep(1)
        time_elapsed += 1

        time_left = seconds - time_elapsed
        minutes_left = time_left // 60
        seconds_left = time_left % 60

        print(f"{CLEAR_AND_RETURN}{minutes_left:02d}:{seconds_left:02d}")

    try:
        playsound("alarm.mp3")
    except Exception as e:
        print(f"Failed to play sound: {e}")

def get_input():
    try:
        minutes = int(input("How many minutes to wait: "))
        seconds = int(input("How many seconds to wait: "))
        return minutes * 60 + seconds
    except ValueError:
        print("Invalid!!! Please Enter an Integer!")
        return 0

if __name__ == "__main__":
    total_seconds = get_input()
    if total_seconds > 0:
        alarm(total_seconds)
