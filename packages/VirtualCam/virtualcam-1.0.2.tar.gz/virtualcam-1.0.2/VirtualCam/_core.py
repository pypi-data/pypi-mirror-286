import numpy as np
from cv2 import VideoCapture,cvtColor,COLOR_BGR2RGB,COLOR_RGB2BGR,resize
from cv2.typing import MatLike
from PIL import ImageTk
from PIL.Image import fromarray,new
from os import system,getenv,mkdir,name as platform
from os.path import exists
from pyvirtualcam import Camera,PixelFormat
from keyboard import is_pressed,add_hotkey,remove_hotkey
from tkinter import *
from tkinter import filedialog as file,messagebox as mb
from configparser import ConfigParser
from threading import Thread
__all__=['SourceLoadError','SourceNotLoadError','VirCam','VirCamUI']
class SourceLoadError(Exception):
    pass
class SourceNotLoadError(Exception):
    pass
class VirCam:
    def __init__(self,width:int,height:int,fps:int|float,kill_keys:str='esc',fmt:PixelFormat=PixelFormat.RGB,device:str|None='Unity Video Capture'):
        '''
        Args:
            width,height: The desired width and height of the images sent to the virtual camera.
            fps: A float or an integer means how many frames(images) should be sent to the virtual camera to display.
            kill_keys: The key combination to stop the virtual camera.
            device: The name of virtual camera. The integrated installation of virtual camera is Unity Video Capture.
        '''
        self.width=width
        self.height=height
        self.fps=fps
        self.kill_keys=kill_keys
        self.fmt=fmt
        self.device=device
        self.path='/'.join(__file__.split('\\')[:-1])+'/'
        self.video=[]
        self.running=[]
        self.doing={}
        self.args=[self.width,self.height,self.fps,self.kill_keys,self.device]
    def config(self,width:int,height:int,fps:int|float,kill_keys:str='esc',fmt:PixelFormat=PixelFormat.RGB,device:str|None=None):
        '''
        Change the configuration of the Virtual Camera.
        
        Args:
            width,height: The desired width and height of the images sent to the virtual camera.
            fps: A float or an integer means how many frames(images) should be sent to the virtual camera to display.
            kill_keys: The key combination to stop the virtual camera.
            device: The name of virtual camera. The integrated installation of virtual camera is Unity Video Capture.
        '''
        self.width=width
        self.height=height
        self.fps=fps
        self.kill_keys=kill_keys
        self.fmt=fmt
        self.device=device
        self.args=[self.width,self.height,self.fps,self.kill_keys,self.device]
    def install(self):
        '''
        Install one virtual camera.(Only for Windows)
        '''
        if platform=='nt':
            system(self.path+'Install.bat')
    def mulinstall(self):
        '''
        Install multiple virtual cameras. Change the amount of virtual cameras into the number you entered.(Onlt for Windows)
        '''
        if platform=='nt':
            system(self.path+'InstallMultipleDevices.bat')
    def uninstall(self):
        '''
        Uninstall all virtual cameras.(Only for Windows)
        '''
        if platform=='nt':
            system(self.path+'Uninstall.bat')
    def load(self,path:str):
        '''
        Load the specific image or video.
        Args:
            path: The path of the source you'd like to load.
        '''
        if not exists(path):
            raise FileNotFoundError("This file doesn't exist.")
        cap=VideoCapture(path)
        if not cap.isOpened():
            raise SourceLoadError("This file can't be loaded.")
        self.video=[]
        while True:
            ret,frame=cap.read()
            if not ret:
                break
            self.video.append(cvtColor(frame,COLOR_BGR2RGB))
    def resize(self,x:int,y:int,a:int,b:int):
        if a*y//x<=b:
            w=a
            h=a*y//x
        else:
            w=b*x//y
            h=b
        return (w,h)
    def solve(self,img,x:int=None,y:int=None):
        if x==None:
            x=self.width
        if y==None:
            y=self.height
        img=fromarray(img)
        img=img.resize(self.resize(img.width,img.height,x,y))
        ret=new('RGB',(x,y),(255,255,255))
        a=(ret.width-img.width)//2
        b=(ret.height-img.height)//2
        ret.paste(img,(a,b))
        return ret
    def close(self,device:str):
        self.running.remove(device)
        del self.doing[device]
        mb.showinfo('Close',f"{device} closed.")
    def display(self,not_ui=True):
        '''
        Run the virtual camera with the specific source.
        Args:
            not_ui: Don't change it.
        '''
        if self.video==[]:
            raise SourceNotLoadError("There isn't an available source loaded.")
        args=self.args
        video=self.video
        fmt=self.fmt
        cur=0
        step=1
        with Camera(args[0],args[1],args[2],fmt=fmt,device=args[4]) as cap:
            while (not_ui or self.doing[args[4]]) and not is_pressed(args[3]):
                cap.send(np.array(self.solve(video[cur])))
                cur+=step
                if cur<0 or cur>=len(self.video):
                    step=-step
                    cur+=step
                cap.sleep_until_next_frame()
        if not not_ui:
            self.close(args[4])
    def rgbwheel(self,start_color:tuple[int,int,int]=(255,0,0),reverse:bool=False,not_ui:bool=True):
        '''
        Run the virtual camera with color wheel.
        Args:
            start_color: The color that start with.
            reverse: Reverse or not.
            not_ui: Don't change it.
        '''
        color=start_color
        args=self.args
        fmt=self.fmt
        img=np.zeros((args[1],args[0],3),np.uint8)
        with Camera(args[0],args[1],args[2],fmt=fmt,device=args[4]) as cap:
            while (not_ui or self.doing[args[4]]) and not is_pressed(args[3]):
                img[:]=color
                cap.send(img)
                if reverse:
                    b,g,r=color
                else:
                    r,g,b=color
                if r==255 and 0<b<=255 and g==0:
                    b-=1
                if r==255 and 0<=g<255 and b==0:
                    g+=1
                if g==255 and 0<r<=255 and b==0:
                    r-=1
                if g==255 and 0<=b<255 and r==0:
                    b+=1
                if b==255 and 0<g<=255 and r==0:
                    g-=1
                if b==255 and 0<=r<255 and g==0:
                    r+=1
                if reverse:
                    color=(b,g,r)
                else:
                    color=(r,g,b)
                cap.sleep_until_next_frame()
        if not not_ui:
            self.close(args[4])
    def rgbimg(self,img_color:tuple[int,int,int]=(0,255,0),not_ui=True):
        '''
        Run the virtual camera with a single-colored image.
        Args:
            img_color: The color of the image you want to display.
            not_ui: Don't change it. 
        '''
        img=np.zeros((self.height,self.width,3),np.uint8)
        img[:]=img_color
        self.img(cvtColor(img,COLOR_RGB2BGR),not_ui)
    def img(self,img:MatLike,not_ui=True):
        '''
        Run the virtual camera with a MatLike image.
        Args:
            img: The image you want to display.
            not_ui: Don't change it.
        '''
        h,w=img.shape[:2]
        args=self.args
        fmt=self.fmt
        img=cvtColor(img,COLOR_BGR2RGB)
        with Camera(w,h,args[2],fmt=fmt,device=args[4]) as cap:
            while (not_ui or self.doing[args[4]]) and not is_pressed(args[3]):
                cap.send(img)
                cap.sleep_until_next_frame()
        if not not_ui:
            self.close(args[4])
