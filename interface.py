from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.app import App
from pilha import Pilha
from jogo import *
from icones import IconButton

# Classe para definir o frasco
class Frasco(Widget):
    def __init__(self, pilha: Pilha, index: int, **kwargs):
        super().__init__(**kwargs)
        self.pilha = pilha
        self.index = index
        self.selected = False
        self.cores = {
            1: (1, 0, 0, 1),    # Vermelho
            2: (0, 1, 0, 1),    # Verde
            3: (0, 0, 1, 1),    # Azul
            4: (1, 1, 0, 1),    # Amarelo
            5: (1, 0, 1, 1),    # Magenta
            6: (0, 1, 1, 1),    # Ciano
            7: (0.5, 0.5, 0.5, 1)  # Cinza
        }

    def on_size(self, *args):
        self.draw()

    def on_pos(self, *args):
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Desenha o frasco
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            if self.selected:
                Color(1, 1, 1, 1)
                linha = 2
                Rectangle(pos=(self.pos[0]-linha, self.pos[1]-linha), 
                         size=(self.size[0]+2*linha, self.size[1]+2*linha))

            # Desenha as bolas
            elementos = self.pilha.get_elementos()
            altura_bola = self.height / 4
            for i, elem in enumerate(elementos):
                if elem != -1:
                    Color(*self.cores.get(elem, (0, 0, 0, 1)))
                    Ellipse(pos=(self.pos[0], self.pos[1] + i * altura_bola),
                           size=(self.width, altura_bola))

# Classe para definir a caixa de mensagem
class MessageBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = dp(10)
        
        with self.canvas.before:
            Color(0.2, 0.3, 0.4, 0.95)  # Cor mais clara e mais opaca
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.message = Label(
            text='',
            font_size=dp(20),  # Fonte maior
            color=(1, 1, 1, 1),
            bold=True,  # Texto em negrito
            padding=(dp(10), dp(10))  # Padding interno do texto
        )
        self.add_widget(self.message)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def set_message(self, text):
        self.message.text = text

# Classe para definir a janela de vitória
class VictoryPopup(Popup):
    def __init__(self, game_instance, **kwargs):
        super().__init__(**kwargs)
        self.game = game_instance
        self.title = 'PARABÉNS!'
        self.size_hint = (0.8, 0.6)
        self.auto_dismiss = False
        
        # Layout principal
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20)
        )
        
        # Label de vitória
        victory_label = Label(
            text='Você Venceu!',
            font_size=dp(32),
            color=(1, 0.8, 0, 1),
            size_hint_y=None,
            height=dp(50)
        )
        content.add_widget(victory_label)
        
        # Container centralizado para o troféu
        trophy_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
        )
        
        # BoxLayout horizontal para centralização
        center_layout = BoxLayout(
            orientation='horizontal',
            size_hint_x=1
        )
        
        # Espaçador esquerdo
        center_layout.add_widget(Widget())
        
        # Troféu
        trophy_icon = IconButton(
            icon_type='trophy',
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            background_normal='',
            background_color=(0, 0, 0, 0),
            pos_hint={'center_y': 0.5}
        )
        center_layout.add_widget(trophy_icon)
        
        # Espaçador direito
        center_layout.add_widget(Widget())
        
        trophy_container.add_widget(center_layout)
        content.add_widget(trophy_container)
        
        # Container dos botões
        buttons = BoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(50),
            padding=(dp(10), 0)
        )
        
        # Botões
        button_style = {
            'background_color': (0.2, 0.6, 1, 1),
            'color': (1, 1, 1, 1),
            'bold': True,
            'font_size': dp(18)
        }
        
        new_game_btn = Button(
            text='Novo Jogo',
            on_press=self.new_game,
            **button_style
        )
        
        menu_btn = Button(
            text='Menu Principal',
            on_press=self.back_to_menu,
            **button_style
        )
        
        buttons.add_widget(new_game_btn)
        buttons.add_widget(menu_btn)
        content.add_widget(buttons)
        
        self.content = content
    
    def new_game(self, instance):
        self.dismiss()
        self.game.novo_jogo(None)
    
    def back_to_menu(self, instance):
        self.dismiss()
        self.game.voltar_menu(None)

