# pylint: skip-file
import streamlit as st
from streamlit_ace import st_ace
from core.assembly import get_info as get_assembly
from core.gcov import get_info as get_gcov
from core.similarity import jaccard
from os import system
import pandas as pd

st.header("Antirattan Lite Online Demo / 反藤甲在线体验")
st.subheader("Rattan / 题解代码")
rattan = st_ace(language="c_cpp", auto_update=True, key="rattan")
st.subheader("Sample / 待检测代码")
sample = st_ace(language="c_cpp", auto_update=True, key="sample")
st.subheader("Input Data / 输入数据")
input_data = st_ace(auto_update=True, key="input_data")


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


w1 = 0.8


def read(path):
    with open(path, encoding="utf-8", mode="r") as f:
        return f.read()


def run():
    with open("1.cpp", "w", encoding="utf-8") as f:
        f.write(str(rattan))
    with open("2.cpp", "w", encoding="utf-8") as f:
        f.write(str(sample))
    with open("1.in", "w", encoding="utf-8") as f:
        f.write(str(input_data))
    with st.spinner("Waiting to compile,run,analysis and calculating similarity..."):
        code = system(
            "g++ -O3 -w 1.cpp -o 1.exe -fprofile-arcs -ftest-coverage")
        if code != 0:
            st.error("Compiled unsuccessfully.")
            return
        code = system(
            "g++ -O3 -w 2.cpp -o 2.exe -fprofile-arcs -ftest-coverage")
        if code != 0:
            st.error("Compiled unsuccessfully.")
            return
        code = system("./1.exe < 1.in > 1.out")
        if code != 0:
            st.error("Run unsuccessfully.")
            return
        code = system("./2.exe < 1.in > 2.out")
        if code != 0:
            st.error("Run unsuccessfully.")
            return
        code = system("gcov 1.cpp > 1.log")
        if code != 0:
            st.error("Analysis unsuccessfully.")
            return
        code = system("gcov 2.cpp > 2.log")
        if code != 0:
            st.error("Analysis unsuccessfully.")
            return
        rattan_assembly, rattan_funcs = get_assembly(read("1.cpp"))
        sample_assembly, sample_funcs = get_assembly(read("2.cpp"))
        rattan_gcov = get_gcov(read("1.cpp.gcov"))
        sample_gcov = get_gcov(read("2.cpp.gcov"))

        rect = [["" for i in range(len(sample_funcs) + 1)]
                for i in range(len(rattan_funcs))]
        progress = st.progress(0.0)
        step = 1 / (len(rattan_funcs) * len(sample_funcs))
        all_step = 0
        for i in range(len(rattan_funcs)):
            rect[i][0] = rattan_funcs[i][0]
            for j in range(len(sample_funcs)):
                asm = jaccard(
                    (rattan_assembly[rattan_funcs[i][3]:rattan_funcs[i][4]+1]),
                    (sample_assembly[sample_funcs[j][3]:sample_funcs[j][4]+1])
                )
                lcs = find_lcsubstr(
                    rattan_gcov[rattan_funcs[i][1]:rattan_funcs[i][2]+1],
                    sample_gcov[sample_funcs[j][1]:sample_funcs[j][2]+1],
                ) / ((rattan_funcs[i][2]-rattan_funcs[i][1]+1+sample_funcs[j][2]-sample_funcs[j][1]+1)/2)
                rect[i][j + 1] = "%.2f%%" % ((w1 * lcs + (1-w1) * asm) * 100)
                all_step += step
                progress.progress(all_step, "Calculated similarity between %s and %s" % (
                    rattan_funcs[i][0], sample_funcs[j][0]))
        columns = [""]
        for j in range(len(sample_funcs)):
            columns.append(str(sample_funcs[j][0].split("::")[-1]))
        dataframe = pd.DataFrame(rect, columns=columns)
        st.dataframe(dataframe)
        system("python3 clean.py")


check_btn = st.button("Check / 检测", on_click=run)
