import gtk
import gtk.glade
import tCards
import tSelection


class ThunderstoneRandomizerGTK():

    def __init__(self):

        monsters = tCards.MONSTERS
        heroes = tCards.HEROES
        villagers = tCards.VILLAGERS

        gladefile = 'gui.glade'
        self.glade = gtk.Builder()
        self.glade.add_from_file(gladefile)
        self.glade.connect_signals(self)

        self.window = self.glade.get_object('MainWindow')

        self.monsterListStore = gtk.ListStore(str, bool, bool, bool)

        for monster in monsters:
            name = monster[tCards.INDEX_NAME]
            row = [name, True, False, False]
            self.monsterListStore.append(row)

        self.monsterTreeView = gtk.TreeView(model=self.monsterListStore)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn('Name', renderer_text, text=0)

        renderer_toggle_normal = gtk.CellRendererToggle()
        renderer_toggle_normal.set_radio(True)
        column_normal = gtk.TreeViewColumn('Normal', renderer_toggle_normal, active=1)

        renderer_toggle_forced = gtk.CellRendererToggle()
        renderer_toggle_forced.set_radio(True)
        column_forced = gtk.TreeViewColumn('Forced', renderer_toggle_forced, active=2)

        renderer_toggle_banned = gtk.CellRendererToggle()
        renderer_toggle_banned.set_radio(True)
        column_banned = gtk.TreeViewColumn('Banned', renderer_toggle_banned, active=3)

        self.monsterTreeView.append_column(column_text)
        self.monsterTreeView.append_column(column_normal)
        self.monsterTreeView.append_column(column_forced)
        self.monsterTreeView.append_column(column_banned)

        self.selectionNotebook = self.glade.get_object('selectionNotebook')
        self.selectionNotebook.append_page(
                self.monsterTreeView, gtk.Label('Monster Cards'))

        self.window.show_all()

    def on_MainWindow_destroy(self, *args):
        gtk.main_quit(*args)


def main():
    gtk.main()

if __name__ == "__main__":
    selectionCards = ThunderstoneRandomizerGTK()
    main()
