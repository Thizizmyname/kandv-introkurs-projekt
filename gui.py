import gtk
import tCards
import tSelection


class SelectionCards():

    def __init__(self):
        self.selection = tSelection.getSelection()

        cards = self.selection.h | self.selection.m | self.selection.v
        self.cardnames = [card[tCards.INDEX_NAME] for card in cards]

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Selection')

        self.scrolledWindow = gtk.ScrolledWindow()
        self.box = gtk.VBox()
        
        for name in self.cardnames:
            item = gtk.Label(name)
            self.box.pack_start(item)
            
            item.show()

        self.scrolledWindow.add(self.box)
        self.window.add(self.scrolledWindow)

        self.box.show()
        self.scrolledWindow.show()
        self.window.show()


def main():
    gtk.main()

if __name__ == "__main__":
    selectionCards = SelectionCards()
    main()
