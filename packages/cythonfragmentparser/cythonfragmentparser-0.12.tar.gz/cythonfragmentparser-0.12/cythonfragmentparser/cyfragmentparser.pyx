cimport cython
cimport numpy as np
import cython

import numpy as np
from adbshellexecuter import UniversalADBExecutor

from parifinder import parse_pairs
from flatten_any_dict_iterable_or_whatsoever import fla_tu
import subprocess
import re
import platform
import pandas as pd
from functools import cache
from itertools import takewhile
from nested2nested import nested_list_to_nested_dict
np.import_array()
iswindows = "win" in platform.system().lower()

if iswindows:
    import ctypes
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD

invisibledict = {}
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }

refi = re.compile(r"([^,]+),([^,]+)-([^,]+),([^,]+)", flags=re.I)
hierachyregex = re.compile(rb"^\s*(?:(?:View Hierarchy:)|(?:Looper))")
ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS = "dumpsys activity top -a -c --checkin"

class subi(dict):
    """
    A subclass of dict that automatically creates nested dictionaries for missing keys.
    """
    def __missing__(self, k):
        self[k] = self.__class__()
        return self[k]

cdef list list_split(list l, list indices_or_sections):
    """
    Splits a list into sublists based on the provided indices or sections.

    Parameters:
    l (list): The list to split.
    indices_or_sections (list): The indices or sections to split the list.

    Returns:
    list: A list of sublists.
    """
    cdef:
        Py_ssize_t Ntotal = len(l)
        Py_ssize_t Nsections = len(indices_or_sections) + 1
        Py_ssize_t i
        list[Py_ssize_t] div_points
        list sub_arys
    div_points = [0] + list(indices_or_sections) + [Ntotal]
    sub_arys = []
    for i in range(Nsections):
        if div_points[i] >= Ntotal:
            break
        sub_arys.append(l[div_points[i]:div_points[i + 1]])
    return sub_arys

@cache
def strstrip(x):
    """
    Strips whitespace from a string.

    Parameters:
    x (str): The string to strip.

    Returns:
    str: The stripped string.
    """
    return x.strip()

def iszero(Py_ssize_t o):
    """
    Checks if a number is zero.

    Parameters:
    o (Py_ssize_t): The number to check.

    Returns:
    bool: True if the number is zero, False otherwise.
    """
    return o == 0

def indent2dict(data, removespaces):
    """
    Converts indented text data into a nested dictionary.

    Parameters:
    data (str or list): The indented text data.
    removespaces (bool): Whether to remove spaces from the keys.

    Returns:
    dict: The nested dictionary.
    """
    def convert_to_normal_dict_simple(di):
        globcounter = 0

        def _convert_to_normal_dict_simple(di):
            nonlocal globcounter
            globcounter = globcounter + 1
            if not di:
                return globcounter
            if isinstance(di, subi):
                di = {k: _convert_to_normal_dict_simple(v) for k, v in di.items()}
            return di

        return _convert_to_normal_dict_simple(di)

    def splitfunc(alli, dh):
        def splifu(lix, ind):
            try:
                firstsplit = [n for n, y in enumerate(lix) if y and y[0] == ind]
            except Exception:
                return lix
            result1 = list_split(l=lix, indices_or_sections=firstsplit)
            newi = ind + 1
            splitted = []
            for l in result1:
                if newi < (lendh):
                    if isinstance(l, list):
                        if l:
                            la = splifu(l, newi)
                            splitted.append(la)
                    else:
                        splitted.append(l)
                else:
                    splitted.append(l)
            return splitted

        lendh = len(dh.keys())
        alli2 = [alli[0]] + alli
        return splifu(alli2, ind=0)

    if isinstance(data, (str, bytes)):
        da2 = data.splitlines()
    else:
        da2 = list(data)
    d = {}
    dox = da2.copy()
    dox = [x for x in dox if x.strip()]
    for dx in dox:
        eg = len(dx) - len(dx.lstrip())
        d.setdefault(eg, []).append(dx)
    dh = {k: v[1] for k, v in enumerate(sorted(d.items()))}
    alli = []
    for xas in dox:
        for kx, kv in dh.items():
            if xas in kv:
                alli.append([kx, xas])
                break

    iu = splitfunc(alli, dh)
    allra = []
    d = nested_list_to_nested_dict(l=iu)
    lookupdi = {}
    for iasd, ius in enumerate((q for q in fla_tu(d) if not isinstance(q[0], int))):
        if iasd == 0:
            continue
        it = list(takewhile(iszero, reversed(ius[1][: len(ius[1]) - 2])))
        iuslen = len(ius[1])
        it = ius[1][: iuslen - 2 - len(it)]
        allra.append([it, ius[0]])
        lookupdi[it] = ius[0]

    allmils = []
    for allraindex in range(len(allra)):
        im = allra[allraindex][0]
        mili = []
        for x in reversed(range(1, len(im) + 1)):
            mili.append(lookupdi[im[:x]])
        mili = tuple(reversed(mili))
        allmils.append(mili)
    allmilssorted = sorted(allmils, key=len, reverse=True)
    countdict = {}
    difi = subi()
    allmilssorted = [
        tuple(map(strstrip, x) if removespaces else x) for x in allmilssorted
    ]
    ixas_range = len(allmilssorted)
    for ixas_index in range(ixas_range):
        for rad in range(len(allmilssorted[ixas_index]) + 1):
            ixasrad = allmilssorted[ixas_index][:rad]
            if ixasrad not in countdict:
                countdict[ixasrad] = 0
            countdict[ixasrad] += 1
    for key, item in countdict.items():
        if item != 1:
            continue
        vaxu = difi[key[0]]
        for inxa in range(len(key)):
            if inxa == 0:
                continue
            vaxu = vaxu[key[inxa]]
    difi2 = convert_to_normal_dict_simple(difi)
    return difi2

