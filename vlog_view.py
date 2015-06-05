#!/usr/bin/python
from gi.repository import Gtk, GObject, Gdk, cairo, Pango
import re
import assets_vlog

class Rect():
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height =height
        self.width = width

class DialogNew(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 1,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(330, 100)
        self.set_border_width(10)

        label0 = Gtk.Label("New Show")
        label1 = Gtk.Label("Title:", xalign=0.9)
        label2 = Gtk.Label("Episodes:", xalign=0.9)
        label3 = Gtk.Label("Subtitle Adress:", xalign=0.9)
        label4 = Gtk.Label("Torrent Adress:", xalign=0.9)

        self.entry1 = Gtk.Entry()
        self.entry2 = Gtk.Entry()
        self.entry3 = Gtk.Entry()
        self.entry4 = Gtk.Entry()

        table = Gtk.Grid()
        table.set_row_spacing(5)
        table.set_column_spacing(5)
        table.set_margin_end(10)
        table.set_margin_bottom(10)

        table.attach(label0, 0,0,2,1)

        table.attach(label1, 0,1,1,1)
        table.attach(label2, 0,2,1,1)
        table.attach(label3, 0,3,1,1)
        table.attach(label4, 0,4,1,1)

        table.attach(self.entry1, 1,1,1,1)
        table.attach(self.entry2, 1,2,1,1)
        table.attach(self.entry3, 1,3,1,1)
        table.attach(self.entry4, 1,4,1,1)

        box = self.get_content_area()
        box.add(table)
        self.show_all()

class DialogEdit(Gtk.Dialog):
    def __init__(self, parent, selection):
        Gtk.Dialog.__init__(self, "My Dialog", parent, 1,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(330, 100)
        self.set_border_width(10)

        model,iter = selection.get_selected()
        if iter !=None:
            id = (model[iter][0])
            title =(model[iter][1]) 

        label0 = Gtk.Label(title)
        #pango1 = label0.get_attributes().change(
        labelexp = Gtk.Label('Formats: 3;1-3  S02-S04  S32  345  33;44')
        label1 = Gtk.Label("Episodes to Add:", xalign=0.9)
        label2 = Gtk.Label("Episodes to Delete:", xalign=0.9)
        label3 = Gtk.Label("Subtitle Adress:", xalign=0.9)
        label4 = Gtk.Label("Torrent Adress:", xalign=0.9)

        if iter !=None:
            tp = parent.medel.get_show_shallow(id)
        else:
            tp = '.'
        self.entry1 = Gtk.Entry()
        self.entry2 = Gtk.Entry()
        self.entry3 = Gtk.Entry()
        if tp[2] is not None:
            self.entry3.set_text(str(tp[2]))
            self.entry3.set_tooltip_text(str(tp[2]))
        self.entry4 = Gtk.Entry()
        if tp[3] is not None:
            self.entry4.set_text(str(tp[3]))
            self.entry4.set_tooltip_text(str(tp[3]))

        table = Gtk.Grid()
        table.set_row_spacing(5)
        table.set_column_spacing(5)
        table.set_margin_end(10)
        table.set_margin_bottom(10)

        table.attach(label0, 0,0,2,1)
        table.attach(labelexp, 0,1,2,1)

        table.attach(label1, 0,2,1,1)
        table.attach(label2, 0,3,1,1)
        table.attach(label3, 0,4,1,1)
        table.attach(label4, 0,5,1,1)

        table.attach(self.entry1, 1,2,1,1)
        table.attach(self.entry2, 1,3,1,1)
        table.attach(self.entry3, 1,4,1,1)
        table.attach(self.entry4, 1,5,1,1)

        box = self.get_content_area()
        box.add(table)
        self.show_all()

def pop_window(label_text):
    window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
    window.set_default_size(400,300)
    box = Gtk.Box.new(1,0)
    label = Gtk.Label()
    label.set_markup(label_text)
    label.set_property('justify', Gtk.Justification.LEFT)
    label.set_line_wrap(True)
    label.set_line_wrap_mode(Pango.WrapMode.WORD)
    label.set_alignment(0.2,0.1)
    label.set_selectable(True)
    box.pack_start(label, True, True, 0)
    button = Gtk.Button('DONE')
    button.connect('clicked',handler_pop_window_close, window)
    box.pack_start(button, False, False, 0)
    scroll = Gtk.ScrolledWindow()
    scroll.add(box)
    window.add(scroll)
    window.show_all()

def handler_pop_window_close(widget, window):
    window.destroy()

class VlogView(Gtk.Window):

    __gsignals__ = {
        'new-entry': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,)),
        'delete-show': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,)),
        'season-done': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,)),
        'fill-all': (GObject.SIGNAL_RUN_FIRST, None,
                      (int,)),
        'add-one': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,)),
        'zoom': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,)),
        'torrent': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,)),
        'subtitle': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,)),
        'details': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,str,)),
        'update-show': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,object,)),
        'search-show': (GObject.SIGNAL_RUN_FIRST, None,
                      (str,)),
        'undotrans': (GObject.SIGNAL_RUN_FIRST, None,
                      ()),
        'reload': (GObject.SIGNAL_RUN_FIRST, None,
                      (int,)),
        'tag': (GObject.SIGNAL_RUN_FIRST, None,
                      (object,object,int,)),
    }

    def __init__(self, model):
        Gtk.Window.__init__(self, title="Vlog")
        #model.connect('error', self.dialog_msg_cb)
        self.set_border_width(0)
	self.set_default_size(400,600)
        self.connect("delete-event", Gtk.main_quit)
        #self.__signals__['new_signal'] = (GObject.SIGNAL_RUN_FIRST, None, (int,))

        self.pixm = {} 
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        #print path

        #model.connect("db-error", self.dialog_msg_cb)



