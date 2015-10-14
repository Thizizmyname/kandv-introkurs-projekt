import sys
from gi.repository import Gtk as gtk
	
class TutorialTextEditor:

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
     
    def __init__(self):
    
        builder = gtk.Builder()
        builder.add_from_file("test.xml") 
        
        self.window = builder.get_object("window")
        builder.connect_signals(self)       
    
if __name__ == "__main__":
    editor = TutorialTextEditor()
    editor.window.show()
    gtk.main()
