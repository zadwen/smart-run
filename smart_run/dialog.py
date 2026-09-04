"""
Yes/no confirmation before we run anything. Uses a GTK dialog when there's
a display available, falls back to a plain terminal prompt otherwise.
"""


def confirm(message, detail=""):
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

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
        return input(prompt).strip().lower() == "y"


def notify(message):
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

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
