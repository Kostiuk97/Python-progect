from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.balance = 0

    def add_item(self, product):
        self.items.append(product)

    def calculate_total(self):
        total = sum([item.price for item in self.items])
        return total

    def add_to_balance(self, amount):
        self.balance += amount

    def clear_cart(self):
        self.items = []

class ShoppingCartApp(App):
    def build(self):
        self.products = [
            Product("Laptop", 1000),
            Product("Phone", 500),
            Product("Планшет", 500),
            Product("Годинник", 200),
            Product("Камера", 700),
            Product("Флешка", 20),
            Product("Мишка", 30),
            Product("Клавіатура", 50),
            Product("Монітор", 300),
            Product("Навушники", 40),
            Product("Кабель USB", 10),
            Product("Мишка бездротова", 35),
            Product("Чохол для ноутбука", 25),
            Product("Коврик для миші", 15),
            Product("Екстерній жорсткий диск", 80),
            Product("USB-хаб", 15),
            Product("Електричний чайник", 40),
            Product("Цифровий фотоапарат", 250)
        ]

        self.shopping_cart = ShoppingCart()

        layout = BoxLayout(orientation='vertical')

        self.product_spinner = Spinner(text='Виберіть товар')
        for product in self.products:
            self.product_spinner.values.append(f"{product.name} - ${product.price}")

        add_to_cart_button = Button(text='Додати у кошик')
        add_to_cart_button.bind(on_press=self.add_to_cart)

        self.total_label = Label(text='Загальна вартість: $0')

        self.balance_label = Label(text=f'Баланс: ${self.shopping_cart.balance}')

        self.amount_input = TextInput(hint_text='Сума для поповнення', multiline=False)
        add_balance_button = Button(text='Поповнити баланс')
        add_balance_button.bind(on_press=self.add_balance)

        self.items_bought_label = Label(text='Куплені товари:')

        buy_button = Button(text='Купити', on_press=self.buy)

        layout.add_widget(self.product_spinner)
        layout.add_widget(add_to_cart_button)
        layout.add_widget(self.amount_input)
        layout.add_widget(add_balance_button)
        layout.add_widget(self.total_label)
        layout.add_widget(self.balance_label)
        layout.add_widget(self.items_bought_label)
        layout.add_widget(buy_button)

        return layout

    def add_to_cart(self, instance):
        selected_product = self.product_spinner.text.split(' - ')[0]
        price = int(self.product_spinner.text.split(' - ')[1].strip('$'))

        if self.shopping_cart.balance >= price:
            self.shopping_cart.add_item(Product(selected_product, price))
            total_amount = self.shopping_cart.calculate_total()
            self.total_label.text = f"Загальна вартість: ${total_amount}"
            self.shopping_cart.add_to_balance(-price)
            self.balance_label.text = f'Баланс: ${self.shopping_cart.balance}'

            popup = Popup(title='Повідомлення', content=Label(text=f"{selected_product} додано у кошик."), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Помилка', content=Label(text='Недостатньо коштів на балансі.'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def add_balance(self, instance):
        amount_str = self.amount_input.text
        try:
            amount = float(amount_str)
            self.shopping_cart.add_to_balance(amount)
            self.amount_input.text = ''
            self.balance_label.text = f'Баланс: ${self.shopping_cart.balance}'
            popup = Popup(title='Повідомлення', content=Label(text=f"Баланс поповнено на ${amount}."), size_hint=(None, None), size=(400, 200))
            popup.open()
        except ValueError:
            popup = Popup(title='Помилка', content=Label(text='Введіть коректну суму.'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def buy(self, instance):
        total_amount = self.shopping_cart.calculate_total()
        if total_amount <= self.shopping_cart.balance:
            self.shopping_cart.balance -= total_amount
            items_bought = [item.name for item in self.shopping_cart.items]  # Get names of purchased items
            self.shopping_cart.clear_cart()
            self.total_label.text = "Загальна вартість: $0"
            self.balance_label.text = f'Баланс: ${self.shopping_cart.balance}'
            self.items_bought_label.text = 'Куплені товари:\n' + '\n'.join(items_bought)  # Display purchased items
            popup = Popup(title='Повідомлення', content=Label(text='Покупка здійснена.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Помилка', content=Label(text='Недостатньо коштів на балансі для здійснення покупки.'), size_hint=(None, None), size=(400, 200))
            popup.open()

if __name__ == '__main__':
    ShoppingCartApp().run()
