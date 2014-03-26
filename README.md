media-import
============

Anki add-on for importing media files as new notes.

---
[Link to add-on](https://ankiweb.net/shared/info/1531997860)

When the add-on is installed, a `Media Import...` option will be added to the `Tools` menu.

![Menu](https://raw.githubusercontent.com/hssm/media-import/master/docs/menu.png)

This option will ask for a directory to scan, and any image or audio file it finds will be added as a new note.


![Complete](https://raw.githubusercontent.com/hssm/media-import/master/docs/complete.png)

New notes created will use the `Basic` note type which has a `Front` and `Back` field. This add-on will use the file name before the extension as the `Front` field and the media file itself as the `Back` field. E.g., *apple.jpg* will have "apple" on the front and the image on the back.

![Card](https://raw.githubusercontent.com/hssm/media-import/master/docs/card.png)


All new notes are added to a deck named `MediaImport`. This deck is created for you automatically if it doesn't exist.
