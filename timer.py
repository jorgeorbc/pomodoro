import threading
import notify2
import time
import sys
import select
import os

EXE_DIR = os.path.dirname(sys.executable)
FILE_PATH = os.path.join(EXE_DIR, "info.txt")

class Pomodoro:
    def __init__(self, duration=25, category='default'):
        self.category = category
        self.duration_minutes = duration
        self.duration = duration * 60
        self.remaining = duration * 60
        self.pause = False
        self.quit = False
        self.timer = "00:00"

    def start(self):
        while self.remaining > 0:
            if self.quit:
                print("\n[Stopped early]")
                break

            mins, secs = divmod(self.remaining, 60)
            self.timer = f'{mins:02d}:{secs:02d}'
            status = (
                "[Paused] Press 'p' to resume, 'q' to quit "
                if self.pause
                else "[Running] Press 'p' to pause, 'q' to quit "
            )
            print(f'\r{self.timer} {status}', end='', flush=True)

            if not self.pause:
                time.sleep(1)
                self.remaining -= 1
            else:
                time.sleep(0.5)
        else:

            notify2.init('Pomodoro')
            n = notify2.Notification(
                "Pomodoro finished",
                f"You have completed {self.duration_minutes} minutes of work."
            )
            n.show()
            file = open(FILE_PATH, "a")
            file.write(f"{self.category}, {self.duration_minutes}\n")
            file.close
            print("\n🎉 Congratulations, You have finished your Pomodoro!")

    def toggle_pause(self):
        self.pause = not self.pause
        print("\n[Pause activated]" if self.pause else "\n[Resumed]")

    def set_quit(self):
        self.quit = True
        print("\n[Leaving the Pomodoro...]")

def user_input_loop(pomodoro):
    while not pomodoro.quit:
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
            key = sys.stdin.readline().strip().lower()
            if key == 'p':
                pomodoro.toggle_pause()
            elif key == 'q':
                pomodoro.set_quit()
                break

def enter_time():
    try:
        prompt = (
            "Enter time in minutes"
            "(default: 25 minutes): "
        )
        t = int(input(prompt) or "25")
        return t if t > 0 else 25
    except ValueError:
        print("Invalid time. Using 25 minutes (default).")
        return 25

def enter_category():
    try:
        category = input("Enter category (default: 'default'): ")
        return category
    except:
        return "default"

if __name__ == "__main__":
    duration = enter_time()
    category = enter_category()
    pomo = Pomodoro(duration, category)
    input_thread = threading.Thread(target=user_input_loop,
                                    args=(pomo,),
                                    daemon=True)
    input_thread.start()
    pomo.start()
