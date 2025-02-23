from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from interface import *

class BallSortApp(App):
    def build(self):
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        
        # Cria o gerenciador de telas
        sm = ScreenManager()
        
        # Adiciona as telas
        sm.add_widget(MenuInicial(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        
        return sm

if __name__ == '__main__':
    BallSortApp().run()