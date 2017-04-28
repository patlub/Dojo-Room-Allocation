"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    (dojo) create_room <room_type> <room_name>
    (dojo) add_person person_name (<FELLOW>|<STAFF>) [<wants_accommodation>]
    (dojo) print_room <room_name>
    (dojo) print_allocations [--o=filename]
    (dojo) print_unallocated [--o=filename]
    (dojo) reallocate_person <person_identifier> <new_room_name>
    (dojo) load_people
    (dojo) save_state [--db=sqlite_database]
    (dojo) load_state <sqlite_database>
    (dojo) (-i | --interactive)
    (dojo) (-h | --help)
Arguments:
    FELLOW|STAFF           Type of person to create/employ
    wants_accommodation    Specify if person(only fellow) wants living space
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    --o=filename
    --db=sqlite_database
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from classes.dojo import Dojo


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


dojo = Dojo()
class TheDojo(cmd.Cmd):
    intro = 'Welcome to THE DOJO OFFICE ALLOCATION PROGRAM!' \
            + ' (type help for a list of commands.)'
    prompt = '(my_program) '

    file = None

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>"""
        room_names = []
        room_names.append(arg['<room_name>'])
        print(room_names)
        room_type = arg['<room_type>']
        dojo.create_room(room_names, room_type)

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <person_name> (<FELLOW>|<STAFF>) [<wants_accommodation>]"""
        person_name = arg['<person_name>']
        accomodation = arg['<wants_accommodation>']

        if arg['<FELLOW>']:
            dojo.add_fellow(person_name, accomodation)
        else:
            dojo.add_staff(person_name)

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        room_name = arg['<room_name>']
        dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [--o=filename]"""
        if arg['--o'] is None:
            dojo.print_allocations()
        else:
            dojo.print_allocations_to_file(arg['--o'])

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        if arg['--o'] is None:
            dojo.print_un_allocations()
        else:
            dojo.print_un_allocations_to_file(arg['--o'])

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        person_name = arg['<person_identifier>']
        room_name = arg['<new_room_name>']
        dojo.re_allocate_person(person_name, room_name)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people"""
        dojo.load_people()

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        if arg['--o'] is None:
            dojo.save_state()
        else:
            dojo.save_state(arg['--o'])

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state [--db=sqlite_database]"""
        if arg['--o'] is None:
            dojo.load_state()
        else:
            dojo.load_state(arg['--o'])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    TheDojo().cmdloop()

print(opt)
