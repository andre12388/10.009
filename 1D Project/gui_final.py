from firebase import firebase

url = "https://padiworld-84347.firebaseio.com/" # URL to Firebase database
token = "QTaA7OMmsgQ8uHGxz9c2wYpOliqem0QrFWGLvfkD" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button  
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, BorderImage, Line
from kivy.uix.image import AsyncImage, Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class LogInScreen(Screen):
    def __init__(self,**kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = FloatLayout(size=(300,300))
        
        """Add background""" 
        with self.canvas.before:
            self.img = BorderImage(source = 'sign in page.jpg',
                                   pos=self.pos,
                                   size=self.size)

        #Ensure that everytime the BorderImage is updated, it's repositioned correctly
        self.bind(pos=self.update_img, size=self.update_img)
        
        """Check Label to tell incorrect inputs"""    
        self.Check = Label(text='',
                           color=[1,0,0,1],
                           font_size=20,
                           pos_hint={'left':0.1, 'center_y':0.125})
        self.layout.add_widget(self.Check)
        
        """Username Label"""
        self.Username = TextInput(text='',
                                  size_hint=(0.218,0.06),
                                   pos_hint={'center_x': 0.499,'center_y': 0.42})
        self.layout.add_widget(self.Username)
        
        """Password Label"""
        self.Password = TextInput(text='',
                                  size_hint=(0.218,0.06),
                                  pos_hint={'center_x': 0.499,'center_y': 0.312},
                                  password_mask=True,
                                  password=True)
        self.layout.add_widget(self.Password)
        
        """Sign In Button"""        
        self.signin = Button(text='Sign In',
                             background_color=[0,0,0,0],
                             color=[0,0,0,0],
                             font_size=30,
                             size_hint=(0.10,0.10),
                             pos_hint={'center_x': 0.7, 'center_y': .60},
                             on_press=self.check)
        self.layout.add_widget(self.signin)
        
        """Sign Up Button"""        
        self.signup = Button(text='Sign Up',
                             background_color=[0,0,0,0],
                             color=[0,0,0,0],
                             font_size=30,
                             size_hint=(0.10,0.10),
                             pos_hint={'center_x': 0.81, 'center_y': .64},
                             on_press = self.signup)
        self.layout.add_widget(self.signup)
        
        """Easter Egg! Pls ignore!"""
        self.funBut = Button(text='',
                             background_color=[0,0,0,0],
                             on_press=self.fun,size_hint=(0.05,0.05),
                             pos_hint={'center_x': 0.02, 'center_y': .99})
        self.layout.add_widget(self.funBut)
        self.count = 0
        
        """Add everything to screen"""
        self.add_widget(self.layout)
        
        
    """Easter Egg Function"""
    def fun(self,instance):
        self.count += 1
        if self.count == 3:
            sound = SoundLoader.load('Banana.mp3')
            sound.play()
            self.count = 0
            
    """Resizing Canvas When App Size Change Function"""            
    def update_img(self, *args):
        self.img.pos = self.pos
        self.img.size = self.size

    """Check Username and Password for Log In"""         
    def check(self,instance):
        Users = firebase.get('/Users')                                          #get dictionary of users
        try:
            if str(self.Password.text) == Users[self.Username.text]:            #if value mtaches key for dictionary
                PS.Name.text = self.Username.text + "'s\n   Farm"               #Edit farm name in PlantSelect Screen
                sound = SoundLoader.load('Illumination.wav')                    #Load sound
                sound.play()
                self.Check.text = ''                                            #Clean up
                self.Username.text = ''
                self.Password.text = ''
                self.manager.transition = RiseInTransition(duration = 2)
                self.manager.current = 'PlantSelect'                            #Switch Screen
                
            else:
                self.Check.text = 'Invalid Password! Please Try Again!'
                sound = SoundLoader.load('What.mp3')
                sound.play()
                
        except KeyError:
            self.Check.text = 'Invalid Username! Press Sign Up to Sign an Account'
            sound = SoundLoader.load('What.mp3')
            sound.play()
        
    def signup(self,instance):
        self.manager.transition.direction = 'down'
        self.manager.current = 'SignUpScreen'
        self.Check.text = ''
        self.Username.text = ''
        self.Password.text = ''
        
class SignUpScreen(Screen):
    def __init__(self,**kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = FloatLayout(size=(300,300))

        with self.canvas.before:
            self.img = BorderImage(source = 'REGISTER.png',pos=self.pos, size=self.size)

        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
        self.bind(pos=self.update_img, size=self.update_img)
            
        self.Check = Label(text='',color=[1,1,1,1],font_size=20,pos_hint={'left': 0.1, 'center_y': .35})
        self.layout.add_widget(self.Check)

        self.Username = TextInput(text='',size_hint=(0.6,0.06),pos_hint={'x': 0.20,'center_y': 0.73})
        self.layout.add_widget(self.Username)

        self.Password = TextInput(text='',size_hint=(0.6,0.06),pos_hint={'x': 0.20,'center_y': 0.58},password_mask=True,password=True)
        self.layout.add_widget(self.Password)

        self.confirmPassword = TextInput(text='',size_hint=(0.6,0.06),pos_hint={'x': 0.20,'center_y': 0.43},password_mask=True,password=True)
        self.layout.add_widget(self.confirmPassword)
        
        self.Register = Button(text='Register',background_color=[0,0,0,0],color=[1,1,1,1],font_size=30,size_hint=(0.15,0.07),pos_hint={'center_x': 0.54, 'center_y': .21},on_press=self.register)
        self.layout.add_widget(self.Register)
        self.GoBack = Button(text='Go Back',background_color=[0,0,0,0],color=[1,1,1,1],font_size=30,size_hint=(0.15,0.07),pos_hint={'center_x': 0.455, 'center_y': .115},on_press=self.goback)
        self.layout.add_widget(self.GoBack)
        self.add_widget(self.layout)
        
    def update_img(self, *args):
        self.img.pos = self.pos
        self.img.size = self.size
        
    def register(self,instance):
        Users = firebase.get('/Users')
        username = str(self.Username.text)
        password = str(self.Password.text)
#        print self.Password.text.isdigit()
#        print self.confirmPassword.text.isdigit()
        if self.Password.text.isdigit() != True and self.confirmPassword.text.isdigit() != True:
            if Users.has_key(str(self.Username.text)) == False and self.Password.text == self.confirmPassword.text:
                print username, password
                Users[username]=password
                self.Check.text = 'Registered! Have Fun!'
                self.Username.text = ''
                self.Password.text=''
                self.confirmPassword.text=''
                firebase.put('/','Users',Users)
                
            elif Users.has_key(str(self.Username.text)):
                self.Check.text = 'Username is taken! Please try again!'
                self.Username.text = ''
                self.Password.text=''
                self.confirmPassword.text=''
                sound = SoundLoader.load('What.mp3')
                sound.play() 
                
        elif self.Password.text != self.confirmPassword.text:
            self.Check.text = 'Password do not match! Please check your password!'
            self.Password.text=''
            self.confirmPassword.text=''
            sound = SoundLoader.load('What.mp3')
            sound.play() 
            
        else:
            self.Check.text = 'Password contains only numbers! Please change!'
            self.Password.text=''
            self.confirmPassword.text=''
            sound = SoundLoader.load('What.mp3')
            sound.play()             
    
    def goback(self,instance):
        self.Check.text = ''
        self.Username.text = ''
        self.Password.text = ''
        self.confirmPassword.text = ''
        self.manager.transition.direction = 'up'
        self.manager.current = 'LogInScreen'

class PlantSelect(Screen):
    def __init__(self,**kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = FloatLayout(size=(300,300))

        with self.canvas.before:
            self.img = BorderImage(source = 'grid updated.jpg',pos=self.pos, size=self.size)

        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
        self.bind(pos=self.update_img, size=self.update_img)
            
        self.plant1 = Button(text='Plant1',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.125,'center_y': 0.625},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant1)
        self.plant2 = Button(text='Plant2',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.375,'center_y': 0.625},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant2)
        self.plant3 = Button(text='Plant3',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.625,'center_y': 0.625},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant3)
        self.plant4 = Button(text='Plant4',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.125,'center_y': 0.375},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant4)
        self.plant5 = Button(text='Plant5',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.375,'center_y': 0.375},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant5)
        self.plant6 = Button(text='Plant6',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.625,'center_y': 0.375},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant6)
        self.plant7 = Button(text='Plant7',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.125,'center_y': 0.125},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant7)
        self.plant8 = Button(text='Plant8',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.375,'center_y': 0.125},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant8)
        self.plant9 = Button(text='Plant9',font_size=40,background_normal='flower4.jpg',size_hint=(0.24,0.24),pos_hint={'center_x': 0.625,'center_y': 0.125},on_press=self.change_to_plant1)
        self.layout.add_widget(self.plant9)
        

        self.wateramount = Label(text='10'+' L',color=[0,0,0,1],font_size=30,pos_hint={'center_x': 0.19, 'center_y': .855})
        self.layout.add_widget(self.wateramount)

        self.fertilizeramount =Label(text='2'+' Kg',color=[0,0,0,1],font_size=30,pos_hint={'center_x': 0.42, 'center_y': .855})
        self.layout.add_widget(self.fertilizeramount)

        self.pointcount = Label(text='2000',color=[0,0,0,1],font_size=30,pos_hint={'center_x': 0.65, 'center_y': .855})
        self.layout.add_widget(self.pointcount)
        
        self.Name = Label(text='',color=[0,0,0,1], font_size = 17, pos_hint={'center_x': 0.865,'center_y':0.855})
        self.layout.add_widget(self.Name)
        
        self.logout = Button(text='Logout',background_color=[0,1,0,1],color=[0,0,0,1],font_size=20,size_hint=(0.12,0.05),pos_hint={'center_x': 0.86, 'center_y': .73},on_press=self.logout)
        self.layout.add_widget(self.logout)
        self.add_widget(self.layout)
        
    def update_img(self, *args):
        self.img.pos = self.pos
        self.img.size = self.size
        
    def change_to_plant1(self,instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'plant 1'
        
    def logout(self,instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'LogInScreen'
     
class Plant1(Screen):
    def __init__(self,**kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = FloatLayout(size=(300,300))

        with self.canvas.before:
            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)

        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
        self.bind(pos=self.update_img, size=self.update_img)
            

        self.TemperatureReading=Label(text='Temperature\n  '+'24',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
        self.layout.add_widget(self.TemperatureReading)
        self.LightIntensity=Label(text='Light Intensity\n  '+'300',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
        self.layout.add_widget(self.LightIntensity)
        self.Humidity=Label(text='Humidity\n  '+'64',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
        self.layout.add_widget(self.Humidity)
        self.Moisture=Label(text='Moisture\n  '+'15000',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
        self.layout.add_widget(self.Moisture)
               

        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
        self.layout.add_widget(self.Plant)
        
        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
        self.layout.add_widget(self.LightIntensityL)
        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
        self.layout.add_widget(self.LightIntensity)
        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
        self.layout.add_widget(self.LightIntensityV)
        
        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
        self.layout.add_widget(self.TemperatureL)
        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
        self.layout.add_widget(self.TemperatureSlider)
        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
        self.layout.add_widget(self.TemperatureV)
        
        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
        self.layout.add_widget(self.HumidityL)
        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
        self.layout.add_widget(self.HumiditySlider)
        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
        self.layout.add_widget(self.HumidityV)
        
        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
        self.layout.add_widget(self.MoistureL)
        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
        self.layout.add_widget(self.MoistureSlider)
        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
        self.layout.add_widget(self.MoistureV)
        
        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
        self.layout.add_widget(self.inc_temp)
        
        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
        self.layout.add_widget(self.inc_moist)
        
        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
        self.layout.add_widget(self.light)
        
        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
        self.layout.add_widget(self.water)
        
        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
        self.layout.add_widget(self.goback)
        self.add_widget(self.layout)
        Clock.schedule_interval(self.callback,30)
        
    def update_img(self, *args):
        self.img.pos = self.pos
        self.img.size = self.size
    
    def adjustT(self,instance):
        firebase.put('/','GameMaster/Plant1/tempt switch','on')
        
    def adjustH(self,instance):
        firebase.put('/','GameMaster/Plant1/humidity switch','on')
    
    def adjustL(self,instance):
        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
    
    def adjustM(self,instance):
        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
    
    def GoBack(self,instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'PlantSelect'
        
    def callback(self,dt):
        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
        self.TemperatureSlider.value = PlantTemp
        self.TemperatureV.text = str(PlantTemp)
        
        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
        self.HumiditySlider.value = PlantHum
        self.HumidityV.text = str(PlantHum)
                
        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
        self.MoistureSlider.value = PlantMois
        self.MoistureV.text = str(PlantMois)
        
        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
        self.LightIntensity.value = PlantLight
        self.LightIntensityV.text = str(PlantLight)
        
#class Plant2(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant1/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant1/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant3(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant1/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant1/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant4(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant1/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant1/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant5(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant1/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant1/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant6(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant6/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant6/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant6/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant6/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant7(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant1/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant1/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant8(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant8/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant8/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant8/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant8/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
#        
#class Plant9(Screen):
#    def __init__(self,**kwargs):
#        Screen.__init__(self, **kwargs)
#        self.layout = FloatLayout(size=(300,300))
#
#        with self.canvas.before:
#            self.img = BorderImage(source = 'plant updated.jpg',pos=self.pos, size=self.size)
#
#        #Ensure that everytime the Rectangle is updated, it's repositioned correctly
#        self.bind(pos=self.update_img, size=self.update_img)
#            
#
#        self.TemperatureReading=Label(text='Temperature\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.80})
#        self.layout.add_widget(self.TemperatureReading)
#        self.LightIntensity=Label(text='Light Intensity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.22,'center_y': 0.80})
#        self.layout.add_widget(self.LightIntensity)
#        self.Humidity=Label(text='Humidity\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.36,'center_y': 0.80})
#        self.layout.add_widget(self.Humidity)
#        self.Moisture=Label(text='Moisture\n  '+'27',background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.50,'center_y': 0.80})
#        self.layout.add_widget(self.Moisture)
#               
#
#        self.Plant=Image(source='flower3.jpg',size_hint=(0.50,0.50),pos_hint={'center_x': 0.782,'center_y': 0.748})
#        self.layout.add_widget(self.Plant)
#        
#        self.LightIntensityL=Label(text='Light Intensity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.1,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityL)
#        self.LightIntensity=Slider(min=0,max=1000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.55},disabled=True)
#        self.layout.add_widget(self.LightIntensity)
#        self.LightIntensityV=Label(text=str(self.LightIntensity.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.6})
#        self.layout.add_widget(self.LightIntensityV)
#        
#        self.TemperatureL=Label(text='Temperature',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.095,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureL)
#        self.TemperatureSlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.40},disabled=True)
#        self.layout.add_widget(self.TemperatureSlider)
#        self.TemperatureV=Label(text=str(self.TemperatureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.45})
#        self.layout.add_widget(self.TemperatureV)
#        
#        self.HumidityL=Label(text='Humidity',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityL)
#        self.HumiditySlider=Slider(min=0,max=100,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.25},disabled=True)
#        self.layout.add_widget(self.HumiditySlider)
#        self.HumidityV=Label(text=str(self.HumiditySlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.30})
#        self.layout.add_widget(self.HumidityV)
#        
#        self.MoistureL=Label(text='Moisture',color=[0,0,0,1],background=[1,1,1,1],font_size=17,pos_hint={'center_x': 0.08,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureL)
#        self.MoistureSlider=Slider(min=0,max=30000,size_hint=(0.4,0.10),color=[0,0,0,1],pos_hint={'center_x': 0.25,'center_y': 0.10},disabled=True)
#        self.layout.add_widget(self.MoistureSlider)
#        self.MoistureV=Label(text=str(self.MoistureSlider.value),color=[0,0,0,1],font_size=20,pos_hint={'center_x': 0.4,'center_y': 0.15})
#        self.layout.add_widget(self.MoistureV)
#        
#        self.inc_temp = Button(text='temp',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.374},on_press=self.adjustT)
#        self.layout.add_widget(self.inc_temp)
#        
#        self.inc_moist = Button(text='humidity',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.642,'center_y': 0.185},on_press=self.adjustH)
#        self.layout.add_widget(self.inc_moist)
#        
#        self.light = Button(text='light',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.374},on_press=self.adjustL)
#        self.layout.add_widget(self.light)
#        
#        self.water = Button(text='moisture',font_size=40,background_color=[0,0,0,0],size_hint=(0.222,0.245),pos_hint={'center_x': 0.87,'center_y': 0.185},on_press=self.adjustM)
#        self.layout.add_widget(self.water)
#        
#        self.goback = Button(text='<== Go Back',font_size=10,size_hint=(0.1,0.05),pos_hint={'center_x': 0.05,'center_y': 0.98},on_press=self.GoBack)
#        self.layout.add_widget(self.goback)
#        self.add_widget(self.layout)
#        Clock.schedule_interval(self.callback,30)
#        
#    def update_img(self, *args):
#        self.img.pos = self.pos
#        self.img.size = self.size
#    
#    def adjustT(self,instance):
#        firebase.put('/','GameMaster/Plant1/tempt switch','on')
#        
#    def adjustH(self,instance):
#        firebase.put('/','GameMaster/Plant1/humidity switch','on')
#    
#    def adjustL(self,instance):
#        firebase.put('/','GameMaster/Plant1/light intensity switch','on')
#    
#    def adjustM(self,instance):
#        firebase.put('/','GameMaster/Plant1/soil moisture switch','on')
#    
#    def GoBack(self,instance):
#        self.manager.transition.direction = 'left'
#        self.manager.current = 'PlantSelect'
#        
#    def callback(self,dt):
#        PlantTemp = firebase.get('/GameMaster/Plant1/tempt')
#        self.TemperatureSlider.value = PlantTemp
#        self.TemperatureV.text = str(PlantTemp)
#        
#        PlantHum = firebase.get('/GameMaster/Plant1/humidity')
#        self.HumiditySlider.value = PlantHum
#        self.HumidityV.text = str(PlantHum)
#                
#        PlantMois = firebase.get('/GameMaster/Plant1/soil moisture')
#        self.MoistureSlider.value = PlantMois
#        self.MoistureV.text = str(PlantMois)
#        
#        PlantLight = firebase.get('/GameMaster/Plant1/light intensity')
#        self.LightIntensity.value = PlantLight
#        self.LightIntensityV.text = str(PlantLight)
        
class SwitchScreenApp(App):
    def build(self):
        sm=ScreenManager()
        
        global LIS
        LIS = LogInScreen(name = 'LogInScreen')
        sm.add_widget(LIS)
        global SUS
        SUS = SignUpScreen(name = 'SignUpScreen')
        sm.add_widget(SUS)
        global PS
        PS = PlantSelect(name = 'PlantSelect')
        sm.add_widget(PS)
        global p1
        P1 = Plant1(name = 'plant 1')
        sm.add_widget(P1)
#        P2 = Plant2(name = 'plant 2')
#        sm.add_widget(P2)
#        P3 = Plant3(name = 'plant 3')
#        sm.add_widget(P3)
#        P4 = Plant4(name = 'plant 4')
#        sm.add_widget(P4)
#        P5 = Plant5(name = 'plant 5')
#        sm.add_widget(P5)
#        P6 = Plant6(name = 'plant 6')
#        sm.add_widget(P6)
#        P7 = Plant7(name = 'plant 7')
#        sm.add_widget(P7)
#        P8 = Plant8(name = 'plant 8')
#        sm.add_widget(P8)
#        P9 = Plant9(name = 'plant 9')
#        sm.add_widget(P9)
        
        sm.current='LogInScreen'
        return sm

SwitchScreenApp().run()        