def execute_sh_command(
    command,
    serial="",
    adb_path="",
    subproc_shell=True,
):
    """
    Executes a shell command on an Android device using adb.

    Parameters:
    command (str): The shell command to execute.
    serial (str): The serial number of the device (default "").
    adb_path (str): The path to the adb executable (default "").
    subproc_shell (bool): Whether to use the shell in the subprocess (default True).

    Returns:
    list: The output lines of the command.
    """
    adbsh=UniversalADBExecutor(adb_path,serial)
    stdout, stderr, returncode = (
        adbsh.shell_with_capturing_import_stdout_and_stderr(
            command=command
        )
    )
    return stdout.strip().splitlines()

def lenq(q):
    """
    Returns the length of the first element in the tuple.

    Parameters:
    q (tuple): The tuple to get the length of the first element.

    Returns:
    int: The length of the first element.
    """
    return len(q[0])

@cache
def get_regex_numbers(datadict_coords):
    """
    Extracts numerical coordinates from a string using a regular expression.

    Parameters:
    datadict_coords (str): The string containing coordinates.

    Returns:
    tuple: A tuple of four integers representing the coordinates.
    """
    regexresults = refi.findall(datadict_coords)
    if regexresults:
        try:
            return tuple(
                map(int, (regexresults[0]))
            )
        except Exception:
            pass
    return (0, 0, 0, 0)

