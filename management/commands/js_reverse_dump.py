from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from js_reverse.templatetags.js_reverse import build_context
from js_reverse.settings import *
from js_reverse.apps import JsReverseConfig as App

from io import StringIO
import os
from inspect import getfile

class Command(BaseCommand):
    help = 'Create a javascript file that defines the %s object and its initialization with the specified view names' % JS_OBJECT_NAME
    default_filename = 'js_reverse.js'
    static_choices_yes = ['true', '1', 'y', 'yes', 'only',]
    static_choices_no = ['false', '0', 'n', 'no',]

    def add_arguments(self, parser):
        
        parser.add_argument(
            '--filename',
            default=self.default_filename,
            nargs='?',
            const=self.default_filename,
            metavar='<filename>',
            dest='output_file',
            help='The output file name to use (default: "%(default)s")'
        )
        
        parser.add_argument(
            '--static',
            default='no',
            nargs='?',
            const='yes',
            choices=self.static_choices_yes + self.static_choices_no,
            metavar='<create static>',
            dest='create_static',
            help='Wether to create a copy of this file in this default app static directory (default: "%(default)s"). Accepted values are: %(choices)s. If \'only\' is given, only the file in the static directory will be produced'
        )
        
        parser.add_argument(
            '--viewname',
            default=ALL_NAMES,
            nargs='+',
            metavar='<view name>',
            dest='view_names',
            help='Space separated list of view names (with namespaces) to include in the generated script. (default: "%(default)s"). If this option is provided, it must be the last one'
        )
        
    def handle(self, *args, **options):
        try:
            context = build_context(' '.join(options['view_names']))
            rendered_object = render_to_string('js_reverse/object.js', context)
            rendered_add_names = render_to_string('js_reverse/add_urls.js', context)
            
            if options['create_static'] != 'only':
                self.write_file(options['output_file'], rendered_object, rendered_add_names)
            if options['create_static'] in self.static_choices_yes:
                static_filename = os.path.join(os.path.dirname(getfile(App)), 'static', 'js_reverse', options['output_file'])
                self.write_file(static_filename, rendered_object, rendered_add_names)
            
            self.print_response(**options)
                
        except Exception as e:
            self.stderr.write(self.style.ERROR(str(e)))
    
    def write_file(self, filename, rendered_object, rendered_add_names):
        with open(filename, 'w') as file:
            file.write(rendered_object)
            file.write('\n\n')
            for line in StringIO(rendered_add_names):
                if(line != '\n'):
                    file.write(line)
                    
    def print_response(self, **options):
        if options['create_static'] != 'only':
            self.stdout.write(self.style.SUCCESS('Reverse js script written into file \'%s\' in current directory' % options['output_file']))
            if options['create_static'] in self.static_choices_yes:
                self.stdout.write(self.style.SUCCESS('A copy of this file has also been created in \'%s\'' % static_filename))
        else:
            self.stdout.write(self.style.SUCCESS('Reverse js script written into file \'%s\'' % static_filename))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('You can now move the generated file in your website or static directory and use it in your html with:'))
        self.stdout.write('')
        self.stdout.write('   <script type="text/javascript" src="%s"></script>' % options['output_file'])
        if options['create_static'] in self.static_choices_yes:
            self.stdout.write(self.style.SUCCESS('or'))
            self.stdout.write('')
            self.stdout.write('   {%% load static %%} {%% static "js_reverse/%s" %%}' % options['output_file'])
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('and use the Urls.reverse() javascript function to get the url of your named views'))
        
        if options['verbosity'] > 1:
            self.stdout.write('')
            self.stdout.write('Names imported in your js script:')
            for name,pattern in context['patterns'].items():
                line = '-  ' + name
                if(options['verbosity'] > 2):
                    line += ' (pattern: ' + pattern + ')'
                self.stdout.write(line)