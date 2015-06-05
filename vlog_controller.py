from vlog_model import VlogModel as Mod
from vlog_view import VlogView as View
from gi.repository import GObject, Gtk, GdkPixbuf, Gdk 
from datetime import date
import dateutil.parser, re, webbrowser
import assets_vlog
import collections

class Parser():

    def __init__(self):
        self.edits = []
        self.closeds = []

    def tokenize(self, string):
        self.edits = []
        self.closeds = []
        token_specification = [
            ('RNG' , r'(?<!\S)(?P<RNG>(\d);(\d+)\-(\d+))(?!\S)'),       #3;2-5
            ('SLV' , r'(?<!\S)(?P<SLV>S(\d+)\-S(\d+))(?!\S)'),          #S01-S02
            ('STD' , r'(?<!\S)(?P<STD>(\d)(\d+))(?!\S)'),               #301
            ('SEA' , r'(?<!\S)S(?P<SEA>\d+)(?!\S)'),    #S02 Home made boundries http://www.rexegg.com/regex-boundaries.html http://stackoverflow.com/questions/15601563/regex-word-boundary-b-matching-and-whitespace
            ('STDD' , r'(?<!\S)(?P<STDD>(\d+);(\d+))(?!\S)'),          #30;01
        ]
        tok_regex = '|'.join(pair[1] for pair in token_specification)
        test = '3253 S32 S32-S43 4,03-534 S32-423 :24 506,23' 
        for mo in re.finditer(tok_regex, string):
            kind = mo.lastgroup
            value = mo.group(kind)
            #print mo.groups()
            if kind == 'RNG':
                var = mo.group(2,3,4)
                self.edits.append((int(var[0]),self.fill_range(var[1],var[2])))
            elif kind == 'SLV':
                var = mo.group(6,7)
                self.closeds.extend(self.fill_range(var[0],var[1]))
            elif kind == 'STD':
                var = mo.group(9,10)
                self.edits.append((int(var[0]),[int(var[1])]))
            elif kind == 'SEA':
                var = mo.group(11)
                self.closeds.extend([int(var)])
            elif kind == 'STDD':
                var = mo.group(13,14)
                self.edits.append((var[0],[var[1]]))
            else:
                print mo.group()

        return self.edits, self.closeds



    def fill_range(self, low, high):
        if low > high:
            temp = low
            low = high
            high = temp
        elif low == high:
            return low
        return list(range(int(low), int(high) + 1))

    def join(self,sea,epi):
        if sea == None:
            return '---'
        if epi == None:
            return '[ '+str(sea)+' ]'
        if epi < 10:
            epi = '0'+str(epi)
        else:
            epi = str(epi)
        return str(sea) + epi

    def get_edit(self):
        return self.edits

    def get_closeds(self):
        return self.closeds