cpdef dict findchi(str ff):
    """
    Finds and parses key-value pairs from a string using a specific format.

    Parameters:
    ff (str): The input string.

    Returns:
    dict: A dictionary containing the parsed key-value pairs.
    """
    cdef:
        dict r0, datadict
        list maininfostmp
        Py_ssize_t maininfos_last_index, last_index_text, infosplitlen_last_index
        list otherdata, infosplit
        str firstimesearch, secondtimesearch, t,orgstri
    try:
        r0 = parse_pairs(string=ff, s1="{", s2="}", str_regex=False)
        datadict = {}
        maininfostmp = list(
            {k: v for k, v in sorted(r0.items(), key=lenq, reverse=True)}.items()
        )
        if not maininfostmp:
            return {}
        maininfos = maininfostmp[0]

        maininfos_last_index = len(maininfos) - 1
        last_index_text = len(maininfos[maininfos_last_index]["text"]) - 1
        otherdata = ff.split(maininfos[maininfos_last_index]["text"])
        orgstri=maininfos[maininfos_last_index]["text"][1 : last_index_text]
        t = (
            orgstri
            + " ÇÇÇÇÇÇ ÇÇÇÇÇÇ"
        )
        infosplit = t.split(maxsplit=5)
        firstimesearch = infosplit[1]
        secondtimesearch = infosplit[2]
        datadict["START_X"] = -1
        datadict["START_Y"] = -1
        datadict["CENTER_X"] = -1
        datadict["CENTER_Y"] = -1
        datadict["AREA"] = -1
        datadict["END_X"] = -1
        datadict["END_Y"] = -1
        datadict["WIDTH"] = -1
        datadict["HEIGHT"] = -1
        datadict["START_X_RELATIVE"] = -1
        datadict["START_Y_RELATIVE"] = -1
        datadict["END_X_RELATIVE"] = -1
        datadict["END_Y_RELATIVE"] = -1
        infosplitlen_last_index = len(infosplit)
        try:
            if infosplitlen_last_index >= 3:
                datadict["COORDS"] = infosplit[infosplitlen_last_index - 3].rstrip("Ç ")
            else:
                datadict["COORDS"] = None
        except Exception:
            datadict["COORDS"] = None
        try:
            datadict["INT_COORDS"] = get_regex_numbers(datadict["COORDS"])
        except Exception:
            datadict["INT_COORDS"] = (0, 0, 0, 0)
        try:
            if otherdata:
                datadict["CLASSNAME"] = otherdata[0]
            else:
                datadict["CLASSNAME"] = None
        except Exception:
            datadict["CLASSNAME"] = None
        try:
            if infosplitlen_last_index >= 2:
                datadict["HASHCODE"] = infosplit[infosplitlen_last_index - 2].rstrip("Ç ")
            else:
                datadict["HASHCODE"] = None
        except Exception:
            datadict["HASHCODE"] = None
        try:
            if infosplitlen_last_index >= 1:
                datadict["ELEMENT_ID"] = infosplit[infosplitlen_last_index-1].rstrip("Ç ")
            else:
                datadict["ELEMENT_ID"] = None
        except Exception:
            datadict["ELEMENT_ID"] = None
        try:
            if infosplit:
                datadict["MID"] = infosplit[0]
            else:
                datadict["MID"] = None
        except Exception:
            datadict["MID"] = None
        maxindexf1 = len(firstimesearch) - 1
        try:
            if maxindexf1 > 0:
                datadict["VISIBILITY"] = firstimesearch[0]
            else:
                datadict["VISIBILITY"] = None
        except Exception:
            datadict["VISIBILITY"] = None

        try:
            if maxindexf1 > 1:
                datadict["FOCUSABLE"] = firstimesearch[1]
            else:
                datadict["FOCUSABLE"] = None
        except Exception:
            datadict["FOCUSABLE"] = None

        try:
            if maxindexf1 > 2:
                datadict["ENABLED"] = firstimesearch[2]
            else:
                datadict["ENABLED"] = None
        except Exception:
            datadict["ENABLED"] = None

        try:
            if maxindexf1 > 3:
                datadict["DRAWN"] = firstimesearch[3]
            else:
                datadict["DRAWN"] = None
        except Exception:
            datadict["DRAWN"] = None

        try:
            if maxindexf1 > 4:
                datadict["SCROLLBARS_HORIZONTAL"] = firstimesearch[4]
            else:
                datadict["SCROLLBARS_HORIZONTAL"] = None
        except Exception:
                datadict["SCROLLBARS_HORIZONTAL"] = None
        try:
            if maxindexf1 > 5:
                datadict["SCROLLBARS_VERTICAL"] = firstimesearch[5]
            else:
                datadict["SCROLLBARS_VERTICAL"] = None
        except Exception:
                datadict["SCROLLBARS_VERTICAL"] = None
        try:
            if maxindexf1 > 6:
                datadict["CLICKABLE"] = firstimesearch[6]
            else:
                datadict["CLICKABLE"] = None
        except Exception:
                datadict["CLICKABLE"] = None
        try:
            if maxindexf1 > 7:
                datadict["LONG_CLICKABLE"] = firstimesearch[7]
            else:
                datadict["LONG_CLICKABLE"] = None
        except Exception:
                datadict["LONG_CLICKABLE"] = None
        try:
            if maxindexf1 >= 8:
                datadict["CONTEXT_CLICKABLE"] = firstimesearch[8]
            else:
                datadict["CONTEXT_CLICKABLE"] = None
        except Exception:
                datadict["CONTEXT_CLICKABLE"] = None

        maxindexf2 = len(secondtimesearch) - 1
        try:
            if maxindexf2 > 0:
                datadict["PFLAG_IS_ROOT_NAMESPACE"] = secondtimesearch[0]
            else:
                datadict["PFLAG_IS_ROOT_NAMESPACE"] = None
        except Exception:
                datadict["PFLAG_IS_ROOT_NAMESPACE"] = None
        try:
            if maxindexf2 > 1:
                datadict["PFLAG_FOCUSED"] = secondtimesearch[1]
            else:
                datadict["PFLAG_FOCUSED"] = None
        except Exception:
                datadict["PFLAG_FOCUSED"] = None
        try:
            if maxindexf2 > 2:
                datadict["PFLAG_SELECTED"] = secondtimesearch[2]
            else:
                datadict["PFLAG_SELECTED"] = None
        except Exception:
                datadict["PFLAG_SELECTED"] = None
        try:
            if maxindexf2 > 3:
                datadict["PFLAG_PREPRESSED"] = secondtimesearch[3]
            else:
                datadict["PFLAG_PREPRESSED"] = None
        except Exception:
                datadict["PFLAG_PREPRESSED"] = None
        try:
            if maxindexf2 > 4:
                datadict["PFLAG_HOVERED"] = secondtimesearch[4]
            else:
                datadict["PFLAG_HOVERED"] = None
        except Exception:
                datadict["PFLAG_HOVERED"] = None
        try:
            if maxindexf2 > 5:
                datadict["PFLAG_ACTIVATED"] = secondtimesearch[5]
            else:
                datadict["PFLAG_ACTIVATED"] = None
        except Exception:
                datadict["PFLAG_ACTIVATED"] = None
        try:
            if maxindexf2 > 6:
                datadict["PFLAG_INVALIDATED"] = secondtimesearch[6]
            else:
                datadict["PFLAG_INVALIDATED"] = None
        except Exception:
                datadict["PFLAG_INVALIDATED"] = None
        try:
            if maxindexf2 >= 7:
                datadict["PFLAG_DIRTY_MASK"] = secondtimesearch[7]
            else:
                datadict["PFLAG_DIRTY_MASK"] = None
        except Exception:
                datadict["PFLAG_DIRTY_MASK"] = None
        datadict["ORIGINAL_STRING"] =orgstri
        return datadict
    except Exception:
        return {}

