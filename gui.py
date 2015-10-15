import gtk
import gtk.glade
import tCards
import tSelection


class ThunderstoneRandomizerGTK():

    def __init__(self):

        # Get monster sets
        monsters = tCards.MONSTERS
        heroes = tCards.HEROES
        villagers = tCards.VILLAGERS

        # Load glade layout
        gladefile = 'gui.glade'
        self.glade = gtk.Builder()
        self.glade.add_from_file(gladefile)
        self.glade.connect_signals(self)

        # Our root window
        self.window = self.glade.get_object('MainWindow')

        # The notebook of card classes
        self.selectionNotebook = self.glade.get_object('selectionNotebook')

        self.selectionWindow = self.glade.get_object('selectionWindow')

        self.monsterScrollableWindow = gtk.ScrolledWindow()
        self.monsterScrollableWindow.set_policy (gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.heroScrollableWindow = gtk.ScrolledWindow()
        self.heroScrollableWindow.set_policy (gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.villageScrollableWindow = gtk.ScrolledWindow()
        self.villageScrollableWindow.set_policy (gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.monsterListStore = self.cardListStore(monsters)
        self.heroListStore = self.cardListStore(heroes)
        self.villageListStore = self.cardListStore(villagers)
        self.selectionListStore = gtk.ListStore(str, bool)

        self.monsterTreeView = self.cardTreeView(self.monsterListStore)
        self.heroTreeView = self.cardTreeView(self.heroListStore)
        self.villageTreeView = self.cardTreeView(self.villageListStore)
        self.selectionTreeView = self.makeSelectionTreeView(self.selectionListStore)
        
        self.monsterScrollableWindow.add(self.monsterTreeView)
        self.heroScrollableWindow.add(self.heroTreeView)
        self.villageScrollableWindow.add(self.villageTreeView)

        self.selectionNotebook.append_page(
            self.monsterScrollableWindow, gtk.Label('Monster Cards'))
        self.selectionNotebook.append_page(
            self.heroScrollableWindow, gtk.Label('Hero Cards'))
        self.selectionNotebook.append_page(
            self.villageScrollableWindow, gtk.Label('Village Cards'))

        self.selectionWindow.add(self.selectionTreeView)

        # Show the application
        self.window.show_all()

        """reshuffleBar = self.glade.get_object('hbox2')

        # Insert selection tree
        self.selectionVBox.remove(reshuffleBar)
        self.selectionVBox.pack_end(self.selectionTreeView)
        self.selectionVBox.pack_end(reshuffleBar)"""


    def _cardListStore(self, cards):
        """
        Creates and returns a listStore containing the card names and three bools
        """

        listStore = gtk.ListStore(str, bool, bool, bool)

        for card in cards:
            name = card[tCards.INDEX_NAME]
            row = [name, True, False, False]
            listStore.append(row)

        return listStore

    def _makeSelectionTreeView(self, listStore):
        """
        Creates and returns a TreeStore with one name column and one checkbox column.
        """

        treeView = gtk.TreeView(model=listStore)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn('Name', renderer_text, text=0)
        column_text.set_expand(True)

        renderer_toggle_reshuffle = gtk.CellRendererToggle()
        renderer_toggle_reshuffle.connect(
            'toggled', self.on_reshuffle_toggle, listStore)

        column_reshuffle = gtk.TreeViewColumn(
            'Reshuffle', renderer_toggle_reshuffle, active=1)

        treeView.append_column(column_text)
        treeView.append_column(column_reshuffle)

        return treeView

    def _cardTreeView(self, listStore):
        """
        Creates and returns a treeView with a name column and three radio buttons.
        """

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

    def _updateListStore(self, listStore, selection):
        listStore.clear()

        for card in selection.m | selection.h | selection.v:
            name = card[tCards.INDEX_NAME]
            listStore.append([name,  False])

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

    def on_randomize(self, widget, data=None):
        selection = tSelection.getSelection()
        self._updateListStore(self.selectionListStore, selection)

    def on_reshuffle_toggle(self, widget, path, listStore):
        listStore[path][1] = not listStore[path][1]

    def on_reshuffleButton_clicked(self, widget, data=None):
        pass


def main():
    gtk.main()

if __name__ == "__main__":
    selectionCards = ThunderstoneRandomizerGTK()
    main()
