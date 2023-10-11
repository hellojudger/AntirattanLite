#include <bits/stdc++.h>
#define res register int
#define maxn 500010
using namespace std;
void read(int &x)
{
    int f = 1;
    x = 0;
    char ch = getchar();
    while (ch < '0' || ch > '9')
    {
        if (ch == '-')
            f = -1;
        ch = getchar();
    }
    while (ch >= '0' && ch <= '9')
    {
        x = x * 10 + ch - '0';
        ch = getchar();
    }
    x *= f;
}
struct node
{
    int to, nxt;
};
node edge[maxn << 1], edge2[maxn << 1];
int indegree[maxn], dad[maxn];
int head[maxn], head2[maxn], m, n, root, dep[maxn], fa[maxn][30], num, sum, siz[maxn], topo[maxn];
void add1(int a, int b)
{
    edge[++num].to = b;
    edge[num].nxt = head[a];
    head[a] = num;
    indegree[b]++;
}
void add2(int a, int b)
{
    edge2[++num].to = b;
    edge2[num].nxt = head2[a];
    head2[a] = num;
}
int lca(int u, int v)
{
    if (dep[u] < dep[v])
        swap(u, v);
    for (res i = 20; i >= 0; --i)
        if (dep[fa[u][i]] >= dep[v])
            u = fa[u][i];
    if (u == v)
        return u;
    for (res i = 20; i >= 0; --i)
        if (fa[u][i] != fa[v][i])
            u = fa[u][i], v = fa[v][i];
    return fa[u][0];
}
void get_siz(int x)
{ //求子树大小
    for (res i = head2[x]; i != -1; i = edge2[i].nxt)
    {
        int y = edge2[i].to;
        get_siz(y);
        siz[x] += siz[y];
    }
}
void topsort()
{
    memset(dad, -1, sizeof(dad));
    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (!indegree[i])
            q.push(i), dad[i] = 0;
    while (!q.empty())
    {
        int temp = q.front();
        q.pop();
        add2(dad[temp], temp);
        dep[temp] = dep[dad[temp]] + 1;
        fa[temp][0] = dad[temp];
        for (int i = 1; i <= 16; i++)
            fa[temp][i] = fa[fa[temp][i - 1]][i - 1];
        for (int p = head[temp]; p != -1; p = edge[p].nxt)
        {
            int v = edge[p].to;
            if (dad[v] == -1)
                dad[v] = temp;
            else
                dad[v] = lca(dad[v], temp);
            indegree[v]--;
            if (!indegree[v])
                q.push(v);
        }
    }
}
int main()
{
    read(n);
    memset(head, -1, sizeof(head));
    memset(indegree, 0, sizeof(indegree));
    for (int i = 1, x; i <= n; i++)
    { //节点数
        while (1)
        {
            read(x);
            if (!x)
                break;
            add1(x, i);
        }
    }
    siz[0] = dep[0] = 0;
    memset(head2, -1, sizeof(head2));
    topsort();
    get_siz(0);
    for (int i = 1; i <= n; i++)
        printf("%d\n", siz[i] - 1);
    return 0;
}