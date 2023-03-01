from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from PyDictionary import PyDictionary
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class DictionaryApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.input_word = TextInput(text='', font_size=40)
        layout.add_widget(self.input_word)

        self.display = TextInput(text='', readonly=True, font_size=30)
        layout.add_widget(self.display)

        btn = Button(text='Find Meaning', font_size=40)
        btn.bind(on_press=self.on_button_press)
        layout.add_widget(btn)

        return layout

    def on_button_press(self, instance):
        word = self.input_word.text

        dictionary=PyDictionary()

        meaning=dictionary.meaning(word)

        try:

            for key,values in meaning.items():

                key=key+":"
                for i in values:
                    key=key+i+","
            
                self.display.text=key
        except:
            self.display.text='Word Not Found'
        

if __name__ == '__main__':
    DictionaryApp().run()