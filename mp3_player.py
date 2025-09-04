import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pygame
import os

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        pygame.mixer.init()

        self.current_track = ""
        self.paused = False
        self.total_length = 0

        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=('Arial', 10), background="#e0e0e0")
        self.style.configure("Horizontal.TScale", background="#f0f0f0")

        self.label = tk.Label(root, text="No track loaded", bg="#f0f0f0", font=('Arial', 12))
        self.label.pack(pady=10)

        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=5)

        self.load_button = ttk.Button(button_frame, text="Load Track", command=self.load_track)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.play_button = ttk.Button(button_frame, text="Play", command=self.play_track)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(button_frame, text="Pause/Resume", command=self.pause_resume_track)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_track)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Center volume frame
        volume_frame = tk.Frame(root, bg="#f0f0f0")
        volume_frame.pack(pady=5)

        self.volume_label = tk.Label(volume_frame, text="Volume:", bg="#f0f0f0")
        self.volume_label.pack(side=tk.LEFT, padx=5)

        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        self.set_volume(50)

        self.progress_scale = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, state=tk.DISABLED, command=self.set_position)
        self.progress_scale.pack(pady=5, fill=tk.X, padx=10)

        self.time_label = tk.Label(root, text="00:00 / 00:00", bg="#f0f0f0", font=('Arial', 10))
        self.time_label.pack(pady=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)

        self.label.pack(anchor=tk.CENTER)
        button_frame.pack(anchor=tk.CENTER)
        volume_frame.pack(anchor=tk.CENTER)
        self.progress_scale.pack(anchor=tk.CENTER)
        self.time_label.pack(anchor=tk.CENTER)

        self.label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        button_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        volume_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.progress_scale.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.time_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def load_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav;*.ogg")])
        if file_path:
            try:
                self.current_track = file_path
                self.label.config(text=os.path.basename(file_path))
                pygame.mixer.music.load(self.current_track)
                sound = pygame.mixer.Sound(self.current_track)
                self.total_length = sound.get_length()
                self.progress_scale.config(state=tk.NORMAL, to=self.total_length)
                self.progress_scale.set(0)
                self.update_time_label()
            except pygame.error as e:
                messagebox.showerror("Error", f"Could not load file: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def play_track(self):
        if self.current_track:
            try:
                pygame.mixer.music.play()
                self.paused = False
                self.update_progress()
            except pygame.error as e:
                messagebox.showerror("Error", f"Could not play file: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def pause_resume_track(self):
        if self.current_track:
            if pygame.mixer.music.get_busy():
                if self.paused:
                    pygame.mixer.music.unpause()
                    self.paused = False
                    self.update_progress()
                else:
                    pygame.mixer.music.pause()
                    self.paused = True
            elif self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.update_progress()

    def stop_track(self):
        if self.current_track:
            pygame.mixer.music.stop()
            self.paused = False
            self.progress_scale.set(0)
            self.update_time_label()

    def set_volume(self, volume):
        try:
            volume_float = float(volume) / 100.0
            pygame.mixer.music.set_volume(volume_float)
        except ValueError:
            messagebox.showerror("Error", "Invalid volume value")

    def update_progress(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_pos = pygame.mixer.music.get_pos() / 1000
            self.progress_scale.set(current_pos)
            self.update_time_label()
            self.root.after(1000, self.update_progress)

    def set_position(self, position):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(float(position))
            self.update_time_label()

    def update_time_label(self):
        if self.current_track:
            current_pos = pygame.mixer.music.get_pos() / 1000 if pygame.mixer.music.get_busy() else 0
            current_time = self.format_time(current_pos)
            total_time = self.format_time(self.total_length)
            self.time_label.config(text=f"{current_time} / {total_time}")
        else:
            self.time_label.config(text="00:00 / 00:00")

    def format_time(self, seconds):
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()