@cache
def regex_check(s):
    """
    Checks if a string matches a specific regex pattern.

    Parameters:
    s (str): The string to check.

    Returns:
    bool: True if the string matches the pattern, False otherwise.
    """
    if hierachyregex.search(s):
        return True
    return False

def get_all_activity_elements(str serial="", str adb_path="", Py_ssize_t number_of_max_views=-1, cython.bint subproc_shell=True):
    """
    Retrieves all activity elements from an Android device using adb.

    Parameters:
    serial (str): The serial number of the device (default "").
    adb_path (str): The path to the adb executable (default "").
    number_of_max_views (Py_ssize_t): The maximum number of views to retrieve (default -1).
    subproc_shell (cython.bint): Whether to use the shell in the subprocess (default True).

    Returns:
    list: A list of all activity elements.
    """
    cdef:
        dict datadict
        dict cachedict = {}
        list list2split = []
        list allda, allsplits, allsi
        cython.bytes hierachybytes = b"View Hierarchy:"
        Py_ssize_t indi1, indi2, len_allsplits, elemtindex, hierachcounter, hierachcounter2, lenf1, ffindex, last_index_allchildrendata, last_index_item
        dict di
        list[list] allchildrendata
        list[list[list]] allconvdata
    try:
        allda = execute_sh_command(
            ADB_SHELL_GET_ALL_ACTIVITY_ELEMENTS,
            serial,
            adb_path,
            subproc_shell
        )
    except Exception:
        allda = []
    lenallda = len(allda)
    for indi1 in range(lenallda):
        if regex_check(allda[indi1]):
            list2split.append(indi1)
    allsi = list_split(
        allda,
        list2split,
    )
    allsplits = []
    for indi2 in range(len(allsi)):
        if allsi[indi2]:
            if hierachybytes in allsi[indi2][0]:
                allsplits.append(allsi[indi2])
    len_allsplits = len(allsplits)
    if number_of_max_views > 0:
        if len_allsplits - number_of_max_views < 0:
            raise IndexError('Out of bounds')
        allsplits = allsplits[len_allsplits - number_of_max_views:]

    len_allsplits = len(allsplits)
    allconvdata = []
    for elemtindex in range(len_allsplits):
        try:
            di = indent2dict(
                b"\n".join(allsplits[elemtindex]).decode("utf-8", "ignore"), removespaces=True
            )
        except Exception:
            di = {}
        if not di:
            continue
        allchildrendata = []
        hierachcounter = 0
        for f in fla_tu(di):
            allchildrendata.append([])

            hierachcounter += 1
            hierachcounter2 = 0
            lenf1 = len(f[1])
            for ffindex in range(lenf1):
                try:
                    try:
                        datadict = {kx: vx for kx, vx in cachedict.setdefault(f[1][ffindex], findchi(f[1][ffindex])).items()}
                        if not datadict:
                            continue
                    except Exception:
                        continue
                    last_index_allchildrendata = len(allchildrendata) - 1
                    allchildrendata[last_index_allchildrendata].append(datadict)
                    datadict["START_X"] = sum(
                        [
                            x["INT_COORDS"][0]
                            for x in allchildrendata[last_index_allchildrendata]
                        ]
                    )
                    datadict["START_Y"] = sum(
                        [
                            x["INT_COORDS"][1]
                            for x in allchildrendata[last_index_allchildrendata]
                        ]
                    )
                    datadict["WIDTH"] = (
                        datadict["INT_COORDS"][2] - datadict["INT_COORDS"][0]
                    )
                    datadict["HEIGHT"] = (
                        datadict["INT_COORDS"][3] - datadict["INT_COORDS"][1]
                    )

                    datadict["END_X"] = datadict["START_X"] + datadict["WIDTH"]
                    datadict["END_Y"] = datadict["START_Y"] + datadict["HEIGHT"]
                    datadict["CENTER_X"] = datadict["START_X"] + (
                        datadict["WIDTH"] // 2
                    )
                    datadict["CENTER_Y"] = datadict["START_Y"] + (
                        datadict["HEIGHT"] // 2
                    )

                    datadict["AREA"] = (datadict["HEIGHT"] * datadict["WIDTH"])

                    datadict["START_X_RELATIVE"] = datadict["INT_COORDS"][0]
                    datadict["START_Y_RELATIVE"] = datadict["INT_COORDS"][1]
                    datadict["END_X_RELATIVE"] = datadict["INT_COORDS"][2]
                    datadict["END_Y_RELATIVE"] = datadict["INT_COORDS"][3]
                    datadict["IS_PARENT"] = True
                    datadict["VIEW_INDEX"] = elemtindex
                    datadict["HIERACHY_CLUSTER"] = hierachcounter
                    datadict["HIERACHY_SINGLE"] = hierachcounter2
                    hierachcounter2 = hierachcounter2 + 1

                except Exception:
                    continue

        try:
            last_index_allchildrendata = len(allchildrendata) - 1
            last_index_item = len(allchildrendata[last_index_allchildrendata]) - 1
            allchildrendata[last_index_allchildrendata][last_index_item][
                "IS_PARENT"
            ] = False
            allconvdata.append([list(x) for x in allchildrendata])

        except Exception:
            pass
    return allconvdata

