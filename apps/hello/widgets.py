from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe
from django import forms


class DatePickerWidget(forms.DateInput):

    class Media:
        '''
        You need to download CSS-file from an external source.
        Otherwise, it can break internal links.
        '''

        js = (
            staticfiles_storage.url('js/datewidget/jquery-1.11.3.js'),
            staticfiles_storage.url('js/datewidget/jquery-ui.min.js'),
        )
        css = {
            'all': (
                   staticfiles_storage.url('//code.jquery.com/ui/1.11.4/'
                                           'themes/smoothness/jquery-ui.css'),
            )
        }

    def __init__(self, params='', attrs=None):
        self.params = params
        super(DatePickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(DatePickerWidget, self).render(name,
                                                        value,
                                                        attrs=attrs)

        return rendered + mark_safe(u'''<script type="text/javascript">
                                        $('#id_%s').datepicker({%s});
                                        </script>''' % (name, self.params,))
