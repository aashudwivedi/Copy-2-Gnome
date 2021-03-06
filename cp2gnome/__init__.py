import pygtk
pygtk.require('2.0')
import rb, gtk, rhythmdb

ui_str = \
"""<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsMenuModePlaceholder">
        <menuitem name="ToolsMenucp2gnome" action="cp2gnome"/>
      </placeholder>
    </menu>
  </menubar>
  <toolbar name="ToolBar">
    <placeholder name="ToolBarPluginPlaceholder">
      <toolitem name="cp2gnome" action="cp2gnome"/>
    </placeholder>
  </toolbar>
</ui>"""

class cp2gnome(rb.Plugin):
    def activate(self, shell):
        self.targets = [('x-special/gnome-copied-files',0,0), ("text/uri-list",0,0)] 
        icon_file_name = "./icon.png"
        iconsource = gtk.IconSource()
        iconsource.set_filename(icon_file_name)
        iconset = gtk.IconSet()
        iconset.add_source(iconsource)
        iconfactory = gtk.IconFactory()
        iconfactory.add("cp2gnome-button", iconset)
        iconfactory.add_default()

        action = gtk.Action("cp2gnome", "cp2gnome",
                            "copy the current selection to gnome clipboard",
                            "cp2gnome-button");
        action_group = gtk.ActionGroup('hot_key_action_group')
        action_group = action_group.add_action_with_accel(action,'<control><shift>C')

        action.connect("activate", self.copy_to_clipboard, shell)
        
        self.action_group = gtk.ActionGroup('cp2gnomeActionGroup')
        self.action_group.add_action(action)
        manager = shell.get_ui_manager()
        manager.insert_action_group(self.action_group, 0)
        self.UI_ID = manager.add_ui_from_string(ui_str)
        manager.ensure_update()

    def deactivate(self, shell):
        manager = shell.get_ui_manager()
        manager.remove_ui(self.UI_ID)
        manager.remove_action_group(self.action_group)
        manager.ensure_update()
    
    def get_selected_paths(self,shell):
        #source = shell.get_property("selected-source")
        source = shell.props.selected_page
        entry = rb.Source.get_entry_view(source)
        selected = entry.get_selected_entries()
        path_list = [] 
        for item in selected:
            path_list.append(item.get_playback_uri())
        return path_list
        
    def copy_to_clipboard(self, event, shell): 
        clipboard = gtk.clipboard_get()
        path_list = self.get_selected_paths(shell)
        print path_list
        clipboard.set_with_data(self.targets, get_func, clear_func,path_list)
 
def get_func(clipboard,selectiondata,info,path_list):
    print type(path_list)
    txt = 'copy\n'+'\n'.join(path_list)
    selectiondata.set(selectiondata.get_target(),8,txt)
    
def clear_func(clipboard,data):
    pass
        