#                       ListStore , Treeview , Scrollable
#####################################################################
        #self.liststore = liststore

        #self.fill_store(model)
        self.medel = model
        #self.refresh_store()
        #self.current_filter_language = None

        #self.log_filter = self.liststore.filter_new()
        #self.log_filter.set_visible_func(self.filter_func)
        #self.filter_on = None



        treeview = Gtk.TreeView()
        self.treeview = treeview
        #treeview = Gtk.TreeView.new_with_model(self.log_filter)

        #renderer2 = Gtk.CellRendererText()
        renderer = Gtk.CellRendererText()
        renderer.set_property('ellipsize',3)
        renderer.set_property('ellipsize-set',True)
        renderer.set_property('weight',600)
        column = Gtk.TreeViewColumn('Title')
        column.pack_start(renderer, True)
        #column.pack_end(renderer2, False)
        column.add_attribute(renderer, "text", 1)
        column.add_attribute(renderer, "cell-background-rgba", 6)
        #column.add_attribute(renderer2, "text", 0)
        column.set_sort_column_id(1)
        column.set_sort_indicator(True)
        column.set_expand(True)
        #column.set_max_width(10)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_alignment(0.5,0.5)
        column = Gtk.TreeViewColumn('Last')
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "text", 2)
        column.add_attribute(renderer, "cell-background-rgba", 6)
        column.set_sort_column_id(2)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_alignment(0.5,0.5)
        column = Gtk.TreeViewColumn('Date')
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "text", 3)
        column.add_attribute(renderer, "cell-background-rgba", 6)
        column.set_sort_column_id(3)
        treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        renderer.set_alignment(0.5,0.5)
        column = Gtk.TreeViewColumn('Passed')
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "text", 4)
        column.add_attribute(renderer, "cell-background-rgba", 6)
        column.set_sort_column_id(4)
        treeview.append_column(column)

        renderer = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Ico")
        column.pack_start(renderer, False)
        column.add_attribute(renderer, "pixbuf", 5)
        column.add_attribute(renderer, "cell-background-rgba", 6)
        column.set_sort_column_id(4)
        treeview.append_column(column)


        popbox = Gtk.Box.new(1,0)
        c1 = Gtk.CheckButton.new_with_label("ss")
        c2 = Gtk.CheckButton.new_with_label("dd")
        c3 = Gtk.CheckButton.new_with_label("dd")
        popbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        popbox.pack_start(c1, False, False, 0)
        popbox.pack_start(c2, False, False, 0)
        popbox.pack_start(c3, False, False, 0)

        self.pop2 = Gtk.Popover.new(treeview)
        self.pop2.set_modal(True)
        self.pop2.add(popbox)
        self.pop2.set_border_width(6)
        #self.pop2.set_position(1)
        #self.pop2.connect("closed", self.handler_pop_closed)
        popbox.show_all()


