media-import
============

Anki add-on for importing media files as new notes.

[Link to add-on](https://ankiweb.net/shared/info/1531997860)

---

This add-on will allow you to import media files into your Anki collection and use their file names as a component of the note. You can create cards that might look like this (using *apple.jpg*):

![Card](https://raw.githubusercontent.com/hssm/media-import/master/docs/card.png)

When the add-on is installed, a `Media Import...` option will be added to the `Tools` menu.

![Menu](https://raw.githubusercontent.com/hssm/media-import/master/docs/menu.png)

Selecting this menu item will open the Media Import window.

![Dialog](https://raw.githubusercontent.com/hssm/media-import/master/docs/dialog.png)

From this window, you are able to:
- Browse and select which folder to use as the source of media files
- Choose which note type to use for the imported notes
- Decide what content to put into each of the fields
 
Here is a list of the content available to insert into fields. We will use an example file named `apple.jpg`.
 - Media - The media file itself (image or audio will appear on the card)
 - File Name - The name of the file without the extension (*apple*)
 - File Name (full) - The name of the file including the extention (*apple.jpg*)
 - Extension - Only the extension of the file (*jpg*)
 - Sequence - A number indicating the order in which the file was imported. If 15 files were imported, each file will contain a value starting from 0 to 14.




All new generated cards are added to a deck named `MediaImport`. This deck is created for you automatically if it doesn't exist.

![Complete](https://raw.githubusercontent.com/hssm/media-import/master/docs/complete.png)
