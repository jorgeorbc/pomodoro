import threading
import notify2
import time
import sys
import select

class Pomodoro:
    def __init__(self, duration=25):
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
                "Pomodoro terminado",
                f"Has completado {self.duration_minutes} minutos de trabajo."
            )
            n.show()
            print("\n🎉 ¡Felicidades, has terminado tu Pomodoro!")

    def toggle_pause(self):
        self.pause = not self.pause
        print("\n[Pausa activada]" if self.pause else "\n[Reanudado]")

    def set_quit(self):
        self.quit = True
        print("\n[Saliendo del Pomodoro...]")

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
            "Ingresa el tiempo en minutos "
            "(por defecto 25): "
        )
        t = int(input(prompt) or "25")
        return t if t > 0 else 25
    except ValueError:
        print("Tiempo inválido. Usando 25 minutos por defecto.")
        return 25

if __name__ == "__main__":
    duration = enter_time()
    pomo = Pomodoro(duration)
    input_thread = threading.Thread(target=user_input_loop,
                                    args=(pomo,),
                                    daemon=True)
    input_thread.start()
    pomo.start()
