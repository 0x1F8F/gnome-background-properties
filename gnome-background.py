#!/bin/python3
import sys
import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from gi.overrides.Gdk import Gdk


css_provider = Gtk.CssProvider()
css_provider.load_from_path('style.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class MainWindow(Gtk.ApplicationWindow):
    def __FILE_DIALOG(self,dialog,response):
        if response==Gtk.ResponseType.OK:
            self.files[self._req]= dialog.get_file().get_path()
            print(f"Selected : {self.files}")
        dialog.destroy()

    def __file_chooser(self,req):
        self._req = req
        print("\tOpening dialog ....")
        dialog = Gtk.FileChooserDialog( title=self._req ,parent=self, action = Gtk.FileChooserAction.OPEN)
        dialog.add_button("Cancel",Gtk.ResponseType.CANCEL)
        dialog.add_button("OK",Gtk.ResponseType.OK)
        dialog.connect("response", self.__FILE_DIALOG)
        dialog.show()

    def __Process(self,button):
        try:
            Dark = self.files.get("Dark")
            Light = self.files.get("Light")
            HOME = os.getenv("HOME")
            Path = "/.local/share/gnome-background-properties/Theme.xml.in"
            xml = f"""<?xml version="1.0"?>
    <!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
    <wallpapers>
      <wallpaper deleted="false">
        <name>Arch Background</name>
        <filename>{Light}</filename>
        <filename-dark>{Dark}</filename-dark>
        <options>zoom</options>
        <shade_type>solid</shade_type>
        <pcolor>#3071AE</pcolor>
        <scolor>#000000</scolor>
      </wallpaper>
    </wallpapers>"""
            print(f"\nDark:{Dark}\nLight:{Light}")

            with open(HOME+Path,"w") as file :
                file.write(xml)
            print("Successfully written")
            self.close()
        except Exception as err:
            print("[ Exception ] :",err)

    def __close_window(self,button):
        self.close()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._req = ""
        self.files = {
            "Title" : "/path/to/file"
        }
        self.set_default_size(600, 700)
        self.set_title("gnome-background-properties")
        lightImageBtn = Gtk.Button(label = "Light Wallpapper")
        lightImageBtn.set_margin_top(40)
        dareImageBtn = Gtk.Button(label = "Dark Wallpapper")

        okBtn = Gtk.Button(label = "OK")
        cancelBtn = Gtk.Button(label = "Cancel")
        cancelBtn.connect("clicked",self.__close_window)
        lightImageBtn.connect("clicked",lambda button: self.__file_chooser("Light"))
        dareImageBtn.connect("clicked",lambda button: self.__file_chooser("Dark"))
        okBtn.connect("clicked",self.__Process)


        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxSeperator = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxSeperator.set_hexpand(True)
        boxSeperator.set_vexpand(True)


        self.set_child(box)
        box.append(lightImageBtn)
        box.append(dareImageBtn)
        box.append(boxSeperator)

        box.append(box2)
        box2.append(cancelBtn)
        box2.append(okBtn)


class APP(Gtk.Application):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.connect("activate",self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = APP(application_id="com.0x1F8F.GnomeBackgroundProperties")
app.run(sys.argv)

