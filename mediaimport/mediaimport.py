# -*- coding: utf-8 -*-
# Version: 2.2
#
# This is an Anki add-on for creating notes by importing media files from a
# user-selected directory. The user is able to map properties of the imported
# file to fields in a note type. For example, a user can map the media file
# to the 'Front' field and the file name to the 'Back' field and generate new
# cards from a folder of media files following this pattern.
#
# See github page to report issues or to contribute:
# https://github.com/hssm/media-import

from aqt import mw
from aqt.qt import *
from aqt import editor
from anki import notes

import dialog

# Support the same media types as the Editor
AUDIO = editor.audio
IMAGE = editor.pics
# Possible field mappings
ACTIONS = ['',
           'Media',
           'File Name',
           'File Name (full)',
           'Extension',
           'Sequence']

def doMediaImport():
    # Raise the main dialog for the add-on and retrieve its result when closed.
    (path, model, fieldMap, ok) = ImportSettingsDialog().getDialogResult()
    if not ok:
        return
    # Get the MediaImport deck id (auto-created if it doesn't exist)
    did = mw.col.decks.id('MediaImport')
    # Passing in a unicode path to os.walk gives us unicode results.
    # We won't walk the path - we only want the top-level files.
    (root, dirs, files) = os.walk(unicode(path)).next()
    mw.progress.start(max=len(files), parent=mw, immediate=True)
    newCount = 0
    failure = False
    for i, fileName in enumerate(files):
        note = notes.Note(mw.col, model)
        note.model()['did'] = did
        mediaName, ext = os.path.splitext(fileName)
        ext = ext[1:].lower()
        path = os.path.join(root, fileName)
        if ext is None or ext not in AUDIO+IMAGE:
            # Skip files with no extension and non-media files
            continue
        # Add the file to the media collection and get its name
        fname = mw.col.media.addFile(path)
        # Now we populate each field according to the mapping selected
        for field, idx in fieldMap.iteritems():
            action = ACTIONS[idx]
            if action == '':
                continue
            elif action == "Media":
                if ext in AUDIO:
                     note[field] = u'[sound:%s]' % fname
                elif ext in IMAGE:
                     note[field] = u'<img src="%s">' % fname
            elif action == "File Name":
                note[field] = mediaName
            elif action == "File Name (full)":
                note[field] = fileName
            elif action == "Extension":
                note[field] = ext
            elif action == "Sequence":
                note[field] = str(i)

        if not mw.col.addNote(note):
            # No cards were generated - probably bad template. No point
            # trying to import anymore.
            failure = True
            break
        newCount += 1
        mw.progress.update(value=i)
    mw.progress.finish()
    mw.deckBrowser.refresh()
    if failure:
        showFailureDialog()
    else:
        showCompletionDialog(newCount)


class ImportSettingsDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, mw)
        self.form = dialog.Ui_Form()
        self.form.setupUi(self)
        self.form.buttonBox.accepted.connect(self.accept)
        self.form.buttonBox.rejected.connect(self.reject)
        self.form.browse.clicked.connect(self.onBrowse)
        # The path to the media directory chosen by user
        self.mediaDir = None
        # The number of fields in the note type we are using
        self.fieldCount = 0
        self.populateModelList()
        self.exec_()

    def populateModelList(self):
        """Fill in the list of available note types to select from."""
        models = mw.col.models.all()
        for m in models:
            item = QListWidgetItem(m['name'])
            # Put the model in the widget to conveniently fetch later
            item.model = m
            self.form.modelList.addItem(item)
        self.form.modelList.sortItems()
        self.form.modelList.connect(self.form.modelList,
                               SIGNAL("currentRowChanged(int)"),
                               self.populateFieldGrid)
        # Triggers a selection so the fields will be populated
        self.form.modelList.setCurrentRow(0)

    def populateFieldGrid(self):
        """Fill in the fieldMapGrid QGridLayout.

        Each row in the grid contains two columns:
        Column 0 = QLabel with name of field
        Column 1 = QComboBox with selection of mappings ("actions")
        The first two fields will default to Media and File Name, so we have
        special cases for rows 0 and 1. The final row is a spacer."""

        self.clearLayout(self.form.fieldMapGrid)
        for row, field in enumerate(self.form.modelList.currentItem().model['flds']):
            cmb = QComboBox()
            cmb.addItems(ACTIONS)
            self.form.fieldMapGrid.addWidget(QLabel(field['name']), row, 0)
            self.form.fieldMapGrid.addWidget(cmb, row, 1)
            if row == 0: cmb.setCurrentIndex(1) # TODO: don't hard-code index?
            if row == 1: cmb.setCurrentIndex(2)
        row += 1
        self.fieldCount = row
        self.form.fieldMapGrid.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding),
            row, 0)

    def getDialogResult(self):
        """Return a tuple containing the user-defined settings to follow
        for an import. The tuple contains four items (in order):
         - Path to chosen media directory
         - The model (note type) to use for new notes
         - A dictionary that maps each of the fields in the model to an
           integer index from the ACTIONS list
         - True/False indicating whether the user clicked OK/Cancel"""

        if self.result() == QDialog.Rejected:
            return (None, None, None, False)

        model = self.form.modelList.currentItem().model
        # Iterate the grid rows to populate the field map
        fieldMap = {}
        grid = self.form.fieldMapGrid
        for row in range(self.fieldCount):
            # QLabel with field name
            field = grid.itemAtPosition(row, 0).widget().text()
            # QComboBox with index from the action list
            action = grid.itemAtPosition(row, 1).widget().currentIndex()
            fieldMap[field] = action

        return (self.mediaDir, model, fieldMap, True)

    def onBrowse(self):
        """Show the directory selection dialog."""
        path = unicode(
            QFileDialog.getExistingDirectory(mw, "Import Directory"))
        if not path:
            return
        self.mediaDir = path
        self.form.mediaDir.setText(self.mediaDir)
        self.form.mediaDir.setStyleSheet("")

    def accept(self):
        # Show a red warning box if the user tries to import without selecting
        # a directory.
        if not self.mediaDir:
            self.form.mediaDir.setStyleSheet("border: 1px solid red")
            return
        QDialog.accept(self)

    def clearLayout(self, layout):
        """Convenience method to remove child widgets from a layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())


def showCompletionDialog(newCount):
    QMessageBox.about(mw, "Media Import Complete",
"""
<p>
Media import is complete and %s new notes were created. 
All generated cards are placed in the <b>MediaImport</b> deck.
<br><br>
Please refer to the introductory videos for instructions on 
<a href="https://youtube.com/watch?v=DnbKwHEQ1mA">flipping card content</a> or 
<a href="http://youtube.com/watch?v=F1j1Zx0mXME">modifying the appearance of cards.</a>
</p>""" % newCount)

def showFailureDialog():
    QMessageBox.about(mw, "Media Import Failure",
"""
<p>
Failed to generate cards and no media files were imported. Please ensure the
note type you selected is able to generate cards by using a valid
<a href="http://ankisrs.net/docs/manual.html#cards-and-templates">card template</a>.
</p>
""")

action = QAction("Media Import...", mw)
mw.connect(action, SIGNAL("triggered()"), doMediaImport)
mw.form.menuTools.addAction(action)

