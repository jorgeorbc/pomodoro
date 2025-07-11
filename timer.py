from pynput import keyboard
import time
import threading

class Pomodoro:
    def __init__(self, duration):
        self.duration = duration * 60
        self.remaining = duration * 60
        self.pause = False
        self.quit = False
        self.timer = "00:00"

    def start(self):
        while self.remaining > 0:
            if self.quit:
                print("\nStopped early")
                break
            if not self.pause:
                mins, secs = divmod(self.remaining, 60)
                self.timer = '{:02d}:{:02d}'.format(mins, secs)
                print('\r' + self.timer,
                      "(Paused - Press 'p' to resume, 'q' to quit)",
                      end='',
                      flush=True)
                time.sleep(1)
                self.remaining -= 1
            else:
                print(self.timer,
                      "(Paused- Press 'p' to resume, 'q' to quit)",
                      end='\r')
                time.sleep(0.5)
        else:
            print("Congrulations, you finish")

    def set_pause(self):
        self.pause = not self.pause

    def set_quit(self):
        self.quit = not self.quit

def create_on_press(pomodoro):
    def on_press(key):
        try:
            if key.char == 'p':
                pomodoro.set_pause()
                print("\n[Pauser/Resumed]")
            elif key.char == 'q':
                pomodoro.set_quit()
                print("\n[Exiting...]")
                return False
        except AttributeError:
            pass
    return on_press



if __name__ == "__main__":
    pomo = Pomodoro(5)
    on_press = create_on_press(pomo)
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    pomo.start()
    listener.join()

