
from django.core.management import call_command
from optparse import make_option
from django.conf import settings
import os
from south.models import MigrationHistory
from apps.hello.models import RequestContent, AboutMe
from urlparse import urlparse
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import glob
from django.db.models import get_app, get_models


def _change_current_thread(threads, sender_id, new_thread):
    """
    Prepares threads for the left-handed panel.
    """
    thread_list = []

    for thread in threads:
        partner = thread.participants.exclude(id=sender_id)[0]
        thread_list.append({
                'thread': thread.id,
                'partner': partner.username,
                'lastid': thread.lastid,
        })

    return {'threads': thread_list, 
            'new_thread': new_thread}


def FixBarista(command):

    result = 'no command'
    linebreaks = ''

    try:

        if command == 'rc_fields':

            rc = RequestContent.objects.first()
            result = rc._meta.get_all_field_names()
            linebreaks = True

        if command == 'rc_clear':

            result = RequestContent.objects.all().delete()

        if command == 'history':

            result = MigrationHistory.objects.all()
            linebreaks = True

        if command == 'clear_history':

            result = MigrationHistory.objects.all().delete()

        if command == 'sh':

            ''' run post_deploy.sh and redirect stderr to stdout
                and stdout to file and print it to stdout '''

            script = 'sh post_deploy.sh 2>&1 | tee -a apps/hello/sh.txt'
            result = os.system(script)

        if command == 'path_base':

            result = os.listdir(settings.BASE_DIR)
            linebreaks = True

        if command == 'path_prebase':

            result = os.listdir(os.path.dirname(settings.BASE_DIR))
            linebreaks = True

        if command == 'path_app':

            folder = os.path.join(settings.BASE_DIR, 'apps', 'hello')
            result = os.listdir(folder)
            linebreaks = True

        if command == 'path_mig':

            folder = os.path.join(settings.BASE_DIR,
                                  'apps',
                                  'hello',
                                  'migrations')
            result = os.listdir(folder)
            linebreaks = True

        if command == 'list':

            make_option('--list',
                        action='store_true',
                        dest='mlist',
                        default=False,
                        help="Tells South to show \
                              all migrations.")
            result = call_command("migrate",
                                  "apps.hello",
                                  mlist=True,)

        if command == 'delete_apps_hello_tables':

            result = call_command("sqlclear",
                                  "hello",)

        if command == 'delete_ghost_migrations':

            make_option('--delete-ghost-migrations',
                        action='store_true',
                        dest='delete_ghosts',
                        default=False,
                        help="Tells South to delete any 'ghost' \
                              migrations (ones in the database \
                              but not on disk).")
            make_option('--ignore-ghost-migrations',
                        action='store_true',
                        dest='ignore_ghosts',
                        default=False,
                        help="Tells South to ignore any 'ghost' \
                              migrations (ones in the database \
                              but not on disk).")
            result = call_command("migrate",
                                  "apps.hello",
                                  delete_ghosts=True,
                                  ignore_ghosts=True,)

        if command == '0002_fake':

            result = call_command("migrate",
                                  "apps.hello",
                                  "0002",
                                  fake=True,)

        if command == 'table_already_exists':

            result = call_command("migrate",
                                  "apps.hello",
                                  fake=True,)

        if command == 'app_db':

            result = settings.DATABASES

        if command == 'goto_0002':

            result = call_command("migrate",
                                  "apps.hello",
                                  "0002",)

        if command == 'app_label':

            rc = AboutMe.objects.first()
            result = rc._meta.app_label

        if command == 'set_app_db':

            settings.DATABASES['default']['NAME'] = 'test8db.sqlite3'
            result = settings.DATABASES

        if command == 'app_tables':

            app = get_app('hello')
            app_tables = []

            for model in get_models(app, include_auto_created=True):
                app_tables.append(model._meta.db_table)

            result = app_tables
            linebreaks = True

        if command == 'redis_ping':

            result = os.system('redis-cli ping')

    except Exception as e:
        result = e

    return result, linebreaks


def check_no_image_in_db(model_instance):
    ''' check if user clear image in db '''

    host = ''
    name = ''

    try:
        host = os.path.abspath(__file__)

        for i in range(4):
            host = os.path.dirname(host)

        name = urlparse(model_instance.photo.url).path

    except ValueError:
        pass

    return host, name


def check_no_image_in_filesystem(file_path):
    ''' check if user deletes image in file system '''

    photo_exists = False

    try:
        if os.path.isfile(file_path):
            photo_exists = True
    except IOError:
        pass

    return photo_exists


def GetTestImage(imagefile, mode='simple'):
    """ Prepear image file for tests """

    IMG_ROOT = os.path.join(settings.BASE_DIR, 'assets/img/')

    if (mode == 'simple'):
        photo = open(IMG_ROOT + imagefile, 'rb')
        return SimpleUploadedFile(photo.name, photo.read())

    elif (mode == 'PIL'):
        if isinstance(imagefile, basestring):
            return Image.open(IMG_ROOT + imagefile)
        else:
            return Image.open(imagefile)


def RemoveTestImages():
    path = os.path.join(os.path.dirname(settings.BASE_DIR),
                        'uploads', 'photo', '*.png')

    for f in glob.glob(path):
        filename = os.path.basename(f)
        if filename.startswith("test"):
            os.remove(f)