#                           HeaderBar
#####################################################################
	header = Gtk.HeaderBar()
	header.set_subtitle(self.get_title())
	header.set_show_close_button(True)
	pixm = assets_vlog.Assets().get_pix()

        box = Gtk.Box(0,0)
        box.get_style_context().add_class("linked")

        button = Gtk.Button()
        img = Gtk.Image.new_from_pixbuf(pixm['undo'])
        #img = Gtk.Image.new_from_stock(Gtk.STOCK_REDO, 4)
        button.set_image(img)
        button.connect("clicked", self.handler_undo)
        box.add(button)

        button = Gtk.Button()
        #img = Gtk.Image.new_from_stock(Gtk.STOCK_NEW, 4)
        img = Gtk.Image.new_from_pixbuf(pixm['wood'])
        #img2 = Gtk.Image()
        #img2.set_from_icon_name("document-new", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect("clicked", self.handler_dialog_new)
        box.add(button)
	header.pack_start(box)

        box = Gtk.Box(0,0)
        box.get_style_context().add_class("linked")

        button = Gtk.Button()
        #img = Gtk.Image.new_from_stock(Gtk.STOCK_EDIT, 4)
        img = Gtk.Image.new_from_pixbuf(pixm['modify'])
        button.set_image(img)
        button.connect("clicked", self.handler_dialog_edit, self.treeview.get_selection())
        box.add(button)

        button = Gtk.ToggleButton()
        #img = Gtk.Image.new_from_stock(Gtk.STOCK_FIND, 4)
        img = Gtk.Image.new_from_pixbuf(pixm['find'])
        button.set_image(img)
        button.connect("clicked", self.handler_up)
        ##self
        searchbutton = button
        box.add(button)

        button = Gtk.ToggleButton()
        #button.set_stock_id(Gtk.STOCK_OK)
        #button = Gtk.Button()
        #img = Gtk.Image.new_from_stock(Gtk.STOCK_ADD, 4)
        img2 = Gtk.Image()
        img2.set_from_icon_name("open-menu-symbolic", Gtk.IconSize.MENU)
        #img = Gtk.Image.new_from_pixbuf(pixm['add'])
        button.set_image(img2)
        box.add(button)

        popbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

        radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "All")
        radio1.connect('toggled', self.handler_radio_changed, 1)
        popbox.pack_start(radio1, False, False, 0)
        radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Active")
        radio2.connect('toggled', self.handler_radio_changed, 2)
        radio2.set_active(True)
        popbox.pack_start(radio2, False, False, 0)
        radio3 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Completed")
        radio3.connect('toggled', self.handler_radio_changed, 3)
        popbox.pack_start(radio3, False, False, 0)
        radio4 = Gtk.RadioButton.new_with_label_from_widget(radio1, "To Watch")
        radio4.connect('toggled', self.handler_radio_changed, 4)
        popbox.pack_start(radio4, False, False, 0)

        #radio_list = [radio1, radio2, radio3, radio4]
        #radio1.connect('group-changed', self.handler_radio_changed, radio_list)

        #c1 = Gtk.CheckButton.new_with_label("ss")
        #c2 = Gtk.CheckButton.new_with_label("dd")
        #c3 = Gtk.CheckButton.new_with_label("dd")
        #popbox.pack_start(c1, False, False, 0)
        #popbox.pack_start(c2, False, False, 0)
        #popbox.pack_start(c3, False, False, 0)

        self.pop = Gtk.Popover.new(button)
        self.pop.set_modal(True)
        self.pop.add(popbox)
        self.pop.set_border_width(6)
        self.pop.connect("closed", self.handler_pop_closed, button)
        popbox.show_all()
        button.connect("toggled", self.handler_toggle_options, self.pop)




	header.pack_end(box)