class VirCamUI(VirCam):
    def top(self,page:Tk|Toplevel):
        page.attributes('-topmost',True)
        page.attributes('-topmost',False)
    def centerwin(self,page:Tk|Toplevel,w:int,h:int):
        scrnw=page.winfo_screenwidth()
        scrnh=page.winfo_screenheight()
        x=(scrnw/2)-(w/2)
        y=(scrnh/2)-(h/2)
        page.geometry('%dx%d+%d+%d'%(w,h,int(x),int(y)))
    def load_source(self,event=None):
        fpath=file.askopenfilename()
        if fpath!='':
            try:
                self.load(fpath)
                mb.showinfo('Success','Load the source successfully.')
            except FileNotFoundError:
                mb.showerror('FileNotFoundError',"The given source doesn't exist.")
                self.top(self.win)
            except SourceLoadError:
                mb.showerror('SourceLoadError','Failed to load the specific source.')
                self.top(self.win)
    def check_config(self,sv:list):
        try:
            w=sv[0].get()
            h=sv[1].get()
            fps=sv[2].get()
            kill_keys=sv[3].get()
            device=sv[4].get()
        except:
            mb.showerror('TypeError',"The arguments given as config are incorrect in type.")
            return False
        if fps==int(fps):
            fps=int(fps)
        def empty():
            pass
        try:
            add_hotkey(kill_keys,empty)
            remove_hotkey(kill_keys)
        except:
            mb.showerror('ValueError',"The kill_keys don't exist.")
            return False
        try:
            Camera(100,100,30,device=device)
        except:
            mb.showerror('CameraNotFoundError',"The specific virtual camera doesn't exist.")
            return False
        self.width=w
        self.height=h
        self.fps=fps
        self.kill_keys=kill_keys
        self.device=device
        self.sv=sv
        self.args=[self.width,self.height,self.fps,self.kill_keys,self.device]
        for i in range(len(self.lbs)):
            self.lbs[i].config(text=self.args[i])
        return True
    def edit_config(self,page:Toplevel,sv:list):
        if self.previewing:
            self.configing=False
            mb.showerror('Error',"You can't change config whle previewing. Press 'preview' to stop previewing.")
            page.destroy()
        elif self.check_config(sv):
            mb.showinfo('Success','Change the config successfully.')
            self.configing=False
            page.destroy()
        else:
            self.top(page)
    def save_config(self,event=None):
        filename=file.asksaveasfilename(defaultextension='.ini',filetypes=[('Configuration Files','*.ini')],initialfile='config.ini',initialdir=self.config_path)
        if filename=='':
            return
        cfg=ConfigParser()
        cfg.add_section('Settings')
        for i in range(len(self.txts)):
            cfg.set('Settings',self.txts[i],str(self.args[i]))
        with open(filename,'w') as cfgfile:
            cfg.write(cfgfile)
    def import_config(self,event=None):
        filename=file.askopenfilename(defaultextension='.ini',filetypes=[('Configuration Files','*.ini')],initialdir=self.config_path)
        if filename=='':
            return
        cfg=ConfigParser()
        cfg.read(filename)
        if not cfg.has_section('Settings'):
            mb.showerror('ImportConfigError',"The specific config file is incorrect in format.")
            return
        for txt in self.txts:
            if not cfg.has_option('Settings',txt):
                mb.showerror('ImportConfigError',"The specific config file is incorrect in format.")
                return
        sv=[IntVar(),IntVar(),DoubleVar(),StringVar(),StringVar()]
        sv[0].set(int(cfg.get('Settings','width')))
        sv[1].set(int(cfg.get('Settings','height')))
        fps=float(cfg.get('Settings','fps'))
        if int(fps)==fps:
            fps=int(fps)
        sv[2].set(fps)
        sv[3].set(cfg.get('Settings','kill_keys'))
        sv[4].set(cfg.get('Settings','device'))
        self.show(sv)
    def show(self,sv:list|None=None):
        if self.configing:
            return
        self.configing=True
        page=Toplevel(self.win)
        page.title('Config')
        self.centerwin(page,210,150)
        e=list[Entry]()
        if sv==None:
            sv=[IntVar(),IntVar(),DoubleVar(),StringVar(),StringVar()]
            for i in range(len(sv)):
                sv[i].set(self.args[i])
        for i in range(len(self.txts)):
            e.append(Entry(page))
            e[i].config(textvariable=sv[i])
            lb=Label(page,text=self.txts[i]+':',fg='green')
            lb.grid(row=i,column=0)
            e[i].grid(row=i,column=1,columnspan=2)
        bt=Button(page,text='Confirm',fg='green',command=lambda:self.edit_config(page,sv))
        bt.grid(row=5,column=1)
        def close():
            page.destroy()
            self.configing=False
        page.protocol('WM_DELETE_WINDOW',close)
        page.bind('<Return>',lambda func:bt.invoke())
        self.top(page)
        page.focus_set()
        page.mainloop()
    def start(self):
        if self.video!=[]:
            if not self.device in self.running:
                self.running.append(self.device)
                self.previewing=False
                self.doing[self.device]=True
                Thread(target=lambda:self.display(False),daemon=True).start()
                mb.showinfo('Success','Start virtual camera successfully.')
                self.win.focus_set()
            else:
                mb.showerror('RuntimeError',"This virtual camera is already running.")
        else:
            mb.showerror('SourceNotLoadError',"There's no source loaded.")
    def wheel(self,reverse=False):
        if not self.device in self.running:
            self.running.append(self.device)
            self.previewing=False
            self.doing[self.device]=True
            Thread(target=lambda:self.rgbwheel(not_ui=False,reverse=reverse),daemon=True).start()
            mb.showinfo('Success','Start virtual camera successfully.')
            self.win.focus_set()
        else:
            mb.showerror('RuntimeError',"This virtual camera is already running.")
    def startsc(self,color,page:Toplevel):
        if not self.device in self.running:
            self.running.append(self.device)
            self.previewing=False
            self.doing[self.device]=True
            page.destroy()
            Thread(target=lambda:self.rgbimg(color,False),daemon=True).start()
            mb.showinfo('Success','Start virtual camera successfully.')
            self.win.focus_set()
        else:
            mb.showerror('RuntimeError',"This virtual camera is already running.")
            page.focus_set()
    def single_color(self):
        page=Toplevel(self.win)
        page.title('Single Color')
        self.centerwin(page,250,200)
        v=[IntVar(),IntVar(),IntVar()]
        sc=[]
        e=[]
        for i in range(3):
            sc.append(Scale(page,from_=0,to=255,orient='horizontal',variable=v[i],length=200))
            e.append(Entry(page,width=3,textvariable=v[i]))
            v[i].set(0)
            sc[i].grid(row=i,column=0)
            e[i].grid(row=i,column=1)
        lb=Label(page,text='███████████████████████████',fg='black')
        lb.grid(row=3,column=0,columnspan=2)
        bt=Button(page,text='Confirm',fg='green',command=lambda:self.startsc((v[0].get(),v[1].get(),v[2].get()),page))
        bt.grid(row=4,column=0,columnspan=2,pady=5)
        def HEX(num:int):
            ret=hex(num)[2:]
            if len(ret)<2:
                ret='0'+ret
            return ret
        def convert():
            lb.config(fg='#'+HEX(v[0].get())+HEX(v[1].get())+HEX(v[2].get()))
            page.after(100,convert)
        convert()
        page.mainloop()
    def preview(self):
        if self.previewing and self.video!=[]:
            w,h=self.resize(self.width,self.height,214,120)
            img=self.solve(self.video[self.cursor],w,h)
            img=ImageTk.PhotoImage(img)
            self.imglb.imgtk=img
            self.imglb.config(image=img)
            self.cursor+=self.step
            if self.cursor<0 or self.cursor>=len(self.video):
                self.step=-self.step
                self.cursor+=self.step
        self.win.after(round(1000/self.fps),self.preview)
    def prvbtcmd(self):
        if self.video!=[]:
            self.previewing=not self.previewing
    def __init__(self):
        self.width=320
        self.height=180
        self.fps=30
        self.kill_keys='esc'
        self.fmt=PixelFormat.RGB
        self.device='Unity Video Capture'
        self.args=[self.width,self.height,self.fps,self.kill_keys,self.device]
        self.configing=False
        self.path='/'.join(__file__.split('\\')[:-1])+'/'
        self.config_path='/'.join(getenv('APPDATA').split('\\')[:-1])+'/Local/VirCamUI/'
        if not exists(self.config_path):
            mkdir(self.config_path)
        self.video=[]
        self.previewing=False
        self.running=[]
        self.doing={}
        self.cursor=0
        self.step=1
        self.txts=['width','height','fps','kill_keys','device']
        self.win=Tk()
        self.win.title('VirCamUI')
        self.centerwin(self.win,320,205)
        bar=Menu(self.win)
        configbar=Menu(bar,tearoff=False)
        configbar.add_command(label='Edit',command=self.show)
        configbar.add_command(label='Import',command=self.import_config,accelerator='Ctrl+O')
        configbar.add_command(label='Save',command=self.save_config,accelerator='Ctrl+S')
        installbar=Menu(bar,tearoff=False)
        installbar.add_command(label='Install(Single)',command=self.install)
        installbar.add_command(label='Install(Multiple)',command=self.mulinstall)
        installbar.add_command(label='Uninstall',command=self.uninstall)
        rgbbar=Menu(bar,tearoff=False)
        rgbbar.add_command(label='Wheel',command=self.wheel)
        rgbbar.add_command(label='Wheel(Reverse)',command=lambda:self.wheel(True))
        rgbbar.add_command(label='Single Color',command=self.single_color)
        bar.add_command(label='Source',command=self.load_source,accelerator='Ctrl+N')
        bar.add_cascade(label='Config',menu=configbar)
        bar.add_cascade(label='Install',menu=installbar)
        bar.add_cascade(label='RGB',menu=rgbbar)
        self.win.config(menu=bar)
        self.win.bind('<Control-N>',self.load_source)
        self.win.bind('<Control-n>',self.load_source)
        self.win.bind('<Control-O>',self.import_config)
        self.win.bind('<Control-o>',self.import_config)
        self.win.bind('<Control-S>',self.save_config)
        self.win.bind('<Control-s>',self.save_config)
        pad=10
        self.lbs=[None,None,None,None,None]
        for i in range(len(self.txts)-1):
            lb=Label(self.win,fg='green',text=self.txts[i]+':')
            lb.grid(row=i,column=0,pady=pad)
            self.lbs[i]=Label(self.win,text=str(self.args[i]))
            self.lbs[i].grid(row=i,column=1,sticky='W',pady=pad)
        lb=Label(self.win,text=self.txts[-1]+':',fg='green')
        lb.grid(row=len(self.txts)-2,column=2,pady=pad)
        self.lbs[-1]=Label(self.win,text=str(self.args[-1]))
        self.lbs[-1].grid(row=len(self.txts)-2,column=3,sticky='W',pady=pad)
        self.imglb=Label(self.win)
        self.imglb.grid(row=0,column=2,columnspan=2,rowspan=3,padx=5)
        prvbt=Button(self.win,text='Preview',fg='green',command=self.prvbtcmd)
        dplbt=Button(self.win,text='Start',fg='green',command=self.start)
        prvbt.grid(row=len(self.txts)-1,column=2)
        dplbt.grid(row=len(self.txts)-1,column=3)
    def run(self):
        self.top(self.win)
        self.win.focus_set()
        self.preview()
        self.win.mainloop()
if __name__=='__main__':
    VirCamUI().run()