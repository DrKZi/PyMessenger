from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.config import Config
from kivy.clock import Clock

from mySocket import *
from threading import Thread
import time

# from win32api import GetSystemMetrics

Config.set('graphics', 'width', 1240)
Config.set('graphics', 'height', 620)
orange = [1, .6, 0, 1]


class ClientApp(App):
    msg = ''
    user = ''
    to = ''

    def __init__(self, **kwargs):
        super(ClientApp, self).__init__(**kwargs)

        self.layout = self.prepare_layout()

        self.my_socket = MySocket()
        self.listenerThread = Thread(target=self.get_data)
        self.listenerThread.start()

        self.popup = Popup()
        self.get_popup()

    def get_data(self):
        time.sleep(1)
        lock = False
        while True:
            self.msg = self.my_socket.get_data().decode()
            if self.msg[:7] == "USERADD":
                self.layout.children[0].children[2].add_widget(ToggleButton(text=str(self.msg[7:]),
                                                                            group="users",
                                                                            on_release=self._toggle,
                                                                            size_hint=(1, None),
                                                                            height=50,
                                                                            allow_no_selection=False
                                                                            ))
            elif self.msg[:6] == "SYSTEM":
                self.layout.children[0].children[3].text += "SYSTEM - "
                self.layout.children[0].children[3].text += self.msg[6:] + "\n"
            elif self.msg == "RESP":
                self.layout.children[0].children[3].text = ""
            elif self.msg:
                if not lock:
                    self.layout.children[0].children[3].text += self.msg + " - "
                    lock = True
                else:
                    self.layout.children[0].children[3].text += self.msg + "\n"
                    lock = False

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
        user_name = Label(text=self.user, font_size='30sp', size_hint=(.4, .1))

        name.add_widget(py)
        name.add_widget(mess)

        al_name.add_widget(name)
        al_user_name.add_widget(user_name)

        gl_top.add_widget(al_name)
        for i in range(4):
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
        bl_users = BoxLayout(size_hint=(.185, .89),
                             orientation="vertical",
                             pos_hint={'x': .81, 'y': .1},
                             )
        fl_main.add_widget(bl_users)
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
        return self.layout

    def sending(self, instance):
        if instance.id == "button_send":
            self.sending(instance.parent.children[1])
        else:
            text = instance.text
            instance.text = ''
            if self.my_socket:
                self.my_socket.send(self.to, text)

    def stop(self, *largs):
        del self.listenerThread
        self.my_socket.close()
        super(ClientApp, self).stop(largs)

    def _username(self):
        self.popup.open()

    def get_popup(self):
        bl_popup = BoxLayout(orientation='vertical', spacing='10', padding=[30, 20, 30, 20])
        bl_popup.add_widget(TextInput(font_size='30sp',
                                      size_hint=(0.75, 0.12),
                                      pos_hint={'x': 0.1, 'y': 0.4},
                                      multiline=False,
                                      on_text_validate=self._set_username
                                      ))
        bl_popup.add_widget(Button(text="OK",
                                   font_size='30sp',
                                   size_hint=(0.2, 0.1),
                                   pos_hint={'x': 0.4, 'y': 0.2},
                                   id='button_ok',
                                   on_press=self._set_username
                                   ))

        self.popup = Popup(title='Enter your username!',
                           content=bl_popup,
                           size_hint=(None, None),
                           size=(400, 200),
                           auto_dismiss=False)
        Clock.schedule_once(lambda dt: self._username(), 0.1)

    def _set_username(self, instance):
        if instance.id == "button_ok":
            self._set_username(instance.parent.children[1])
        else:
            self.user = instance.text
            if not self.user:
                return
            self.my_socket.set_name(self.user)
            self.popup.dismiss()
            self.layout.children[1].children[0].children[0].text = self.user

    def _toggle(self, instance):
        self.to = instance.text
        self.my_socket.select_user(self.to)


if __name__ == "__main__":
    ClientApp().run()

