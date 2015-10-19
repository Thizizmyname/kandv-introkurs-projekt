import gtk
import gtk.glade
import tCards
import tSelection
from tSelection import MonsterBannedException, \
                       HeroBannedException, \
                       VillageBannedException


class ThunderstoneRandomizerGTK():

    def __init__(self):

        # Get monster sets
        self.monsters = tCards.MONSTERS
        self.heroes = tCards.HEROES
        self.villagers = tCards.VILLAGERS

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
        self.monsterScrollableWindow.set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.heroScrollableWindow = gtk.ScrolledWindow()
        self.heroScrollableWindow.set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.villageScrollableWindow = gtk.ScrolledWindow()
        self.villageScrollableWindow.set_policy(
            gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.monsterListStore = self._cardListStore(self.monsters)
        self.heroListStore = self._cardListStore(self.heroes)
        self.villageListStore = self._cardListStore(self.villagers)

        self.monsterSelectionListStore = self._emptySelectionListStore()
        self.heroSelectionListStore = self._emptySelectionListStore()
        self.villageSelectionListStore = self._emptySelectionListStore()

        self.monsterTreeView = self._cardTreeView(self.monsterListStore)
        self.heroTreeView = self._cardTreeView(self.heroListStore)
        self.villageTreeView = self._cardTreeView(self.villageListStore)

        self.monsterSelectionTreeView = self._makeSelectionTreeView(
            self.monsterSelectionListStore, 'Monsters')
        self.heroSelectionTreeView = self._makeSelectionTreeView(
            self.heroSelectionListStore, 'Heroes')
        self.villageSelectionTreeView = self._makeSelectionTreeView(
            self.villageSelectionListStore, 'Villagers')

        self.monsterScrollableWindow.add(self.monsterTreeView)
        self.heroScrollableWindow.add(self.heroTreeView)
        self.villageScrollableWindow.add(self.villageTreeView)

        self.selectionNotebook.append_page(
            self.monsterScrollableWindow, gtk.Label('Monster Cards'))
        self.selectionNotebook.append_page(
            self.heroScrollableWindow, gtk.Label('Hero Cards'))
        self.selectionNotebook.append_page(
            self.villageScrollableWindow, gtk.Label('Village Cards'))

        self.selectionVBox = gtk.VBox()
        self.selectionVBox.pack_start(self.monsterSelectionTreeView)
        self.selectionVBox.pack_start(self.heroSelectionTreeView)
        self.selectionVBox.pack_start(self.villageSelectionTreeView)

        self.selectionWindow.add_with_viewport(self.selectionVBox)

        self.errorLabel = self.glade.get_object('errorLabel')

        self.validateCheckbox = self.glade.get_object('validateCheckbox')

        # Show the application
        self.window.show_all()

    def _cardListStore(self, cards):
        """
        Creates and returns a listStore containing the card names and
        three bools
        """

        listStore = gtk.ListStore(str, bool, bool, bool)

        for card in cards:
            name = card[tCards.INDEX_NAME]
            row = [name, True, False, False]
            listStore.append(row)

        listStore.set_sort_column_id(0, gtk.SORT_ASCENDING)
        return listStore

    def _emptySelectionListStore(self):
        listStore = gtk.ListStore(str, bool)
        listStore.set_sort_column_id(0, gtk.SORT_ASCENDING)

        return listStore

    def _makeSelectionTreeView(self, listStore, className):
        """
        Creates and returns a TreeStore with one name column
        and one checkbox column.
        """

        treeView = gtk.TreeView(model=listStore)

        renderer_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn(className, renderer_text, text=0)
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
        Creates and returns a treeView with a name column
        and three radio buttons.
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

    def _updateListStore(self, listStore, cardSet):
        listStore.clear()

        for card in cardSet:
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

    def _getCustomizationSelector(self, listStore):
        forced = []
        banned = []

        for row in listStore:
            if self._isForced(row):
                card = tCards.cardFromCardName(row[0])
                forced.append(card)
            if self._isBanned(row):
                card = tCards.cardFromCardName(row[0])
                banned.append(card)

        forced = set(forced)
        banned = set(banned)

        selector = tSelection.ClassSelector(forced, banned)
        return selector

    def on_randomize(self, widget, data=None):

        self.errorLabel.set_text('')

        monsterSelector = self._getCustomizationSelector(self.monsterListStore)
        heroSelector = self._getCustomizationSelector(self.heroListStore)
        villageSelector = self._getCustomizationSelector(self.villageListStore)

        try:

            self._updateSelectionListStores(
                monsterSelector, heroSelector, villageSelector)

        except (MonsterBannedException,
                HeroBannedException,
                VillageBannedException) as e:

            self.errorLabel.set_text(e.message)

    def _isForced(self, row):
        return row[2]

    def _isBanned(self, row):
        return row[3]

    def on_reshuffle_toggle(self, widget, path, listStore):
        listStore[path][1] = not listStore[path][1]

    def on_reshuffleButton_clicked(self, widget, data=None):

        monsterSelector = self._getReshuffleSelector(
            self.monsterSelectionListStore)
        heroSelector = self._getReshuffleSelector(self.heroSelectionListStore)
        villageSelector = self._getReshuffleSelector(
            self.villageSelectionListStore)

        self._updateSelectionListStores(
            monsterSelector, heroSelector, villageSelector)

    def _updateSelectionListStores(self,
                                   monsterSelector,
                                   heroSelector,
                                   villageSelector):

        selection = tSelection.getSelection(
            monster=monsterSelector,
            hero=heroSelector,
            village=villageSelector,
            validate=self.validateCheckbox.get_active())

        if not selection.validate():
            self.errorLabel.set_text(
                    'Selection dependencies could not be validated!' + '\n' +
                    'Please change your preferences and try again.')

        self._updateListStore(self.monsterSelectionListStore, selection.m)
        self._updateListStore(self.heroSelectionListStore, selection.h)
        self._updateListStore(self.villageSelectionListStore, selection.v)

    def _getReshuffleSelector(self, listStore):

        keep = []

        for row in listStore:
            if not self._reshuffle(row):
                card = tCards.cardFromCardName(row[0])
                keep.append(card)

        keep = set(keep)

        selector = tSelection.ClassSelector(keep, set())
        return selector

    def _reshuffle(self, row):
        return row[1]


def main():
    gtk.main()

if __name__ == "__main__":
    selectionCards = ThunderstoneRandomizerGTK()
    main()
