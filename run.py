# pylint:disable = all
import prettytable
from core.assembly import get_info as get_assembly
from core.gcov import get_info as get_gcov
from core.similarity import jaccard
import colorama

w1 = 0.8


def read(path):
    with open(path, encoding="utf-8", mode="r") as f:
        return f.read()


rattan_assembly, rattan_funcs = get_assembly(read("1.cpp"))
sample_assembly, sample_funcs = get_assembly(read("2.cpp"))
rattan_gcov = get_gcov(read("1.cpp.gcov"))
sample_gcov = get_gcov(read("2.cpp.gcov"))

rect = [[0 for i in range(len(sample_funcs))]
        for i in range(len(rattan_funcs))]


def find_lcsubstr(s1, s2):
    # https://blog.csdn.net/Scofield971031/article/details/89027314
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
    mmax = 0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
    return mmax


for i in range(len(rattan_funcs)):
    for j in range(len(sample_funcs)):
        asm = jaccard(
            (rattan_assembly[rattan_funcs[i][3]:rattan_funcs[i][4]+1]),
            (sample_assembly[sample_funcs[j][3]:sample_funcs[j][4]+1])
        )
        lcs = find_lcsubstr(
            rattan_gcov[rattan_funcs[i][1]:rattan_funcs[i][2]+1],
            sample_gcov[sample_funcs[j][1]:sample_funcs[j][2]+1],
        ) / ((rattan_funcs[i][2]-rattan_funcs[i][1]+1+sample_funcs[j][2]-sample_funcs[j][1]+1)/2)
        rect[i][j] = w1 * lcs + (1-w1) * asm

columns = [""]
for j in range(len(rattan_funcs)):
    columns.append("%d." % (j+1) + str(rattan_funcs[j][0].split("::")[-1]))
table = prettytable.PrettyTable(columns)
for j in range(len(sample_funcs)):
    ans = ["%d." % (j+1) + sample_funcs[j][0]]
    for i in range(len(rattan_funcs)):
        s = "%.2f%%" % (rect[i][j] * 100)
        d = rect[i][j] * 100
        if d >= 20 and d <= 30:
            s = colorama.Fore.GREEN + s + colorama.Fore.RESET
        elif d > 30 and d <= 50:
            s = colorama.Fore.YELLOW + s + colorama.Fore.RESET
        elif d > 50:
            s = colorama.Fore.RED + s + colorama.Fore.RESET
        else:
            s = colorama.Fore.BLUE + s + colorama.Fore.RESET
        ans.append(s)
    table.add_row(ans)
print(table)