cpdef tuple[dict[cython.ulonglong,set],dict[cython.ulonglong,set[tuple]]] parse_children(
    cython.Py_ssize_t[:] HIERACHY_SINGLE,
    cython.Py_ssize_t[:] HIERACHY_CLUSTER,
    cython.ulonglong[:] ORIGINAL_STR_ID,
    dict mapping_dict):
    cdef:
        dict parentsdict
        dict[cython.ulonglong,set] all_my_children_together
        dict[cython.ulonglong,set[tuple]] all_my_children

        Py_ssize_t hierachyindex1, hierachyindex2
    parentsdict = {}
    for hierachyindex1 in range(len(HIERACHY_SINGLE)):
        if ORIGINAL_STR_ID[hierachyindex1] not in parentsdict:
            parentsdict[ORIGINAL_STR_ID[hierachyindex1]] = {}
        for hierachyindex2 in range(len(HIERACHY_SINGLE)):
            if hierachyindex2 <= hierachyindex1:
                continue
            if HIERACHY_CLUSTER[hierachyindex1] < HIERACHY_CLUSTER[hierachyindex2]:
                break

            if HIERACHY_SINGLE[hierachyindex2] > HIERACHY_SINGLE[hierachyindex1]:
                if HIERACHY_CLUSTER[hierachyindex2] not in parentsdict[ORIGINAL_STR_ID[hierachyindex1]]:
                    parentsdict[ORIGINAL_STR_ID[hierachyindex1]][HIERACHY_CLUSTER[hierachyindex2]] = {
                        HIERACHY_SINGLE[hierachyindex2]: {}
                    }
                parentsdict[ORIGINAL_STR_ID[hierachyindex1]][HIERACHY_CLUSTER[hierachyindex2]][
                    HIERACHY_SINGLE[hierachyindex2]
                ] = mapping_dict[ORIGINAL_STR_ID[hierachyindex2]]

    all_my_children_together = {}
    all_my_children = {}

    for parent, childrengroup in parentsdict.items():
        for childrendictx in childrengroup.values():
            if parent not in all_my_children:
                all_my_children[parent] = set()
            all_my_children[parent].add(tuple(childrendictx.values()))

            if parent not in all_my_children_together:
                all_my_children_together[parent] = set()
            all_my_children_together[parent].update((childrendictx.values()))
    return all_my_children_together,all_my_children

