import gdb

# last_size = None
# malloc_map = {}
#
#
# def ExprAsInt(expr):
#     return int(str(gdb.parse_and_eval("(void*)(%s)" % expr)).split(" ")[0], 16)
#
#
# class MallocFinishBreakpoint(gdb.FinishBreakpoint):
#     def __init__(self):
#         gdb.FinishBreakpoint.__init__(
#             self,
#             gdb.newest_frame(),
#             internal=False,
#         )
#         self.silent = False
#
#     def stop(self):
#         where = ExprAsInt('$rax')
#         print("0x%.8x <---- malloc of 0x%x bytes" % (where, last_size))
#
#         if where in malloc_map:
#             print("[!] where already in malloc map")
#         malloc_map[where] = last_size
#
#         # try:
#         #     gdb.execute("x/4gx 0x%x" % (where - 0x10))
#         # except Exception as e:
#         #     print(e)
#
#         return False
#
#
# class MallocBreakpoint(gdb.Breakpoint):
#     def __init__(self):
#         gdb.Breakpoint.__init__(self, 'malloc', internal=False)
#         self.silent = False
#
#     def stop(self):
#         global last_size
#         last_size = ExprAsInt('$rdi')
#
#         MallocFinishBreakpoint()
#
#         return False
#
#
# class FreeBreakpoint(gdb.Breakpoint):
#     def __init__(self):
#         gdb.Breakpoint.__init__(self, 'free', internal=False)
#         self.silent = False
#
#     def stop(self):
#         where = ExprAsInt('$rax')
#         gdb.execute("info registers")
#         if where in malloc_map:
#             print("0x%.8x <---- free of 0x%x bytes" % (where, malloc_map[where]))
#             del malloc_map[where]
#         else:
#             print("0x%.8x <---- free (not in malloc map?!)" % where)
#
# MallocBreakpoint()
# FreeBreakpoint()

'''
gef➤  python from ipykernel.kernelapp import main; main()
NOTE: When using the `ipython kernel` entry point, Ctrl-C will not work.

To exit, you will have to explicitly quit this process, by either sending
"quit" from a client, or using Ctrl-\ in UNIX-like environments.

To read more about this, see https://github.com/ipython/ipython/issues/2049


To connect another client to this kernel, use:
    --existing kernel-6392.json

---------------------------------------------------------------------------------

➜  ~ jupyter console --ZMQTerminalInteractiveShell.editing_mode=vi --existing kernel-6392.json
Jupyter console 5.2.0

Python 3.5.2 (default, Nov 12 2018, 13:43:14)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.5.0 -- An enhanced Interactive Python. Type '?' for help.



In [1]: import gdb

In [2]: run /home/ubuntu/.gdbinit-gef.py
GEF for linux ready, type `gef' to start, `gef config' to configure
76 commands loaded for GDB 7.11.1 using Python engine 3.5
[*] 4 commands could not be loaded, run `gef missing` to know why.
[+] Configuration from '/home/ubuntu/.gef.rc' restored
[+] 10 extra commands added from '/home/ubuntu/gef-extras/scripts'

'''

class NewCommand(GenericCommand):
    """Dummy new command."""
    _cmdline_ = "newcmd"
    _syntax_ = "{:s}".format(_cmdline_)

    @only_if_gdb_running         # not required, ensures that the debug session is started
    def do_invoke(self, argv):
        # do anything allowed by gef, for example show the current running
        # architecture as Python object:
        print(" = {}".format(current_arch) )
        # or showing the current $pc
        print("pc = {:#x}".format(current_arch.pc))
        print(get_process_maps())
        print("hahahahahahah")
        # print(gdb.parse_and_eval('telescope'))

        for i in range(100):
            # gef_print(DereferenceCommand.pprint_dereferenced(0x0000555555757000, i))
            print(DereferenceCommand.pprint_dereferenced(0x0000555555757000, i))

        address = 0x0000555555757000
        block = read_memory(address, 100 * 8)
        gef_print(hexdump(block, base=address))
        return


register_external_command(NewCommand())
