"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    dojo create_room <room_type> <room_name>
    dojo add_person <person_name> <FELLOW|STAFF> [wants_accommodation]
    dojo print_room <room_name>
    dojo print_allocations [-o=filename]
    dojo print_unallocated [-o=filename]
    dojo reallocate_person reallocate_person <person_identifier> <new_room_name>
    dojo load_people
    dojo save_state [--db=sqlite_database]
    dojo load_state <sqlite_database>

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    -o <filename>, --output <filename>  Filename to save output
   --db=sqlite_database
"""

import sys
import cmd
from docopt import docopt, DocoptExit


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


class MyInteractive (cmd.Cmd):
    intro = 'Welcome to my interactive program!' \
        + ' (type help for a list of commands.)'
    prompt = '(my_program) '
    file = None

    @docopt_cmd
    def do_tcp(self, arg):
        """Usage: tcp <host> <port> [--timeout=<seconds>]"""

        print(arg)

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>"""

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <person_name> <FELLOW|STAFF> [wants_accommodation]"""

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [-o=filename]"""

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [-o=filename]"""

    @docopt_cmd
    def do_print_reallocate_person(self, arg):
        """Usage: reallocate_person reallocate_person <person_identifier> <new_room_name>"""




    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)