#                           Popup  Menu
#####################################################################
        menu = Gtk.Menu()
        item = Gtk.ImageMenuItem.new_with_label("Add One")
        img = Gtk.Image.new_from_pixbuf(pixm['add2'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("activate",self.handler_add_one, self.treeview.get_selection())
        menu.append(item)

        item = Gtk.SeparatorMenuItem()
        menu.append(item)
        item = Gtk.ImageMenuItem.new_with_label("Goto Subtitle")
        img = Gtk.Image.new_from_pixbuf(pixm['subtitle'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("activate",self.handler_go_subtitle, self.treeview.get_selection())
        #item.connect("activate", self.reload_cb)
        menu.append(item)
        item = Gtk.ImageMenuItem.new_with_label("Goto Torrent")
        img = Gtk.Image.new_from_pixbuf(pixm['torrent'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("activate",self.handler_go_torrent, self.treeview.get_selection())
        menu.append(item)

        item = Gtk.SeparatorMenuItem()
        menu.append(item)
        item = Gtk.MenuItem("Set Completed")
        item.connect("activate",self.handler_season_done, self.treeview.get_selection())
        menu.append(item)
        item = Gtk.MenuItem("Copy to Clipboard")
        item.connect("activate",self.handler_clipboard, self.treeview.get_selection())
        menu.append(item)
        
        submenu = Gtk.Menu()
        item = Gtk.ImageMenuItem.new_with_label("None")
        img = Gtk.Image.new_from_pixbuf(pixm['silver-tag'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("button-press-event",self.handler_set_tag, self.treeview.get_selection(), 0)
        submenu.append(item)
        item = Gtk.SeparatorMenuItem()
        submenu.append(item)
        item = Gtk.ImageMenuItem.new_with_label("Green")
        img = Gtk.Image.new_from_pixbuf(pixm['green-tag'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("button-press-event",self.handler_set_tag, self.treeview.get_selection(), 2)
        submenu.append(item)
        item = Gtk.ImageMenuItem.new_with_label("Blue")
        img = Gtk.Image.new_from_pixbuf(pixm['blue-tag'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("button-press-event",self.handler_set_tag, self.treeview.get_selection(), 4)
        submenu.append(item)
        item = Gtk.ImageMenuItem.new_with_label("Red")
        img = Gtk.Image.new_from_pixbuf(pixm['red-tag'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("button-press-event",self.handler_set_tag, self.treeview.get_selection(), 6)
        submenu.append(item)

        item = Gtk.ImageMenuItem.new_with_label("Set Tag")
        #item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_OK, None)
        img = Gtk.Image.new_from_pixbuf(pixm['tags'])
        item.set_image(img)
        item.set_always_show_image(True)
        #item.connect("activate",self.handler_clipboard, self.treeview.get_selection())
        item.set_submenu(submenu)
        menu.append(item)

        item = Gtk.SeparatorMenuItem()
        menu.append(item)
        item = Gtk.ImageMenuItem.new_with_label("Delete Show")
        img = Gtk.Image.new_from_pixbuf(pixm['delete'])
        item.set_image(img)
        item.set_always_show_image(True)
        item.connect("activate",self.handler_delete_show, self.treeview.get_selection())
        menu.append(item)
        item = Gtk.MenuItem("Details")
        item.connect("activate",self.handler_details, self.treeview.get_selection())
        menu.append(item)

        #######################################################
        treeview.connect("button_release_event", self.handler_pop_up, self.treeview.get_selection(), menu)
        treeview.connect("button_press_event", self.handler_double)
        select = treeview.get_selection()
        select.connect("changed", self.handler_tree_selection, header)

        scrollable_treelist = Gtk.ScrolledWindow()
        scrollable_treelist.set_vexpand(True)
        scrollable_treelist.add(treeview)

        search_e = Gtk.SearchEntry()
        search_e.set_size_request(300,30)
        search_e.connect('activate', self.handler_search_activate)

        bar_box = Gtk.Box()
        bar_box.set_halign(3)
        bar_box.pack_start(search_e, True, True, 0)

        search_w = Gtk.SearchBar()
        search_w.add(bar_box)
        search_w.connect_entry(search_e)
        search_w.set_show_close_button(True)
        self.connect('key-press-event', self.handler_window_key_press_event, search_w)

        searchbutton.bind_property('active',search_w,'search-mode-enabled',1)
        #search_e.connect('search-changed', self.search_changed_cb)
        search_e.connect('changed', self.handler_search_changed)

        vbox_main = Gtk.Box(orientation=1)
        vbox_main.pack_start(search_w, False, True, 0)
        vbox_main.pack_start(scrollable_treelist, True, True, 0)

        self.connect('key-press-event', self.handler_esc_key)
        self.add(vbox_main)
        #self.add(self.scrollable_treelist)
        self.set_titlebar(header)
        #self.refresh_store()
        self.show_all()
        self.emit('fill-all',4)



    #######################################################
    def filter_func(self, model, iter, data):
        if self.filter_on is None or self.filter_on == "None":
            return True
        else:
            a = re.compile(str(self.filter_on), re.I)
            if a.match(model[iter][1]):
                return True 
            else:
                return False

    #def refresh_store(self):
    #    #self.liststore.clear()
    #    self.emit('fill-all',2)

    def set_model(self, model):
        self.treeview.set_model(model)

    def set_pop_window(self, text):
        pop_window(text)


    # Callbacks
    #######################################################
    def handler_esc_key(self, widget, event):pass   
    def handler_search_activate(self, entry):
        self.treeview.set_cursor(Gtk.TreePath.new_from_indices([0]))

    def handler_search_changed(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.filter_on = widget.get_text()
        text = widget.get_text()
        #we update the filter, which updates in turn the view
        self.emit('search-show',text)
        #self.log_filter.refilter()

    def handler_window_key_press_event(self,event,void,bar):
        return bar.handle_event(void)

    def handler_pop_up(self, widget, event, selection, menu):
        if event.button == 3:
            model,iter = selection.get_selected()
            if iter != None:
                menu.popup(None, None, None, None, event.button, event.time)
                menu.show_all()

    def handler_double(self, widget, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            #alloc = self.get_allocation()
            #self.pop2.set_visible(True)
            #rect = cairo.RectangleInt()
            #rect.x=event.x - alloc.x
            #rect.y=event.y - alloc.y
            #print event.x,event.y
            #print alloc.x,alloc.y
            #print rect.x,rect.y
            #self.pop2.set_pointing_to(rect)
            selection = widget.get_selection()
            self.handler_go_torrent(widget, selection)
            self.handler_go_subtitle(widget, selection)

    def handler_details(self, widget, selection):
        model,iter = selection.get_selected()
        if iter !=None:
            text=''
            self.emit('details',model,iter,text)

    def handler_radio_changed(self, button, name):
        if button.get_active():
            if name == 1:
                self.emit('reload',1)
            elif name == 3:
                self.emit('reload',3)
            elif name == 4:
                self.emit('reload',4)
            elif name == 2:
                self.emit('reload',2)
        else:pass

    def handler_up(self, widget):pass

    def handler_pop_closed(self, widget, button):
        button.set_active(False)

    def handler_toggle_options(self, button, popover):
        popover.set_visible(button.get_active())
        #self.pop.show_all()

    def handler_tree_selection(self, selection, header):
        model,iter = selection.get_selected()
        if iter != None:
            header.set_title(model[iter][1])
    def handler_set_tag(self, w, e, selection,code):
        model,iter = selection.get_selected()
        if iter !=None:
            self.emit('tag', model, iter, code)

    def handler_season_done(self, widget, selection):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Season Done!")
        dialog.format_secondary_text("Are You Sure?")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            model,iter = selection.get_selected()
            if iter !=None:
                self.emit('season-done',model,iter)
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def handler_dialog_new(self, widget):
        dialog = DialogNew(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.emit('new-entry',(dialog.entry1.get_text(), dialog.entry2.get_text(), dialog.entry3.get_text(), dialog.entry4.get_text()))
            #self.refresh_store()
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            #self.emit('my_signal')
            #print("The Cancel button was clicked")
            dialog.destroy()

    def handler_dialog_edit(self, widget, selection):
        model,iter = selection.get_selected()
        if iter !=None:
            dialog = DialogEdit(self,selection)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Update!")
                dialog2.format_secondary_text("Are You Sure?")
                response2 = dialog2.run()
                if response2 == Gtk.ResponseType.YES:
                    if iter !=None:
                        self.emit('update-show',(dialog.entry1.get_text(), dialog.entry2.get_text(), dialog.entry3.get_text(), dialog.entry4.get_text()), model,iter)
                elif response2 == Gtk.ResponseType.NO:pass
                dialog2.destroy()
            elif response == Gtk.ResponseType.CANCEL:pass
                #self.emit('my_signal')
                #print("The Cancel button was clicked")
            dialog.destroy()

    def handler_undo(self, widget):
            self.emit('undotrans')

    def handler_dialog_msg(self, model,str):
        dialog = Gtk.MessageDialog(self, 1, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Error")
        dialog.format_secondary_text(str)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:pass
        elif response == Gtk.ResponseType.CANCEL:pass
        dialog.destroy()

    def handler_delete_show(self, widget, selection):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Delete!")
        dialog.format_secondary_text("Are You Sure?")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            model,iter = selection.get_selected()
            if iter !=None:
                #print(model[iter][0])
                self.emit('delete-show',model,iter)
                #self.refresh_store()
                #print model.iter_next(iter)
                #self.treeview.set_cursor(model.iter_next(iter))
                #model= self.treeview.get_model()
                #if model.iter_previous(iter) != None:
                #    self.treeview.set_cursor(model.get_path(model.iter_previous(iter)))
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def handler_add_one(self, widget, selection):
        dialog2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Add One!")
        dialog2.format_secondary_text("Are You Sure?")
        response2 = dialog2.run()
        if response2 == Gtk.ResponseType.YES:
            model,iter = selection.get_selected()
            if iter !=None:
                #print(model[iter][0])
                self.emit('add-one',model,iter)
        elif response2 == Gtk.ResponseType.NO:pass
        dialog2.destroy()

    def handler_get_detail(self, widget, selection):
        dialog2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Add One!")
        dialog2.format_secondary_text("Are You Sure?")
        response2 = dialog2.run()
        if response2 == Gtk.ResponseType.YES:
            model,iter = selection.get_selected()
            if iter !=None:
                #print(model[iter][0])
                self.emit('add-one',model,iter)
        elif response2 == Gtk.ResponseType.NO:pass
        dialog2.destroy()

    def handler_clipboard(self, widget, selection):
        model,iter = selection.get_selected()
        if iter !=None:
            self.clipboard.set_text(model[iter][1], -1)

    def handler_go_subtitle(self, widget, selection):
        model,iter = selection.get_selected()
        if iter !=None:
            self.emit('subtitle',model,iter)

    def handler_go_torrent(self, widget, selection):
        model,iter = selection.get_selected()
        if iter !=None:
            self.emit('torrent',model,iter)


if __name__ == "__main__":
    win = VlogView()
    #win.connect('new_signal', outsider)
    Gtk.main()
