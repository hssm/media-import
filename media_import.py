# -*- coding: utf-8 -*-
# This is an Anki add-on for creating notes/cards by importing media
# files from a user-selected directory. The file name (without the
# extension) will be used as the expression, and the media file itself
# will be used as the answer part.

from os import listdir
from os.path import isfile, join

from aqt import mw
from aqt.qt import *
from aqt import editor
from anki import notes

# Support the same media types as the Editor
AUDIO = editor.audio
IMAGE = editor.pics


def doMediaImport():
    dir = str(QFileDialog.getExistingDirectory(mw, "Import Directory"))
    if not dir:
        return
    # Get the MediaImport deck id (auto-created if it doesn't exist)
    did = mw.col.decks.id('MediaImport')
    model = mw.col.models.byName('Basic')
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    mw.progress.start(max=len(files), parent=mw, immediate=True)
    newCount = 0
    for i, file in enumerate(files):
        note = notes.Note(mw.col, model)
        note.model()['did'] = did
        exp, ext = os.path.splitext(file)
        # Skip files with no extension
        if not ext:
            continue
        note['Front'] = unicode(exp)
        path = unicode(os.path.join(dir, file))
        ext = ext[1:].lower()
        if ext in AUDIO:
            fname = mw.col.media.addFile(path)
            note['Back'] = u'[sound:%s]' % fname
            newCount += 1
        elif ext in IMAGE:
            fname = mw.col.media.addFile(path)
            note['Back'] = u'<img src="%s">' % fname
            newCount += 1
        else:
            continue
        mw.progress.update(value=i)
        mw.col.addNote(note)
    mw.progress.finish()
    mw.deckBrowser.refresh()
    showCompletionDialog(newCount)

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



action = QAction("Media Import...", mw)
mw.connect(action, SIGNAL("triggered()"), doMediaImport)
mw.form.menuTools.addAction(action)