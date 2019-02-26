import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

software_list = [("Firefox", 2002,  "C++"),
                 ("Eclipse", 2004, "Java" ),
                 ("Pitivi", 2004, "Python"),
                 ("Pitivi", 2004, "Python"),
                 ("Pitivi", 2004, "Python")]

agenda_lst = [("Serv Empresa", "20/01/2019","10:00"),
              ("Serv Notas Fiscais", "20/01/2019","12:00"),
              ("Serv PDV", "20/01/2019","15:00")]

class InicioWindow(Gtk.ApplicationWindow):
    
    def __init__(self, app):
        Gtk.Window.__init__(self, title="nBackup - Backup remoto", application=app)
        self.set_default_size(630, 400)
        self.set_border_width(10)
        
        self.grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        #self.grid.set_column_homogeneous(True)
        #self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        lb_status_clientes = Gtk.Label("Status Clientes")
        self.grid.add(lb_status_clientes)

        self.liststore = Gtk.ListStore(str, int, str)
        for software_ref in software_list:
            self.liststore.append(list(software_ref))
        self.current_filter_language_status = None

        self.filter = self.liststore.filter_new()
        self.filter.set_visible_func(self.filter_func)
        
        self.treeview = Gtk.TreeView.new_with_model(self.filter)
        for i, column_title in enumerate(["Software", "Release Year", "Language"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        scroll_clientes = Gtk.ScrolledWindow()
        scroll_clientes.set_hexpand(True)
        scroll_clientes.set_min_content_height(150)
        scroll_clientes.set_min_content_width(250)
        self.grid.attach_next_to(scroll_clientes, lb_status_clientes, Gtk.PositionType.BOTTOM, 1, 2)
        scroll_clientes.add(self.treeview)

        lb_proximas_execucoes = Gtk.Label("Próximas Execuções")
        self.grid.attach_next_to(lb_proximas_execucoes, lb_status_clientes, Gtk.PositionType.RIGHT, 2, 1)

        self.list_exec = Gtk.ListStore(str, str, str)
        for e in agenda_lst:
            self.list_exec.append(list(e))
        self.filtro_execucao = None

        self.filtro = self.list_exec.filter_new()
        self.filtro.set_visible_func(self.filtro_execucoes)

        self.tree_execucoes = Gtk.TreeView.new_with_model(self.filtro)
        for i, titulo_col in enumerate(["Cliente","Data","Hora"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(titulo_col, renderer, text=i)
            self.tree_execucoes.append_column(column)

        
        self.scroll_exec = Gtk.ScrolledWindow()
        self.scroll_exec.set_hexpand(True)
        self.scroll_exec.set_min_content_height(150)
        self.grid.attach_next_to(self.scroll_exec, lb_proximas_execucoes, Gtk.PositionType.BOTTOM, 2, 2)
        self.scroll_exec.add(self.tree_execucoes)


        copy_action = Gio.SimpleAction.new("copy", None)
        copy_action.connect("activate", self.copy_callback)
        self.add_action(copy_action)

        paste_action = Gio.SimpleAction.new("paste", None)
        paste_action.connect("activate", self.paste_callback)
        self.add_action(paste_action)

        shape_action = Gio.SimpleAction.new_stateful(
            "shape", GLib.VariantType.new('s'),
            GLib.Variant.new_string('line'))
        shape_action.connect("activate", self.shape_callback)
        self.add_action(shape_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_callback)
        self.add_action(about_action)

    def filter_func(self, model, iter, data):
        
        if self.current_filter_language_status is None or self.current_filter_language_status == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language_status
    
    def filtro_execucoes(self, model, iter, data):
        
        if self.filtro_execucao is None or self.filtro_execucao == "None":
            return True
        else:
            return model[iter][2] == self.filtro_execucao
        

    def copy_callback(self, action, param):
        print("copy activated")
    
    def paste_callback(self, action, param):
        print("paste activated")

    def shape_callback(self, action, param):
        print("Shape is set to", param.get_string())
        action.set_state(param)

    def about_callback(self, action, param):
        aboutdialog = Gtk.AboutDialog()

        authors = ["GNOME Documentation Team"]
        documenters = ["GNOME Documentation Team"]

        aboutdialog.set_program_name("MenuBar Example")
        aboutdialog.set_copyright("Copyright \xc2\xa9 2012 GNOME Documentation Team")
        aboutdialog.set_authors(authors)
        aboutdialog.set_documenters(documenters)
        aboutdialog.set_website("http://developer.gnome.org")
        aboutdialog.set_website_label("GNOME Developer Website")

        aboutdialog.connect("response", self.on_close)
        aboutdialog.show()

    


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)
        

    def do_activate(self):
        win = InicioWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        new_action = Gio.SimpleAction.new("novo_cliente", None)
        new_action.connect("activate", self.novo_cliente)
        self.add_action(new_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_callback)
        self.add_action(quit_action)

        state_action = Gio.SimpleAction.new_stateful(
            "state", GLib.VariantType.new('s'), GLib.Variant.new_string('off'))
        state_action.connect("activate", self.state_callback)
        self.add_action(state_action)

        awesome_action = Gio.SimpleAction.new_stateful(
            "awesome", None, GLib.Variant.new_boolean(False))
        awesome_action.connect("activate", self.awesome_callback)
        self.add_action(awesome_action)

        builder = Gtk.Builder()

        try:
            builder.add_from_file("menubar.ui")
        except:
            print("file not found")
            sys.exit()
        
        self.set_menubar(builder.get_object("menubar"))
        self.set_app_menu(builder.get_object("appmenu"))
        
        
    def novo_cliente(self, action, parameter):
        print("clicked New")

    def quit_callback(self, action, parameter):
        print("You clicked quit")
        sys.exit()

    def state_callback(self, action, parameter):
        print("State is set to", parameter.get_string())
        action.set_state(parameter)

    def awesome_callback(self, action, parameter):
        action.set_state(GLib.Variant.new_boolean(not action.get_state()))
        if action.get_state().get_boolean() is True:
            print("You checked Awesome")
        else:
            print("You unchecked Awesome")
 

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)