class VlogController(GObject.GObject):
    __gsignals__ = {
        'trash-warn': (GObject.SIGNAL_RUN_FIRST, None,
                      (str,)),
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.pixbuf = assets_vlog.Assets.get_pix()
        self.par = Parser() 
        self.m = Mod()
        self.v = View(self.m)
        self.v.connect('new-entry', self.new_entry)
        self.v.connect('delete-show', self.delete)
        self.v.connect('season-done', self.done)
        #self.v.connect('fill-all', self.fill)
        self.v.connect('add-one', self.add_one)
        self.v.connect('zoom', self.get_detail)
        self.v.connect('torrent', self.go_torrent)
        self.v.connect('subtitle', self.go_subtitle)
        self.v.connect('update-show', self.edit)
        self.v.connect('undotrans', self.undoer)
        self.v.connect('search-show', self.search_like)
        self.v.connect('reload', self.reload)
        self.v.connect('details', self.get_detail)
        self.v.connect('tag', self.set_tag)
        self.m.connect('error', self.v.handler_dialog_msg)
        #self.connect('trash-warn', self.v.dialog_msg_cb)
        liststore = Gtk.ListStore(int, str, str, str, int, GdkPixbuf.Pixbuf, Gdk.RGBA)

        #self.liststore = Gtk.ListStore(int, str, str, int, str, GdkPixbuf.Pixbuf)
        self.fill_store(liststore, self.m.get_show_list_active())

        #self.v.set_model(None)
        Gtk.main()

    def search_like(self, widget, str):
        res = self.m.search(str)
        model =  widget.treeview.get_model()
        model.clear()
        self.fill_store(model, res)

    def reload(self, widget, code):
        if code == 1:
            res = self.m.get_show_list()
        elif code == 2:
            res = self.m.get_show_list_active()
        elif code == 3:
            res = self.m.get_show_list_completed()
        elif code == 4:
            res = self.m.get_show_list_towatch()
        model =  widget.treeview.get_model()
        model.clear()
        self.fill_store(model, res)

    def edit(self, widget, obj, model, iter):
        id = model[iter][0]
        self.m.update_show(id,obj[2],obj[3])
        #add
        if obj[0] != '':
            edit, close = self.par.tokenize(obj[0])
            self.m.insert_show_season(id, edit)
        #delete
        if obj[1] != '':
            edit, close = self.par.tokenize(obj[1])
            #self.m.delete_show_season(id, edit) #caution
        self.m.commit()

        row = self.m.get_show(id)[0]
        trans = self.row_translate(row)
        model.set(iter,[2,3,4,5],trans[2:])

    def new_entry(self, widget , tuplei):
        #'''(title, sea+epi, date)'''
        #'''data sample [(season1,[episodes,]), (season2,[episodes,]] '''
        edit, close = self.par.tokenize(tuplei[1])
        print edit, close

        self.m.insert_bundle((tuplei[0],tuplei[2],tuplei[3],edit) )
        self.m.commit()

        id = self.m.get_last_show_id()
        row = self.m.get_show(id)[0]

        model = widget.treeview.get_model()
        iter = model.append(self.row_translate(row))
        widget.treeview.set_cursor(model.get_path(iter))

    def add_one(self, w, model, iter): 
        id = model[iter][0]
        stri = model[iter][2]

        row = self.m.get_show(id)[0]
        if row[2] == None: #to watch ise
            self.m.insert_show_season(id, [(1,[1])])
        elif row[3] == None:#sezon tamamlanmissa
            self.m.insert_show_season(id, [(row[2]+1,[1])])
        else:
            self.m.insert_show_episode(id, row[2], [row[3]+1])
        self.m.commit()

        row = self.m.get_show(id)[0]
        trans = self.row_translate(row)
        model.set(iter,[2,3,4,5],trans[2:])

    def get_detail(self, w, model, iter, text): 
        #'''data sample (title,torrent,subtitle,[(season1,[episodes,]), (season2,[episodes,]], tag )'''
        id = model[iter][0]
        stri = model[iter][2]

        row = self.m.get_show_deep(id)
        text = '{}. <big>{}</big>\n'.format(row[0],row[1])
        text += '\t<u>{}</u>\n'.format(row[2])
        text += '\t<u>{}</u>\n'.format(row[3])
        for e in row[6]:
            text += '\t<span background="#f9d229" >season: {}</span>\n'.format(e[0])
            text += '\t\t'
            for k in e[2]:
                text += '<span>{}</span> '.format(k[0])
            text += '\n'
        w.set_pop_window(text)

    def delete(self,widget, model,iter):
        self.m.delete_show(model[iter][0])
        self.m.commit()

        model.remove(iter)
        
    def done(self,widget, model,iter):
        stri = model[iter][2]
        id = model[iter][0]

        row = self.m.get_show(id)[0]
        if row[2] == None: #to watch ise
            print 'havent watched yet'
        elif row[3] == None:#sezon tamamlanmissa
            print 'already completed'
        else:
            self.m.delete_show_episodes(id, row[2])
        self.m.commit()

        row = self.m.get_show(id)[0]
        trans = self.row_translate(row)
        model.set(iter,[2,3,4,5],trans[2:])

    def set_tag(self, widget, model, iter, code):
        print 'hi'
        id = model[iter][0]
        self.m.update_tag(id, code)
        self.m.commit()
        row = self.m.get_show(id)[0]
        print row
        trans = self.row_translate(row)
        model.set(iter,[2,3,4,5,6],trans[2:])


    def delta(self, dateq):
        delta  = date.today() - dateq
        return delta.days

    def to_date(self, datestr):return dateutil.parser.parse(datestr).date()

    def pix_feeder(self, date_var):
        if date_var < 7:
            return self.pixbuf['red']
        elif date_var < 14:
            return self.pixbuf['green']
        else:
            return self.pixbuf['blue']


    def fill_store(self, store, raw):
        for row in raw:
            store.append(self.row_translate(row))
        self.v.set_model(store)

    def row_translate(self,row):
        '''id, title, sea_num, epi_num, date_str'''
        #print row
        send = []
        send.append(row[0])
        send.append(row[1].title())
        send.append(self.par.join(row[2],row[3]))
        send.append(row[4].isoformat())
        days = self.delta(row[4])
        send.append(days)
        send.append(self.pix_feeder(days))
        send.append(self.color_translate(row[5]))
        return send

    def color_translate(self, id):
        if id==2:
            return Gdk.RGBA(0.91,0.98,0.58,1)   #green
        elif id==4:
            return Gdk.RGBA(0.75,0.87,0.98,1)   #blue
        elif id==6:
            return Gdk.RGBA(0.98,0.81,0.78,1)
        else:
            return None

    def go_subtitle(self, widget, model, iter):
        stri = model[iter][2]
        id = model[iter][0]

        row = self.m.get_show_shallow(id)
        webbrowser.open(row[2])

    def go_torrent(self, widget, model, iter):
        stri = model[iter][2]
        id = model[iter][0]

        row = self.m.get_show_shallow(id)
        webbrowser.open(row[3])

    def undoer(self, widget):pass


if __name__ == "__main__":
    o = VlogController()
    #test = '3253 S32 S32-S43 4,03-534 S32-423 :24 506,23' 
    p = Parser()
   # p.tokenize(' 5,32-29 S32 S32-S35 4,03-5 S32-423 :24 506,23')
   # print p.closeds
   # print p.edits
    #o.make_epis('103,104')
    #edit, close = p.tokenize('301 302 3;6-8')
    #print edit, close
