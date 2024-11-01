from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

# Material Design Colors
PRIMARY_COLOR = '#2196F3'  # Blue
SECONDARY_COLOR = '#FFC107'  # Amber
SUCCESS_COLOR = '#4CAF50'  # Green
BACKGROUND_COLOR = '#FAFAFA'  # Light Grey
TEXT_COLOR = '#212121'  # Dark Grey
ACCENT_COLOR = '#FF4081'  # Pink

class StylizedButton(Button):
    def __init__(self, **kwargs):
        super(StylizedButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.font_size = dp(18)
        self.bold = True
        self.padding = [dp(20), dp(20)]

class StylizedInput(TextInput):
    def __init__(self, **kwargs):
        super(StylizedInput, self).__init__(**kwargs)
        self.background_color = get_color_from_hex('#FFFFFF')
        self.foreground_color = get_color_from_hex(TEXT_COLOR)
        self.font_size = dp(16)
        self.padding = [dp(15), dp(10)]
        self.multiline = False
        self.cursor_color = get_color_from_hex(PRIMARY_COLOR)

class MonthlyBudgetScreen(Screen):
    def __init__(self, **kwargs):
        super(MonthlyBudgetScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(*get_color_from_hex(BACKGROUND_COLOR)[:-1], 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        scroll_view = ScrollView()
        self.inner_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.inner_layout.bind(minimum_height=self.inner_layout.setter('height'))

        # Add input fields
        self.inputs = {}
        fields = [
            ('annual_income', 'Annual Income ($)'),
            ('annual_expenses', 'Annual Expenses ($)'),
            ('salary_hike', 'Annual Salary Hike (%)'),
            ('stocks_investment', 'Money in Stocks ($)'),
            ('stocks_return', 'Expected Stocks Return (%)'),
            ('funds_investment', 'Money in Funds ($)'),
            ('funds_return', 'Expected Funds Return (%)'),
            ('savings_amount', 'Savings Account Balance ($)'),
            ('savings_interest', 'Savings Interest Rate (%)'),
            ('other_investment', 'Other Investments ($)'),
            ('other_return', 'Other Investments Return (%)'),
            ('current_networth', 'Current Net Worth ($)'),
            ('prediction_years', 'Years to Predict')
        ]

        for field_id, hint in fields:
            input_field = StylizedInput(
                hint_text=hint,
                size_hint_y=None,
                height=dp(50)
            )
            self.inputs[field_id] = input_field
            self.inner_layout.add_widget(input_field)

        predict_btn = StylizedButton(
            text='Predict Net Worth',
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex(SUCCESS_COLOR)
        )
        predict_btn.bind(on_press=self.calculate_prediction)
        self.inner_layout.add_widget(predict_btn)

        self.result_label = Label(
            text='Prediction Results\n',
            size_hint_y=None,
            height=dp(200),
            color=get_color_from_hex(TEXT_COLOR),
            font_size=dp(16)
        )
        self.inner_layout.add_widget(self.result_label)

        back_btn = StylizedButton(
            text='Back',
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex(PRIMARY_COLOR),
            on_press=self.go_back
        )
        self.inner_layout.add_widget(back_btn)

        scroll_view.add_widget(self.inner_layout)
        main_layout.add_widget(scroll_view)
        self.add_widget(main_layout)

    def calculate_prediction(self, instance):
        try:
            # Get values from inputs
            annual_income = float(self.inputs['annual_income'].text or 0)
            annual_expenses = float(self.inputs['annual_expenses'].text or 0)
            salary_hike = float(self.inputs['salary_hike'].text or 0) / 100
            stocks_investment = float(self.inputs['stocks_investment'].text or 0)
            stocks_return = float(self.inputs['stocks_return'].text or 0) / 100
            funds_investment = float(self.inputs['funds_investment'].text or 0)
            funds_return = float(self.inputs['funds_return'].text or 0) / 100
            savings_amount = float(self.inputs['savings_amount'].text or 0)
            savings_interest = float(self.inputs['savings_interest'].text or 0) / 100
            other_investment = float(self.inputs['other_investment'].text or 0)
            other_return = float(self.inputs['other_return'].text or 0) / 100
            current_networth = float(self.inputs['current_networth'].text or 0)
            years = int(self.inputs['prediction_years'].text or 10)

            result = "Predicted Net Worth:\n\n"
            total_networth = current_networth

            for year in range(1, years + 1):
                # Update values for the year
                annual_expenses *= 1.03  # 3% increase in expenses
                annual_income *= (1 + salary_hike)
                stocks_investment *= (1 + stocks_return)
                funds_investment *= (1 + funds_return)
                savings_amount *= (1 + savings_interest)
                other_investment *= (1 + other_return)

                # Calculate new net worth
                total_networth = (stocks_investment + funds_investment + 
                                savings_amount + other_investment + 
                                (annual_income - annual_expenses))

                result += f"Year {year}: ${total_networth:,.2f}\n"

            self.result_label.text = result

        except ValueError:
            self.result_label.text = "Please enter valid numbers in all fields"

    def go_back(self, instance):
        self.manager.current = 'main'

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(*get_color_from_hex(BACKGROUND_COLOR)[:-1], 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(30))

        title = Label(
            text='Budget Manager',
            font_size=dp(32),
            size_hint_y=None,
            height=dp(60),
            color=get_color_from_hex(TEXT_COLOR),
            bold=True
        )
        layout.add_widget(title)

        button_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None,
            height=dp(400)
        )

        buttons = [
            ('Savings\nCalculator', SUCCESS_COLOR, 'savings'),
            ('Monthly Budget\n& Predictions', PRIMARY_COLOR, 'monthly_budget'),
            ('Debt/Credit\nTracker', SECONDARY_COLOR, 'debt_credit')
        ]

        for text, color, screen in buttons:
            btn = StylizedButton(
                text=text,
                background_color=get_color_from_hex(color),
                size_hint_y=None,
                height=dp(120)
            )
            btn.bind(on_press=lambda x, s=screen: self.switch_screen(s))
            button_layout.add_widget(btn)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class SavingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SavingsScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(*get_color_from_hex(BACKGROUND_COLOR)[:-1], 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))

        header = Label(
            text='Savings Calculator',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(50),
            color=get_color_from_hex(TEXT_COLOR),
            bold=True
        )
        main_layout.add_widget(header)

        self.income_input = StylizedInput(
            hint_text='Monthly Income ($)',
            size_hint_y=None,
            height=dp(50)
        )
        self.income_input.bind(text=self.calculate_savings)
        main_layout.add_widget(self.income_input)

        scroll_view = ScrollView()
        expense_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        expense_layout.bind(minimum_height=expense_layout.setter('height'))

        # Predefined expense categories
        expense_categories = [
            'Rent/Mortgage',
            'Utilities',
            'Groceries',
            'Transportation',
            'Healthcare',
            'Entertainment',
            'Insurance',
            'Phone/Internet',
            'Clothing',
            'Miscellaneous'
        ]

        self.expense_inputs = []
        for category in expense_categories:
            expense_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(50),
                spacing=dp(10)
            )
            
            category_label = Label(
                text=category,
                size_hint_x=0.4,
                color=get_color_from_hex(TEXT_COLOR),
                halign='right'
            )
            
            expense_input = StylizedInput(
                hint_text=f'$ Amount',
                size_hint_x=0.6
            )
            expense_input.bind(text=self.calculate_savings)
            self.expense_inputs.append(expense_input)
            
            expense_box.add_widget(category_label)
            expense_box.add_widget(expense_input)
            expense_layout.add_widget(expense_box)

        scroll_view.add_widget(expense_layout)
        main_layout.add_widget(scroll_view)

        results_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(10)
        )

        self.total_expenses_label = Label(
            text='Total Expenses: $0.00',
            color=get_color_from_hex(SECONDARY_COLOR),
            font_size=dp(18),
            bold=True
        )
        results_layout.add_widget(self.total_expenses_label)

        self.savings_label = Label(
            text='Monthly Savings: $0.00',
            color=get_color_from_hex(SUCCESS_COLOR),
            font_size=dp(20),
            bold=True
        )
        results_layout.add_widget(self.savings_label)

        main_layout.add_widget(results_layout)

        back_btn = StylizedButton(
            text='Back',
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex(PRIMARY_COLOR),
            on_press=self.go_back
        )
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def calculate_savings(self, instance, value):
        try:
            income = float(self.income_input.text or 0)
            total_expenses = sum(float(input.text or 0) for input in self.expense_inputs)
            savings = income - total_expenses
            
            self.total_expenses_label.text = f'Total Expenses: ${total_expenses:.2f}'
            self.savings_label.text = f'Monthly Savings: ${savings:.2f}'
            
            # Change color based on savings amount
            if savings < 0:
                self.savings_label.color = get_color_from_hex('#F44336')  # Red
            else:
                self.savings_label.color = get_color_from_hex(SUCCESS_COLOR)
                
        except ValueError:
            self.total_expenses_label.text = 'Please enter valid numbers'
            self.savings_label.text = 'Please enter valid numbers'

    def go_back(self, instance):
        self.manager.current = 'main'

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
class DebtCreditScreen(Screen):
    def __init__(self, **kwargs):
        super(DebtCreditScreen, self).__init__(**kwargs)
        
        with self.canvas.before:
            Color(*get_color_from_hex(BACKGROUND_COLOR)[:-1], 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))

        header = Label(
            text='Debt/Credit Tracker',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(50),
            color=get_color_from_hex(TEXT_COLOR),
            bold=True
        )
        self.layout.add_widget(header)

        scroll_view = ScrollView()
        self.inner_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        self.inner_layout.bind(minimum_height=self.inner_layout.setter('height'))

        # Add name/description fields for each debt/credit entry
        for i in range(10):
            entry_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(120),
                spacing=dp(5)
            )

            # Add a description field
            description_input = StylizedInput(
                hint_text=f'Description (e.g., "Loan from John" or "Credit Card")',
                size_hint_y=None,
                height=dp(40)
            )
            entry_layout.add_widget(description_input)

            # Add debt/credit amount fields
            amount_layout = BoxLayout(size_hint_y=None, height=dp(50))
            debt_input = StylizedInput(
                hint_text='Debt Amount ($)',
                size_hint_x=0.45
            )
            credit_input = StylizedInput(
                hint_text='Credit Amount ($)',
                size_hint_x=0.45
            )

            debt_input.bind(text=self.update_result)
            credit_input.bind(text=self.update_result)

            amount_layout.add_widget(debt_input)
            amount_layout.add_widget(credit_input)
            entry_layout.add_widget(amount_layout)

            self.inner_layout.add_widget(entry_layout)

        scroll_view.add_widget(self.inner_layout)
        self.layout.add_widget(scroll_view)

        # Results section
        results_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )

        self.total_debt_label = Label(
            text='Total Debt: $0.00',
            color=get_color_from_hex('#F44336'),  # Red
            font_size=dp(18),
            bold=True
        )
        results_layout.add_widget(self.total_debt_label)

        self.total_credit_label = Label(
            text='Total Credit: $0.00',
            color=get_color_from_hex(SUCCESS_COLOR),
            font_size=dp(18),
            bold=True
        )
        results_layout.add_widget(self.total_credit_label)

        self.result_label = Label(
            text='Net Balance: $0.00',
            color=get_color_from_hex(TEXT_COLOR),
            font_size=dp(20),
            bold=True
        )
        results_layout.add_widget(self.result_label)

        self.layout.add_widget(results_layout)

        back_btn = StylizedButton(
            text='Back',
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex(PRIMARY_COLOR),
            on_press=self.go_back
        )
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def update_result(self, instance, value):
        total_debt = 0
        total_credit = 0

        for child in self.inner_layout.children:
            if isinstance(child, BoxLayout):
                amount_layout = child.children[0]  # Get the amount layout
                debt_text = amount_layout.children[1].text  # Debt input
                credit_text = amount_layout.children[0].text  # Credit input

                try:
                    total_debt += float(debt_text or 0)
                except ValueError:
                    pass

                try:
                    total_credit += float(credit_text or 0)
                except ValueError:
                    pass

        balance = total_credit - total_debt
        
        self.total_debt_label.text = f"Total Debt: ${total_debt:.2f}"
        self.total_credit_label.text = f"Total Credit: ${total_credit:.2f}"

        if balance < 0:
            result = f"Net Debt: ${abs(balance):.2f}"
            self.result_label.color = get_color_from_hex('#F44336')  # Red
        elif balance > 0:
            result = f"Net Credit: ${balance:.2f}"
            self.result_label.color = get_color_from_hex(SUCCESS_COLOR)  # Green
        else:
            result = "Balanced: $0.00"
            self.result_label.color = get_color_from_hex(TEXT_COLOR)  # Default color

        self.result_label.text = result

    def go_back(self, instance):
        self.manager.current = 'main'

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MyApp(App):
    def build(self):
        self.title = 'Budget Manager'
        Window.clearcolor = get_color_from_hex(BACKGROUND_COLOR)
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SavingsScreen(name='savings'))
        sm.add_widget(DebtCreditScreen(name='debt_credit'))
        sm.add_widget(MonthlyBudgetScreen(name='monthly_budget'))
        return sm

if __name__ == '__main__':
    MyApp().run()                