# Classe para definir o menu inicial
class MenuInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Estilo do título
        titulo = Label(
            text='Ball Sort Puzzle',
            font_size=dp(32),  # Fonte maior
            size_hint_y=0.2,
            bold=True,  # Texto em negrito
            color=(1, 1, 1, 1)  # Cor consistente com o resto do jogo
        )
        layout.add_widget(titulo)
        
        # Layout do slider
        self.slider_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=10)
        
        # Label do slider com estilo melhorado
        self.slider_label = Label(
            text=f'Número de Cores: {int(4)}',  # Valor inicial
            font_size=dp(20),
            bold=True,
            color=(1, 1, 1, 1)
        )
        
        # Slider com cores personalizadas
        self.slider = Slider(
            min=2,
            max=7,
            value=4,
            step=1,
            cursor_size=(dp(30), dp(30)),  # Cursor maior
            background_width=dp(8)  # Barra mais grossa
        )
        self.slider.bind(value=self.on_slider_change)
        
        self.slider_layout.add_widget(self.slider_label)
        self.slider_layout.add_widget(self.slider)
        layout.add_widget(self.slider_layout)
        
        # Layout dos botões
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),  # Espaçamento aumentado
            size_hint_y=0.3,
            padding=dp(20)  # Padding adicional
        )
        
        # Estilo comum para os botões
        button_style = {
            'background_color': (0.2, 0.6, 1, 1),
            'color': (1, 1, 1, 1),
            'bold': True,
            'font_size': dp(24),  # Fonte maior
            'size_hint_y': None,
            'height': dp(60),  # Altura maior
            'padding': (dp(20), dp(10))  # Padding interno
        }
        
        # Botão Iniciar
        btn_iniciar = Button(
            text='Iniciar Jogo',
            on_press=self.iniciar_jogo,
            **button_style
        )
        
        # Botão Sair
        btn_sair = Button(
            text='Sair do Jogo',
            on_press=self.sair_jogo,
            **button_style
        )
        
        buttons_layout.add_widget(btn_iniciar)
        buttons_layout.add_widget(btn_sair)
        layout.add_widget(buttons_layout)
        
        self.add_widget(layout)

    # Método para atualizar o slider
    def on_slider_change(self, instance, value):
        self.slider_label.text = f'Número de Cores: {int(value)}'

    # Método para iniciar o jogo
    def iniciar_jogo(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.start_game(int(self.slider.value))
        self.manager.current = 'game'
    
    # Método para sair do jogo
    def sair_jogo(self, instance):
        App.get_running_app().stop()

# Classe para definir a tela do jogo
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = None
    
    # Método para iniciar o jogo
    def start_game(self, n_cores):
        if self.game_widget:
            self.remove_widget(self.game_widget)
        self.game_widget = BallSortGame(n_cores)
        self.add_widget(self.game_widget)

# Classe para definir o jogo Ball Sort
class BallSortGame(BoxLayout):
    def __init__(self, n_cores: int, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.n_cores = n_cores
        self.selected_frasco = None
        self.init_game()
        self.create_interface()

    # Método para iniciar o jogo
    def init_game(self):
        self.list_pilhas = lista_de_pilhas(self.n_cores)
        list_numeros = lista_de_inteiros(self.n_cores)
        self.list_pilhas = enche_lista_de_pilhas(list_numeros, self.list_pilhas)

    # Método para criar a interface
    def create_interface(self):
        # Header com título e menu
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        
        # Dropdown menu melhorado
        self.dropdown = DropDown(
            auto_width=False,
            width=dp(200)  # Largura fixa maior
        )
        
        # Estilo comum para botões do menu
        menu_button_style = {
            'size_hint_y': None,
            'height': dp(50),
            'background_color': (0.8, 0.8, 0.8, 1),
            'color': (1, 1, 1, 1),
            'font_size': dp(18)
        }
        
        # Usando o novo IconButton para o menu
        menu_button = IconButton(
            icon_type='menu',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            background_normal='',  # Remove o background padrão
            background_color=(0.2, 0.2, 0.2, 1)  # Cor de fundo escura para contraste
        )
        
        menu_button.bind(on_release=self.dropdown.open)
        
        novo_jogo_btn = Button(
            text='Novo Jogo',
            **menu_button_style
        )
        novo_jogo_btn.bind(on_release=lambda btn: self.menu_action('novo_jogo'))
        
        menu_principal_btn = Button(
            text='Menu Principal',
            **menu_button_style
        )
        menu_principal_btn.bind(on_release=lambda btn: self.menu_action('menu'))
        
        # Adiciona padding entre os botões do dropdown
        for btn in [novo_jogo_btn, menu_principal_btn]:
            container = BoxLayout(size_hint_y=None, height=dp(60), padding=(dp(5), dp(5)))
            container.add_widget(btn)
            self.dropdown.add_widget(container)
        
        header.add_widget(menu_button)

        title_label = Label(
            text='Ball Sort Puzzle',
            font_size=dp(24),
            bold=True,
            color=(1, 1, 1, 1)
        )
        header.add_widget(title_label)
        self.add_widget(header)
        
        # Container para os frascos
        self.frascos_container = GridLayout(
            cols=4 if self.n_cores <= 5 else 5,
            spacing=10,
            padding=10
        )
        self.frascos = []
        
        # Cria os frascos
        for i, pilha in enumerate(self.list_pilhas):
            frasco = Frasco(pilha, i, size_hint=(1, 1))
            self.frascos.append(frasco)
            self.frascos_container.add_widget(frasco)
            
        self.add_widget(self.frascos_container)
        
        # Caixa de mensagem
        self.message_box = MessageBox()
        self.message_box.set_message('Selecione um frasco')
        self.add_widget(self.message_box)

    # Método para ação do menu
    def menu_action(self, action):
        self.dropdown.dismiss()
        if action == 'novo_jogo':
            self.novo_jogo(None)
        elif action == 'menu':
            self.voltar_menu(None)

    # Método para novo jogo no menu
    def novo_jogo(self, instance):
        self.init_game()
        for frasco in self.frascos:
            frasco.pilha = self.list_pilhas[frasco.index]
            frasco.selected = False
            frasco.draw()
        self.message_box.set_message('Novo jogo iniciado')
        self.selected_frasco = None

    # Método para voltar ao menu principal
    def voltar_menu(self, instance):
        self.parent.manager.current = 'menu'

    # Método para toque na tela
    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        
        for frasco in self.frascos:
            if frasco.collide_point(*touch.pos):
                self.handle_frasco_touch(frasco)
                return True

    # Método para toque no frasco
    def handle_frasco_touch(self, frasco):
        if self.selected_frasco is None:
            if not frasco.pilha.pilha_vazia():
                self.selected_frasco = frasco
                frasco.selected = True
                frasco.draw()
                self.message_box.set_message('Selecione o destino')
        else:
            if self.selected_frasco != frasco:
                sucesso, mensagem = jogada(self.list_pilhas, 
                                         self.selected_frasco.index,
                                         frasco.index)
                
                self.message_box.set_message(mensagem)
                self.selected_frasco.selected = False
                self.selected_frasco.draw()
                frasco.draw()
                
                if vencedor(self.list_pilhas):
                    victory_popup = VictoryPopup(self)
                    victory_popup.open()
            
            self.selected_frasco = None