def parse_fragments_active_screen(
    serial="",
    adb_path="",
    number_of_max_views=1,
    screen_width=720,
    screen_height=1280,
    subproc_shell=False,
):
    """
    Parses the active screen fragments from an Android device and returns them as a DataFrame.

    Parameters:
    serial (str): The serial number of the device (default "").
    adb_path (str): The path to the adb executable (default "").
    number_of_max_views (int): The number of maximum views to retrieve (default 1).
    screen_width (int): The width of the screen (default 720).
    screen_height (int): The height of the screen (default 1280).
    subproc_shell (bool): Whether to use the shell in the subprocess (default False).

    Returns:
    pd.DataFrame: The parsed screen fragments as a DataFrame.
    """
    screen_area = float(screen_width) * float(screen_height)
    d = get_all_activity_elements(
        serial, adb_path, number_of_max_views, subproc_shell
    )
    if not d: 
        return pd.DataFrame()
    dframelist = []
    for l1 in range(len(d)):
        e = d[l1]
        for l2 in range(len(e)):
            ee = e[l2]
            last_element_list = []
            for n0 in range(len(ee) - 1):
                last_element_list.append(False)
            last_element_list.append(True)
            try:
                dframelist.append(pd.DataFrame(ee).assign(IS_LAST=last_element_list))
            except Exception:
                pass

    try:
        df = pd.concat(dframelist, ignore_index=True)
        df=df.assign(AREA_PERCENTAGE=((df.AREA.astype("Float64") / screen_area) * 100.0).astype("Float64"))
        df.loc[:, "ORIGINAL_STR_ID"] = df.ORIGINAL_STRING.apply(id)
        df.loc[:, "ORIGINAL_STR_ID"] = (
            df["ORIGINAL_STR_ID"] + df.END_X + df.END_Y + df.WIDTH + df.HEIGHT
        ).astype(np.uint64)
        df.HIERACHY_CLUSTER = df.HIERACHY_CLUSTER.astype(np.int64)
        df.HIERACHY_SINGLE = df.HIERACHY_SINGLE.astype(np.int64)
        HIERACHY_CLUSTER = df.HIERACHY_CLUSTER.__array__().astype(np.int64)
        HIERACHY_SINGLE = df.HIERACHY_SINGLE.__array__().astype(np.int64)
        ORIGINAL_STR_ID = df.ORIGINAL_STR_ID.__array__().astype(np.uint64)
        #parentsdict = {}
        dfn = df.drop_duplicates(subset=["ORIGINAL_STR_ID"]).reset_index(drop=True).copy()
        dfn["REAL_INDEX"] = dfn.index.__array__().copy()
        dfn.index = dfn.ORIGINAL_STR_ID.__array__().copy()
        mapping_dict = dfn.REAL_INDEX.to_dict()
        all_my_children_together,all_my_children=parse_children(HIERACHY_SINGLE,HIERACHY_CLUSTER,ORIGINAL_STR_ID,mapping_dict)
        dfn["ALL_MY_CHILDREN"] = dfn["ORIGINAL_STR_ID"].apply(lambda q: ())
        dfn.loc[all_my_children_together.keys(), "ALL_MY_CHILDREN"] = dfn.loc[
            all_my_children_together.keys()
        ].apply(lambda q: tuple(sorted(all_my_children_together[q.name])), axis=1)
        dfn["ALL_MY_CHILDREN_GROUPED"] = dfn["ORIGINAL_STR_ID"].apply(lambda q: ())
        dfn.loc[all_my_children.keys(), "ALL_MY_CHILDREN_GROUPED"] = dfn.loc[
            all_my_children.keys()
        ].apply(lambda q: tuple(all_my_children[q.name]), axis=1)
        dfn.index = dfn["REAL_INDEX"].__array__().copy()
        dfn.drop(
            columns=[
                "IS_PARENT",
                "VIEW_INDEX",
                "HIERACHY_CLUSTER",
                "HIERACHY_SINGLE",
                "IS_LAST",
                "ORIGINAL_STR_ID",

            ],inplace=True
        )
        dfn.columns = [
            ("aa_{}".format(dfn.columns[i])).lower() for i in range(len(dfn.columns))
        ]
        return dfn
    except Exception: 
        return pd.DataFrame()
