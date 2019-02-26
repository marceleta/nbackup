import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InicioWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="nBackup - Backup Remoto", application=app)
        self.set_default_size(200,200)


class Aplicacao(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = InicioWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder()
        
        try:
            builder.add_from_file("menubar.ui")
        except:
            print("file not found")
            sys.exit()

        self.set_menubar(builder.get_object("menubar"))

    
