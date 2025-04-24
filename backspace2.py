import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label

# 🔠 Список слів — на всі рівні одразу
SYMBOLS = [
    'Кіт', 'Пес', 'Миша', 'Книга', 'Гора', 'Озеро',
    'Кава', 'Чай', 'Дерево', 'Квітка', 'Будинок', 'Авто',
    'Море', 'Риба', 'Сонце', 'Місяць', 'Птах', 'Сніг'
]

class MemoryCard(Button):
    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)
        self.symbol = symbol
        self.is_matched = False
        self.text = ''
        self.font_size = 20

    def reveal(self):
        if not self.is_matched:
            self.text = self.symbol

    def hide(self):
        if not self.is_matched:
            self.text = ''

    def mark_matched(self):
        self.is_matched = True


class MemoryGame(GridLayout):
    def __init__(self, symbols, cols, **kwargs):
        super().__init__(**kwargs)
        self.cols = cols
        self.cards = []
        self.selected_cards = []

        card_symbols = symbols * 2
        random.shuffle(card_symbols)

        for symbol in card_symbols:
            card = MemoryCard(symbol=symbol)
            card.bind(on_press=self.card_pressed)
            self.cards.append(card)
            self.add_widget(card)

    def card_pressed(self, card):
        if card in self.selected_cards or card.is_matched or len(self.selected_cards) == 2:
            return

        card.reveal()
        self.selected_cards.append(card)

        if len(self.selected_cards) == 2:
            Clock.schedule_once(self.check_match, 1)

    def check_match(self, dt):
        card1, card2 = self.selected_cards
        if card1.symbol == card2.symbol:
            card1.mark_matched()
            card2.mark_matched()
        else:
            card1.hide()
            card2.hide()
        self.selected_cards = []


class DifficultyMenu(BoxLayout):
    def __init__(self, start_game_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(text='Оберіть складність:', font_size=24))

        btn_easy = Button(text='Легка (4x4)', size_hint=(1, 0.3))
        btn_easy.bind(on_press=lambda x: start_game_callback('easy'))
        self.add_widget(btn_easy)

        btn_hard = Button(text='Складна (6x6)', size_hint=(1, 0.3))
        btn_hard.bind(on_press=lambda x: start_game_callback('hard'))
        self.add_widget(btn_hard)


class MemoryApp(App):
    def build(self):
        self.root_layout = BoxLayout()
        self.show_difficulty_menu()
        return self.root_layout

    def show_difficulty_menu(self):
        self.root_layout.clear_widgets()
        menu = DifficultyMenu(self.start_game)
        self.root_layout.add_widget(menu)

    def start_game(self, difficulty):
        self.root_layout.clear_widgets()
        if difficulty == 'easy':
            symbols = SYMBOLS[:8]
            game = MemoryGame(symbols=symbols, cols=4)
        else:
            symbols = SYMBOLS[:18]
            game = MemoryGame(symbols=symbols, cols=6)
        self.root_layout.add_widget(game)


if __name__ == '__main__':
    MemoryApp().run()