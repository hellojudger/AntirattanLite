import requests

session = requests.session()
arguments = {
    "source": "",
    "compiler": "g132",
    "options": {
        "userArguments": "-O3 -w",
        "compilerOptions": {
            "producePp": None,
            "produceGccDump": {},
            "produceOptInfo": False,
            "produceCfg": False,
            "produceIr": None,
            "produceLLVMOptPipeline": None,
            "produceDevice": False,
            "overrides": [],
        },
        "filters": {
            "binaryObject": False,
            "binary": False,
            "execute": False,
            "intel": True,
            "demangle": True,
            "labels": True,
            "libraryCode": True,
            "directives": True,
            "commentOnly": True,
            "trim": False,
            "debugCalls": False,
        },
        "tools": [],
        "libraries": [],
        "executeParameters": {"args": "", "stdin": ""},
    },
    "lang": "c++",
    "files": [],
    "bypassCache": 0,
    "allowStoreCodeDebug": True,
}
url = "https://godbolt.org/api/compiler/g132/compile"
header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
    "Referer" : "https://godbolt.org",
    "Accept" : "application/json, text/javascript, */*; q=0.01"
}

def get_info(rattan):
    global arguments
    arguments["source"] = rattan
    rattan_info = session.post(url, json=arguments, headers=header).json()["asm"]
    rattan_funcs = []
    rattan_assembly = list(map(lambda x:x["text"], rattan_info))
    pos = -1
    visited = {}
    for line in rattan_info:
        pos += 1
        text = str(line["text"])
        if text.startswith(".") or text.startswith(" ") or text.startswith("\t") or text.startswith("\n"):
            continue
        if len(text.strip().rstrip()) == 0:
            continue
        if pos == len(rattan_info) - 1:
            continue
        if str(rattan_info[pos+1]["text"]).strip().rstrip().startswith(".zero"):
            continue
        if str(rattan_info[pos+1]["text"]).strip().rstrip().startswith(".quad"):
            continue
        funcname = text.split('(')[0]
        cur = pos + 1
        while True:
            if rattan_info[cur]["source"] is not None:
                break
            cur += 1
        ed = cur
        edline = int(-pow(10, 18))
        while True:
            if rattan_info[ed]["text"].startswith("."):
                ed += 1
                continue
            if rattan_info[ed]["source"] is None:
                break
            if rattan_info[ed]["source"]["file"] is not None:
                ed += 1
                continue
            edline = max(edline, rattan_info[ed]["source"]["line"])
            ed += 1
        if funcname.startswith("_") or "." in funcname:
            continue
        if funcname in visited.keys():
            continue
        rattan_funcs.append([funcname, rattan_info[cur]["source"]["line"], edline, cur, ed-1])
        visited[funcname] = True
    return rattan_assembly, rattan_funcs
