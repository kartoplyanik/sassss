import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock

simvoli = ['910', '500', '20', '21', '34', '2100', '42005', 'dsa']  # 8 унікальних

class MemoryCard(Button):
    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)
        self.symbol = symbol
        self.is_matched = False
        self.text = ''
        self.font_size = 32

    def reveal(self):
        if not self.is_matched:
            self.text = self.symbol

    def hide(self):
        if not self.is_matched:
            self.text = ''

    def mark_matched(self):
        self.is_matched = True

class MemoryGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.cards = []
        self.selected_cards = []

        card_symbols = simvoli * 2  # 16 карт
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

class MemoryApp(App):
    def build(self):
        return MemoryGame()

if __name__ == '__main__':
    MemoryApp().run()