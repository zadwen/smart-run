"""
Yes/no confirmation before we run anything. Uses a GTK dialog when there's
a display available, falls back to a plain terminal prompt otherwise.
"""


def confirm(message, detail=""):
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        if not Gtk.init_check()[0]:
            raise RuntimeError("No graphical display available")

        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=message,
        )
        if detail:
            dialog.format_secondary_text(detail)
        dialog.set_title("Smart Run")
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.YES
    except Exception:
        prompt = f"{message} {detail} [y/N]: "
        try:
            return input(prompt).strip().lower() in ("y", "yes")
        except (EOFError, KeyboardInterrupt):
            return False


def notify(message):
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        if not Gtk.init_check()[0]:
            raise RuntimeError("No graphical display available")

        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.set_title("Smart Run")
        dialog.run()
        dialog.destroy()
    except Exception:
        print(message)


def choose_file():
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
        if not Gtk.init_check()[0]:
            raise RuntimeError("No graphical display available")
        picker = Gtk.FileChooserDialog(title="Smart Run — Choose a program or installer", action=Gtk.FileChooserAction.OPEN)
        picker.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Choose file", Gtk.ResponseType.OK)
        result = picker.run()
        path = picker.get_filename() if result == Gtk.ResponseType.OK else None
        picker.destroy()
        return path
    except (ImportError, ValueError, RuntimeError):
        notify("To use Smart Run in a terminal, type: smart-run /path/to/file")
        return None


def choose_candidate(paths):
    if len(paths) == 1:
        return paths[0]
    # Avoid guessing which of several installers the user intended.
    notify("Several possible programs were found. The extracted folder will open. Right-click the program you want and choose Smart Run.")
    return None
