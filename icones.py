from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.metrics import dp
from kivy.clock import Clock

class IconButton(Button):

    # Classe para criar botões com ícones
    def __init__(self, icon_type, **kwargs):
        super().__init__(**kwargs)
        self.icon_type = icon_type
        Clock.schedule_once(self.delayed_draw)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def delayed_draw(self, dt):
        self.update_canvas()
        
    # Método para atualizar o canvas    
    def update_canvas(self, *args):
        self.canvas.after.clear()  
        with self.canvas.after:
            if self.icon_type == 'menu':
                self.draw_menu_icon()
            elif self.icon_type == 'trophy':
                self.draw_trophy_icon()
    
    # Método para desenhar o ícone do menu
    def draw_menu_icon(self):
        
        line_height = dp(2)
        line_spacing = dp(6)
        total_height = (line_height * 3) + (line_spacing * 2)
        
        # Calculate positions
        start_y = self.center_y + (total_height / 2) - line_height
        line_width = min(self.width * 0.6, dp(24))  # Limit maximum width
        start_x = self.center_x - (line_width / 2)
        
        # Draw three white lines
        Color(1, 1, 1, 1)  # White color
        for i in range(3):
            y = start_y - (i * (line_height + line_spacing))
            Rectangle(pos=(start_x, y), size=(line_width, line_height))
    
    # Método para desenhar o ícone da taça
    def draw_trophy_icon(self):
        padding = dp(8)
        total_width = self.width - 2 * padding
        total_height = self.height - 2 * padding
        
        scale_factor = 2.0 
        base_width = total_width * 0.3 * scale_factor  
        top_width = base_width * 2      
        pedestal_width = base_width * 0.5          
        
        base_height = total_height * 0.1 * scale_factor    
        pedestal_height = total_height * 0.15 * scale_factor
        body_height = total_height * 0.4 * scale_factor     
        top_height = total_height * 0.15 * scale_factor     
        
        center_x = self.center_x
        bottom_y = self.y + padding
        
        Color(1, 0.8, 0, 1)  
        
        # Base retangular
        Rectangle(
            pos=(center_x - base_width/2, bottom_y),
            size=(base_width, base_height)
        )
        
        # Pedestal retangular
        pedestal_y = bottom_y + base_height
        Rectangle(
            pos=(center_x - pedestal_width/2, pedestal_y),
            size=(pedestal_width, pedestal_height)
        )
        
        # Corpo da taça
        top_y = pedestal_y + pedestal_height
        Ellipse(
            pos=(center_x - top_width/2, top_y),
            size=(top_width, top_height / 2),
        )
        
        Rectangle(
            pos=(center_x - top_width/2, top_y + top_height / 4),
            size=(top_width, body_height)
        )
        
        # Alças
        Color(1, 0.6, 0, 1)
        handle_width = dp(3)
        handle_offset = dp(10)
        
        Line(
            ellipse=(center_x - top_width * 0.75, top_y + body_height * 0.4, top_width * 0.7, top_height * 1.2, 200, 340),
            width=handle_width
        )
        
        Line(
            ellipse=(center_x + top_width * 0.15 - handle_offset, top_y + body_height * 0.4, top_width * 0.7, top_height * 1.2, 20, 160),
            width=handle_width
        )
            