
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import matplotlib.pyplot as plt
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
import sqlite3
import datetime
from kivy.uix.gridlayout import GridLayout
#from kivy import platform

from kivy.utils import platform
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
#if platform=='android':
    #from android.permissions import Permission,request_permissions
    #request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])

Expense=0
MonthlyBudget=0

class BudgetApp(App):
    global Expense
    def build(self):
        global Expense
        global MonthlyBudget
        main_layout = GridLayout(cols=2)


        try:
            conn = sqlite3.connect("expense_budget.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses ORDER BY Id DESC")
            result = cursor.fetchone()
            conn.close()
            print(result)
            if result is not None:
                id, date, exp, bud = result
                self.total_expense=Label(text=str(int(exp)),pos=(200,500),size_hint=(0.5,0.1))
                main_layout.add_widget(self.total_expense)
                self.monthly_budget=Label(text=str(int(bud)),pos=(200,450),size_hint=(0.5,0.1))
                main_layout.add_widget(self.monthly_budget)
                
                
        except:
            self.total_expense=Label(text=str(Expense),pos=(200,500),size_hint=(0.3,0.1))
            main_layout.add_widget(self.total_expense)
            self.monthly_budget=Label(text=str(MonthlyBudget),pos=(200,450),size_hint=(0.3,0.1))
            main_layout.add_widget(self.monthly_budget)
        self.total_label=Label(text='Total Expenditure',pos=(50,500),size_hint=(0.3,0.1))
        main_layout.add_widget(self.total_label)
        self.budget_label=Label(text='Monthly Budget',pos=(50,450),size_hint=(0.3,0.1))
        main_layout.add_widget(self.budget_label)
        self.total_budget=Label(text='Total Budget',pos=(-50,400),size_hint=(0.3,0.1))
        main_layout.add_widget(self.total_budget)
        self.budget_input = TextInput(text='', pos=(200, 400), size_hint=(0.3, 0.1))
        main_layout.add_widget(self.budget_input)
        self.daily_expense=Label(text='Daily Expense',pos=(-50,300),size_hint=(0.3,0.1))
        main_layout.add_widget(self.daily_expense)
        self.expense_input = TextInput(text="", pos=(200, 300), size_hint=(0.3, 0.1))
        main_layout.add_widget(self.expense_input)
   
        self.report_button = Button(text='Reset', pos=(200, 200), size_hint=(0.3, 0.1))
        main_layout.add_widget(self.report_button)
        self.report_button.bind(on_press=self.reset)
        self.submit_button = Button(text='Submit', pos=(200, 150), size_hint=(0.3, 0.1))
        main_layout.add_widget(self.submit_button)
        self.submit_button.bind(on_press=self.submit)
        self.reset_button = Button(text='Report', pos=(200, 100), size_hint=(0.3, 0.1))
        main_layout.add_widget(self.reset_button)
        self.reset_button.bind(on_press=self.report)
        return main_layout
    
    def submit(self, instance):
        global Expense
        global MonthlyBudget
        current_date=datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            if int(self.monthly_budget.text)==0 and int(self.total_expense.text)==0:
                MonthlyBudget=int(self.budget_input.text)
                if self.expense_input.text=="":
                    expense=0
                else:
                    expense=int(self.expense_input.text)
                Expense=Expense+expense
                conn=sqlite3.connect('expense_budget.db')
                c=conn.cursor()
                c.execute("""CREATE TABLE IF NOT EXISTS expenses(Id integer primary key autoincrement, date text, total_expense real, budget real DEFAULT {})""".format(MonthlyBudget))
                c.execute("""INSERT INTO expenses(date,total_expense) values(?,?)""" ,(current_date,Expense))
                conn.commit()
                conn.close()
                self.budget_input.text=""
                self.expense_input.text=""
                self.monthly_budget.text=str(MonthlyBudget)
                self.total_expense.text=str(Expense)
                
            
            elif int(self.total_expense.text)>=0 and int(self.monthly_budget.text)>0:
                expense=int(self.expense_input.text)
                Expense=int(self.total_expense.text)
                Expense=Expense+expense
                conn=sqlite3.connect('expense_budget.db')
                c=conn.cursor()
                c.execute("""INSERT INTO expenses(date,total_expense) values(?,?)""" ,(current_date,Expense))
                result=c.execute('select * from expenses')
                conn.commit()
                conn.close()
                print(result)
                self.budget_input.text=""
                self.expense_input.text=""
                self.total_expense.text=str(Expense)
        except:
            pass


    def reset(self,instance):
        global MonthlyBudget
        global Expense
        MonthlyBudget=0
        Expense=0
        try:
            self.monthly_budget.text=str(MonthlyBudget)
            self.total_expense.text=str(Expense)
        except:
            pass
        try:
            conn=sqlite3.connect('expense_budget.db')
            c=conn.cursor()
            c.execute("DROP TABLE expenses")
            conn.close()
        except:
            pass

    def report(self,instance):
        
        conn=sqlite3.connect('expense_budget.db')
        cursor=conn.cursor()
        cursor.execute('Select sum(total_expense) from expenses')
        total_expense=cursor.fetchone()
        total_expense=total_expense[0]
        cursor.execute('Select budget from expenses')
        budget=cursor.fetchone()
        budget=budget[0]
        cursor.execute("SELECT strftime('%d', Date), sum(total_expense) FROM expenses GROUP BY strftime('%d', Date)")
        data=cursor.fetchall()
        conn.close()
        print(data)
        #Plot the histogram
        dates=[row[0] for row in data]
        expenses=[row[1] for row in data]

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].bar(dates,expenses)
        ax[0].set_xlabel('Date')
        ax[0].set_ylabel('Expense')
        ax[0].set_title('Expense Bar Chart')
        labels = ['Budget', 'Expenses']
        sizes = [budget, total_expense]

        ax[1].pie(sizes,labels=labels, startangle=90)
        ax[1].set_title('Expense vs Budget pie Chart')
        plt.savefig('Expense Chart.png')

if __name__ == '__main__':
    BudgetApp().run()

