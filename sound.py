import pygame
import os

class SoundManager:
    def __init__(self, sound_folder='sounds'):
        """
        初始化声音管理器。
        """
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds(sound_folder)

    def load_sounds(self, folder):
        """
        从指定文件夹加载所有声音文件。
        """
        for filename in os.listdir(folder):
            if filename.endswith('.wav'):
                sound_name = os.path.splitext(filename)[0]
                sound_path = os.path.join(folder, filename)
                self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                print(f"Loaded sound: {sound_name}")

    def play(self, sound_name):
        """
        播放指定名称的声音。
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            print(f"Playing sound: {sound_name}")
        else:
            print(f"Sound {sound_name} not found.")

# Example usage
if __name__ == "__main__":
    sound_manager = SoundManager()
    sound_manager.play('game_over')
