import sys
import os
import signal
import rumps

class TimerBar(rumps.App):
    def __init__(self, remaining, parent_pid=None):
        super().__init__("00:00:00 😴", quit_button=None)
        self.remaining = remaining
        self.parent_pid = parent_pid

        self.menu = [
            rumps.MenuItem("Show Sleep Timer App", callback=self.show_app),
            None,  # Separator line
            rumps.MenuItem("Stop Timer", callback=self.stop_timer)
        ]

        self.timer = rumps.Timer(self.tick, 1)
        self.timer.start()

    def tick(self, sender):
        if self.remaining <= 0:
            rumps.quit_application()
            return
        
        self.title = f"{self.remaining//3600:02d}:{(self.remaining%3600)//60:02d}:{self.remaining%60:02d} 😴"
        self.remaining -= 1

    def show_app(self, sender):
        if self.parent_pid:
            try:
                os.kill(int(self.parent_pid), signal.SIGUSR1)
            except Exception as e:
                print("Error signaling show app:", e)

    def stop_timer(self, sender):
        if self.parent_pid:
            try:
                os.kill(int(self.parent_pid), signal.SIGUSR2)
            except Exception as e:
                print("Error signaling stop timer:", e)
        rumps.quit_application()

if __name__ == '__main__':
    remaining = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
    parent_pid = int(sys.argv[2]) if len(sys.argv) > 2 else None
    app = TimerBar(remaining, parent_pid)
    app.run()
