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

        self.selectionNotebook = self.glade.get_object('selectionNotebook')

        self.monsterListStore = self.cardListStore(monsters)
        self.heroListStore = self.cardListStore(heroes)
        self.villageListStore = self.cardListStore(villagers)

        self.monsterTreeView = self.cardTreeView(self.monsterListStore)
        self.heroTreeView = self.cardTreeView(self.heroListStore)
        self.villageTreeView = self.cardTreeView(self.villageListStore)

        self.selectionNotebook.append_page(
            self.monsterTreeView, gtk.Label('Monster Cards'))
        self.selectionNotebook.append_page(
            self.heroTreeView, gtk.Label('Hero Cards'))
        self.selectionNotebook.append_page(
            self.villageTreeView, gtk.Label('Village Cards'))

        self.window.show_all()

    def cardListStore(self, cards):
        listStore = gtk.ListStore(str, bool, bool, bool)

        for card in cards:
            name = card[tCards.INDEX_NAME]
            row = [name, True, False, False]
            listStore.append(row)

        return listStore

    def cardTreeView(self, listStore):
        treeView = gtk.TreeView(model=listStore)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn('Name', renderer_text, text=0)
        column_text.set_expand(True)

        renderer_toggle_normal = gtk.CellRendererToggle()
        renderer_toggle_normal.set_radio(True)
        renderer_toggle_normal.connect(
            'toggled', self.on_normal_toggle, listStore)

        column_normal = gtk.TreeViewColumn(
            'Normal', renderer_toggle_normal, active=1)

        renderer_toggle_forced = gtk.CellRendererToggle()
        renderer_toggle_forced.set_radio(True)
        renderer_toggle_forced.connect(
            'toggled', self.on_forced_toggle, listStore)

        column_forced = gtk.TreeViewColumn(
            'Forced', renderer_toggle_forced, active=2)

        renderer_toggle_banned = gtk.CellRendererToggle()
        renderer_toggle_banned.set_radio(True)
        renderer_toggle_banned.connect(
            'toggled', self.on_banned_toggle, listStore)

        column_banned = gtk.TreeViewColumn(
            'Banned', renderer_toggle_banned, active=3)

        treeView.append_column(column_text)
        treeView.append_column(column_normal)
        treeView.append_column(column_forced)
        treeView.append_column(column_banned)

        return treeView

    def on_MainWindow_destroy(self, *args):
        gtk.main_quit(*args)

    def on_normal_toggle(self, widget, path, listStore):
        listStore[path][1] = True
        listStore[path][2] = False
        listStore[path][3] = False

    def on_forced_toggle(self, widget, path, listStore):
        listStore[path][1] = False
        listStore[path][2] = True
        listStore[path][3] = False

    def on_banned_toggle(self, widget, path, listStore):
        listStore[path][1] = False
        listStore[path][2] = False
        listStore[path][3] = True


def main():
    gtk.main()

if __name__ == "__main__":
    selectionCards = ThunderstoneRandomizerGTK()
    main()
