import os
from gi.repository import GdkPixbuf

class Assets():
    abs_path = os.path.dirname(os.path.realpath(__file__)) + '/'
    icon_folder = 'assets'
    pixbuf = {}
    db_name = 'vlog.db'

    @staticmethod
    def get_db(): return Assets.abs_path + Assets.db_name

    @staticmethod
    def get_pix():
        pix_files = [
            ('green','Thumbs_up.png'),
            ('blue','bb.png'), 
            ('red','Warning.png'), 
            ('wood','wooden-box.png'), 
            ('add','add2.png'), 
            ('modify','edit.png'), 
            ('find','search_16.png'),
            ('undo','undo-icon.png'),
            ('tags','Tags.png'),
            ('delete','cross.png'),
            ('add2','add.png'),
            ('blue-tag','Dark_blue_button.png'),
            ('green-tag','Green_button.png'),
            ('silver-tag','Silver_button.png'),
            ('red-tag','Red_button.png'),
            ('orange-tag','Orange_button.png'),
            ('torrent','tumblr.png'),
            ('subtitle','ic_text_format_48px-16.png'),
        ]
        for name,file in pix_files:
            Assets.pixbuf[name] = GdkPixbuf.Pixbuf.new_from_file_at_size(Assets.abs_path + Assets.icon_folder + '/' + file, 16, 16)
        return Assets.pixbuf

if __name__ == "__main__":
    print Assets.get_db()
    print Assets.get_pix()
