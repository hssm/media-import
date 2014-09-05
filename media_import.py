# -*- coding: utf-8 -*-
# Version: 1.3
#
# This is an Anki add-on for creating notes/cards by importing media
# files from a user-selected directory. The file name (without the
# extension) will be used as the expression, and the media file itself
# will be used as the answer part.
#
# See github page to report issues or to contribute:
# https://github.com/hssm/media-import

import os
from os import listdir
from os.path import isfile, join

from aqt import mw
from aqt.qt import *
from aqt import editor
from anki import notes
from anki import stdmodels

# Support the same media types as the Editor
AUDIO = editor.audio
IMAGE = editor.pics

def getMediaModel():
    """Return a note type (model) suitable for this add-on.
    
    The note type is called 'Basic' and contains two fields:
    Front and Back. The note type will be created if it doesn't
    already exist."""
    
    m = mw.col.models
    model = m.byName('Basic')
    if (model and len(model['flds']) == 2
        and 'Front' in m.fieldNames(model)
        and 'Back' in m.fieldNames(model)):
        return model
    else:
        model = stdmodels.addBasicModel(mw.col)
        m.save(model)
        return model


def doMediaImport():
    dir = str(QFileDialog.getExistingDirectory(mw, "Import Directory"))
    if not dir:
        return
    # Get the MediaImport deck id (auto-created if it doesn't exist)
    did = mw.col.decks.id('MediaImport')
    # Get the note type to use for the new notes
    model = getMediaModel()
    # Passing in a unicode path to os.walk gives us unicode results.
    # We won't walk the path - we only want the top-level files.
    (root, dirs, files) = os.walk(unicode(dir)).next()
    mw.progress.start(max=len(files), parent=mw, immediate=True)
    newCount = 0
    failure = False
    for i, file in enumerate(files):
        note = notes.Note(mw.col, model)
        note.model()['did'] = did
        exp, ext = os.path.splitext(file)
        ext = ext[1:].lower()
        path = os.path.join(root, file)
        if not ext:
            # Skip files with no extension
            continue
        elif ext in AUDIO:
            fname = mw.col.media.addFile(path)
            note['Back'] = u'[sound:%s]' % fname
        elif ext in IMAGE:
            fname = mw.col.media.addFile(path)
            note['Back'] = u'<img src="%s">' % fname
        else:
            # Skip non-media files
            continue
        note['Front'] = exp
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
Failed to generate cards and no media files were imported. Please ensure
your <b>Basic</b> note type is able to generate cards by using a valid
<a href="http://ankisrs.net/docs/manual.html#cards-and-templates">card template</a>.
</p>
""")

action = QAction("Media Import...", mw)
mw.connect(action, SIGNAL("triggered()"), doMediaImport)
mw.form.menuTools.addAction(action)