import socket
import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread


KV = """
MyBl:
	orientation: "vertical"
	
	Label:
		font_size: "18sp"
		miltiline: True
		text_size: self.width*0.98, self.height
		valign: 'top'
		size_hint_x: 1.0
		size_hint_y: 0.7
		height: self.texture_size[1] + 15
		text: root.data_label
		
	TextInput:
		id: Inp
		miltiline: False
		padding_y: (5,5)
		size_hint: (1, 0.2)
		on_text: app.process()
	
	Button:
		text: "Send message"
		
		bold: True
		background_color:'#70FF00'
		size_hint: (1,0.1)
		on_press: root.callback()
"""

class MyBl(BoxLayout):
	data_label = StringProperty("Welcome!\n")
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		SERVER = "146.19.247.186"
		PORT = 3000
		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.client.connect((SERVER, PORT))
		self.client.send('__join'.encode('ascii'))
		threading.Thread(target=self.get_data).start()
	
	def callback(self):
		msg = self.ids.Inp.text
		self.set_data_label("You: " + msg)
		self.client.send(msg.encode('ascii'))
		
	def get_data(self):
		UDP_MAX_SIZE = 65535
		while App.get_running_app().running:
			in_data = self.client.recv(UDP_MAX_SIZE)
			kkk = in_data.decode('ascii')
			self.set_data_label(kkk)
			
	@mainthread
	def set_data_label(self, data):
		self.data_label += str(data) + "\n"			
	
class MyApp(App):
	running = True
	
	def process(self):
		text = self.root.ids.Inp.text
	
	def build(self):
		return Builder.load_string(KV)
		
	def on_stop(self):
		self.running = False
		
MyApp().run()
