from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.config import Config

# from win32api import GetSystemMetrics

Config.set('graphics', 'width', 1240)
Config.set('graphics', 'height', 620)
orange = [1, .6, 0, 1]


class ClientApp(App):
    def prepare_layout(self):
        parent_bl = BoxLayout(orientation='vertical', spacing=3)

        name = BoxLayout()
        al_name = AnchorLayout(anchor_x='left', anchor_y='center', padding=[10])
        al_user_name = AnchorLayout(anchor_x='right', anchor_y='center', padding=[10])
        gl_top = GridLayout(rows=1, size_hint=(1, .1))

        py = Label(text='Py', font_size='30sp', size_hint=(0.05, 1), color=(1, 1, 1, 1), bold=True)
        mess = Button(text='Messenger',
                      font_size='20sp',
                      size_hint=(.15, 1),
                      color=(0, 0, 0, 1),
                      background_color=orange,
                      background_normal='',
                      disabled=True,
                      background_disabled_normal='',
                      bold=True
                      )
        user_name = Label(text='User', font_size='30sp', size_hint=(.4, .1))

        name.add_widget(py)
        name.add_widget(mess)

        al_name.add_widget(name)
        al_user_name.add_widget(user_name)

        gl_top.add_widget(al_name)
        for i in range(5):
            gl_top.add_widget(Widget())
        gl_top.add_widget(al_user_name)

        parent_bl.add_widget(gl_top)

        fl_main = FloatLayout()

        fl_main.add_widget(TextInput(text='',
                                     disabled=True,
                                     background_disabled_normal='',
                                     background_color=[1, 1, 1, .8],
                                     size_hint=(.795, .89),
                                     pos_hint={'x': .005, 'y': .1},
                                     font_size='20sp'
                                     ))
        fl_main.add_widget(TextInput(size_hint=(.185, .89),
                                     disabled=True,
                                     background_disabled_normal='',
                                     background_color=[1, 1, 1, .8],
                                     pos_hint={'x': .81, 'y': .1},
                                     font_size='30sp'
                                     ))
        fl_main.add_widget(TextInput(size_hint=(.795, .09),
                                     pos_hint={'x': .005, 'y': .005},
                                     font_size='30sp',
                                     multiline=False,
                                     on_text_validate=self.sending
                                     ))
        fl_main.add_widget(Button(size_hint=(.185, .09),
                                  pos_hint={'x': .81, 'y': .005},
                                  text='Send',
                                  font_size='30sp',
                                  color=(0, 0, 0, 1),
                                  background_color=orange,
                                  background_normal='',
                                  bold=True,
                                  id='button_send',
                                  on_press=self.sending
                                  ))

        parent_bl.add_widget(fl_main)

        return parent_bl

    def build(self):
        layout = self.prepare_layout()

        layout.children[0].children[3].text += ""

        return layout

    def sending(self, instance):
        if instance.id == "button_send":
            self.sending(instance.parent.children[1])
        else:
            text = instance.text
            instance.text = ''
            print(text)


if __name__ == "__main__":
    ClientApp().run()

