import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from tela.tela import Aplicacao


class LoginWindow(Gtk.Window):

    def __init__(self):        
        Gtk.Window.__init__(self, title="Login nBackup")
        self.connect("destroy", Gtk.main_quit)

        self.set_resizable(False)
        #self.set_position(Gtk.WindowPosition.MOUSE)

        grid = Gtk.Grid(column_homogeneous=True, 
                        column_spacing=10, row_spacing=5)
        self.add(grid)
        self.set_border_width(6)

        lb_usuario = Gtk.Label("Login:")
        grid.add(lb_usuario)

        self.en_usuario = Gtk.Entry()
        grid.attach(self.en_usuario, 1, 0, 5, 1)

        lb_senha = Gtk.Label("Senha:")
        grid.attach_next_to(lb_senha, lb_usuario, Gtk.PositionType.BOTTOM, 1, 2)

        self.en_senha = Gtk.Entry()
        #self.en_senha.set_placeholder_text("Senha")
        self.en_senha.set_visibility(False)
        self.en_senha.set_invisible_char("*")
        grid.attach_next_to(self.en_senha, lb_senha, Gtk.PositionType.RIGHT, 5, 1)
        
        bt_entrar = Gtk.Button(label="Entrar")
        bt_entrar.connect("clicked", self.on_entrar_clicked)
        grid.attach_next_to(bt_entrar, lb_senha, Gtk.PositionType.BOTTOM, 3, 1)

        bt_cancelar = Gtk.Button(label="Cancelar")
        bt_cancelar.connect("clicked", self.on_cancelar_clicked)
        grid.attach_next_to(bt_cancelar, bt_entrar, Gtk.PositionType.RIGHT, 3, 1)

        
    def on_entrar_clicked(self, widget):        
        self.show_aplicacao()           

    def on_cancelar_clicked(self, widget):
        sys.exit()

    def show_aplicacao(self):
        w = Aplicacao()
        exit_status = w.run(sys.argv)
        sys.exit(exit_status)

    def show_login(self):
        self.show_all()
        Gtk.main()

        
    
