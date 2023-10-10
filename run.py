import requests
import difflib
import prettytable

session = requests.session()
arguments = {
    "source": "",
    "compiler": "g132",
    "options": {
        "userArguments": "-O2 -w",
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

def read(path):
    with open(path, encoding="utf-8", mode="r") as f:
        return f.read()

rattan = read("1.cpp")
sample = read("2.cpp")
arguments["source"] = rattan
rattan_info = session.post(url, json=arguments, headers=header).json()["asm"]
arguments["source"] = sample
sample_info = session.post(url, json=arguments, headers=header).json()["asm"]

rattan_funcs = []
rattan_assembly = list(map(lambda x:x["text"], rattan_info))
pos = -1

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
    rattan_funcs.append([funcname, rattan_info[cur]["source"]["line"], edline, cur, ed-1])

sample_funcs = []
sample_assembly = list(map(lambda x:x["text"], sample_info))
pos = -1

for line in sample_info:
    pos += 1
    text = str(line["text"])
    if text.startswith(".") or text.startswith(" ") or text.startswith("\t") or text.startswith("\n"):
        continue
    if len(text.strip().rstrip()) == 0:
        continue
    if pos == len(sample_info) - 1:
        continue
    if str(sample_info[pos+1]["text"]).strip().rstrip().startswith(".zero"):
        continue
    if str(sample_info[pos+1]["text"]).strip().rstrip().startswith(".quad"):
        continue
    funcname = text.split('(')[0]
    cur = pos + 1
    while True:
        if sample_info[cur]["source"] is not None:
            break
        cur += 1
    ed = cur
    edline = int(-pow(10, 18))
    while True:
        if sample_info[ed]["text"].startswith("."):
            ed += 1
            continue
        if sample_info[ed]["source"] is None:
            break
        if sample_info[ed]["source"]["file"] is not None:
            ed += 1
            continue
        edline = max(edline, sample_info[ed]["source"]["line"])
        ed += 1
    if funcname.startswith("_") or "." in funcname:
        continue
    sample_funcs.append([funcname, sample_info[cur]["source"]["line"], edline, cur, ed-1])

rect = [[0 for i in range(len(sample_funcs))] for i in range(len(rattan_funcs))]

with open("1.cpp.gcov", "r", encoding="utf-8") as f:
    rattan_gcov = f.read()
rattan_gcov = list(map(lambda x : (x.split(':')[0].strip().rstrip()), rattan_gcov.splitlines()))[5:]

with open("2.cpp.gcov", "r", encoding="utf-8") as f:
    sample_gcov = f.read()

sample_gcov = list(map(lambda x : (x.split(':')[0].strip().rstrip()), sample_gcov.splitlines()))[5:]

def find_lcsubstr(s1, s2):
    # https://blog.csdn.net/Scofield971031/article/details/89027314
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]: # 如果相等，则加入现有的公共子串
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return mmax  # 返回最长子串及其长度

w1 = 0.8

for i in range(len(rattan_funcs)):
    for j in range(len(sample_funcs)):
        asm = difflib.SequenceMatcher(None, 
            "\n".join(rattan_assembly[rattan_funcs[i][3]:rattan_funcs[i][4]+1]),
            "\n".join(sample_assembly[sample_funcs[j][3]:sample_funcs[j][4]+1])
        ).ratio()
        # print(rattan_gcov[rattan_funcs[i][1]:rattan_funcs[i][2]+1], sample_gcov[sample_funcs[i][1]:sample_funcs[i][2]+1])
        lcs = find_lcsubstr(
            rattan_gcov[rattan_funcs[i][1]:rattan_funcs[i][2]+1],
            sample_gcov[sample_funcs[j][1]:sample_funcs[j][2]+1],
        ) / ((rattan_funcs[i][2]-rattan_funcs[i][1]+1+sample_funcs[j][2]-sample_funcs[j][1]+1)/2)
        rect[i][j] = w1 * lcs + (1-w1) * asm

columns = [""]
for j in range(len(rattan_funcs)):
    columns.append("%d." % (j+1) +  str(rattan_funcs[j][0].split("::")[-1]))
table = prettytable.PrettyTable(columns)
for j in range(len(sample_funcs)):
    ans = ["%d." % (j+1) + sample_funcs[j][0]]
    for i in range(len(rattan_funcs)):
        ans.append("%.2f%%" % (rect[i][j] * 100))
    table.add_row(ans)
print(table)
