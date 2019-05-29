import gdb
import sys
from os import system

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



####################################################
In [18]: for i, m in enumerate(vmmap):
       :     print(i, m.path)
       :
0
1 /media/sf_VIRTUALBOX_SHARE/babyheap
2 /media/sf_VIRTUALBOX_SHARE/babyheap
3 /media/sf_VIRTUALBOX_SHARE/babyheap
4 [heap]
5 /lib/x86_64-linux-gnu/libc-2.23.so
6 /lib/x86_64-linux-gnu/libc-2.23.so
7 /lib/x86_64-linux-gnu/libc-2.23.so
8 /lib/x86_64-linux-gnu/libc-2.23.so
9
10 /lib/x86_64-linux-gnu/ld-2.23.so
11
12 [vvar]
13 [vdso]
14 /lib/x86_64-linux-gnu/ld-2.23.so
15 /lib/x86_64-linux-gnu/ld-2.23.so
16
17 [stack]
18 [vsyscall]
###################################################



FIXME:
Reading symbols from ./babyheap...(no debugging symbols found)...done.
warning: File "/media/sf_VIRTUALBOX_SHARE/.gdbinit" auto-loading has been declined by your `auto-load safe-path' set to "$debugdir:$datadir/auto-load".
To enable execution of this file add
        add-auto-load-safe-path /media/sf_VIRTUALBOX_SHARE/.gdbinit
line to your configuration file "/home/ubuntu/.gdbinit".
---Type <return> to continue, or q <return> to quit---


'''

# class NewCommand(GenericCommand):
#     """Dummy new command."""
#     _cmdline_ = "newcmd"
#     _syntax_ = "{:s}".format(_cmdline_)
#
#     @only_if_gdb_running         # not required, ensures that the debug session is started
#     def do_invoke(self, argv):
#         # do anything allowed by gef, for example show the current running
#         # architecture as Python object:
#         print(" = {}".format(current_arch) )
#         # or showing the current $pc
#         print("pc = {:#x}".format(current_arch.pc))
#         print(get_process_maps())
#         print("hahahahahahah")
#         # print(gdb.parse_and_eval('telescope'))
#
#         for i in range(100):
#             # gef_print(DereferenceCommand.pprint_dereferenced(0x0000555555757000, i))
#             print(DereferenceCommand.pprint_dereferenced(0x0000555555757000, i))
#
#         address = 0x0000555555757000
#         block = read_memory(address, 100 * 8)
#         gef_print(hexdump(block, base=address))
#         return
# register_external_command(NewCommand())


def gef_execute_gdb_script(commands):
    """Execute the parameter `source` as GDB command. This is done by writing `commands` to
    a temporary file, which is then executed via GDB `source` command. The tempfile is then deleted."""
    fd, fname = tempfile.mkstemp(suffix=".gdb", prefix="gef_")
    with os.fdopen(fd, "w") as f:
        f.write(commands)
        f.flush()

    output = ""

    if os.access(fname, os.R_OK):
        output = gdb.execute("source {:s}".format(fname), to_string=True)
        os.unlink(fname)

    return output


# malloc_counter = 0
snapshot_num = 0

def get_heap_start_addr():
    get_process_maps.cache_clear()
    vmmap = get_process_maps()
    try:
        heap_section = next (s for s in vmmap if '[heap]' in s.path)
    except Exception as e:
        print("get_heap_start_addr Exception:", str(e))
        return None

    heap_start = heap_section.page_start
    return int(heap_start)


def print_heap(header=None):
    global snapshot_num
    if not header:
        header = ""

    snapshot_num += 1

    # gdb.execute("vmmap heap")

    # get_process_maps.cache_clear()

    heap_start_addr = get_heap_start_addr()
    first_chunk_size = 0
    if heap_start_addr:
        first_chunk_size = read_int_from_memory(heap_start_addr + 0x8)
        first_chunk_size &= ~0xf

    # heap_start = heap_section.page_start

    def gdbcmd(command):
        res = "gef➤ %s\n" % command
        res += gef_execute_gdb_script(command)
        return res

    filename = 'snapshot_%03d' % snapshot_num
    with open(filename, 'w') as filetowrite:
        output = " %s *****************************************************\n" % filename
        output += header + "\n"

        # output += gdbcmd("telescope &__malloc_hook 3")

        output += gdbcmd("telescope $_heap({}) {}".format(hex(first_chunk_size), 50))
        # output += gdbcmd("telescope {} {}".format(hex(heap_start), 50))
        # output += "gef➤ telescope {} {}\n".format(hex(heap_start), 50)
        # for i in range(50):
        #     output += DereferenceCommand.pprint_dereferenced(heap_start, i)
        #     output += "\n"

        output += gdbcmd("heap chunks")
        output += gdbcmd("heap bins")

        system("clear")
        print(output)
        filetowrite.write(output)


class MyTraceMallocBreakpoint(gdb.Breakpoint):
    def __init__(self, name):
        super(MyTraceMallocBreakpoint, self).__init__(name, gdb.BP_BREAKPOINT, internal=True)
        self.name = name
        self.silent = True

    def stop(self):
        # global malloc_counter
        # malloc_counter += 1

        size = get_register(current_arch.function_parameters[0])
        print_heap("{}({}) [ before ]".format(self.name, hex(size)))
        self.retbp = MyTraceMallocRetBreakpoint(self.name, size)
        # return False
        return True


class MyTraceMallocRetBreakpoint(gdb.FinishBreakpoint):
    """Internal temporary breakpoint to retrieve the return value of malloc()."""

    def __init__(self, name, size):
        super(MyTraceMallocRetBreakpoint, self).__init__(gdb.newest_frame(), internal=True)
        self.name = name
        self.size = size
        self.silent = True

    def stop(self):
        if self.return_value:
            addr = long(self.return_value)
        else:
            addr = to_unsigned_long(gdb.parse_and_eval(current_arch.return_register))

        print_heap("{}({}) == {}  [ after ]".format(self.name, hex(self.size), hex(addr)))

        # if malloc_counter == 1:
        #     return True

        # return False
        return True


class MyTraceFreeBreakpoint(gdb.Breakpoint):
    """Track calls to free() and attempts to detect inconsistencies."""
    def __init__(self):
        super(MyTraceFreeBreakpoint, self).__init__("__libc_free", gdb.BP_BREAKPOINT, internal=True)
        self.silent = True
        return

    def stop(self):
        addr = long(gdb.parse_and_eval(current_arch.function_parameters[0]))
        self.retbp = MyTraceFreeRetBreakpoint(addr)
        print_heap("__libc_free({}) [ before ]".format(hex(addr)))
        # return False
        return True


class MyTraceFreeRetBreakpoint(gdb.FinishBreakpoint):
    """Internal temporary breakpoint to track free-ed values."""

    def __init__(self, addr):
        super(MyTraceFreeRetBreakpoint, self).__init__(gdb.newest_frame(), internal=True)
        self.silent = True
        self.addr = addr
        return

    def stop(self):
        print_heap("__libc_free({}) [ after  ]".format(hex(self.addr)))
        # return False
        return True

MyTraceFreeBreakpoint()
MyTraceMallocBreakpoint("__libc_malloc")
MyTraceMallocBreakpoint("__libc_calloc")

