# fragment parser for Android

### Tested against Windows 10 / Python 3.11 / Anaconda / Windows 

### pip install cythonfragmentparser

### Cython and a C compiler must be installed!

```PY
from cythondfprint import add_printer
from cythonfragmentparser import parse_fragments_active_screen
import shutil
add_printer(1)
adbexe = shutil.which("adb.exe")
counter=0
try:
    while True:
        df = parse_fragments_active_screen(
            serial="127.0.0.1:5585",
            adb_path=adbexe,
            number_of_max_views=1,
            screen_width=900,
            screen_height=1600,
            subproc_shell=False,
        )
        print(df)
        counter=counter+1
        print(counter)
except KeyboardInterrupt:
    pass
```