#include <bits/stdc++.h>
#define int long long
using namespace std;

const int N = 65535;
struct edge
{
    int nxt, to;
} g[N << 1];
int head[N], ec;
void add(int u, int v)
{
    g[++ec].nxt = head[u];
    g[ec].to = v;
    head[u] = ec;
}

int in[N], n, pre[N], dep[N], fa[N][35];
vector<int> tree[N];

int lca(int u, int v)
{
    if (dep[u] < dep[v])
        swap(u, v);
    for (int i = 30; ~i; i--)
    {
        if (dep[fa[u][i]] >= dep[v])
            u = fa[u][i];
    }
    if (u == v)
        return u;
    for (int i = 30; ~i; i--)
    {
        if (fa[u][i] != fa[v][i])
            u = fa[u][i], v = fa[v][i];
    }
    return fa[u][0];
}

void dominator()
{
    for (int i = 1; i <= n; i++)
    {
        for (int j = head[i]; j; j = g[j].nxt)
            in[g[j].to]++;
    }
    queue<int> q;
    for (int i = 1; i <= n; i++)
    {
        if (!in[i])
            q.push(i), pre[i] = 0;
        else
            pre[i] = -1;
    }
    while (!q.empty())
    {
        int u = q.front();
        q.pop();
        tree[pre[u]].push_back(u);
        dep[u] = dep[pre[u]] + 1;
        fa[u][0] = pre[u];
        for (int i = 1; i <= 30; i++)
            fa[u][i] = fa[fa[u][i - 1]][i - 1];
        for (int j = head[u]; j; j = g[j].nxt)
        {
            int v = g[j].to;
            in[v]--;
            if (pre[v] == -1)
                pre[v] = u;
            else
                pre[v] = lca(pre[v], u);
            if (!in[v])
                q.push(v);
        }
    }
}

int siz[N];
void dfs(int u)
{
    siz[u] = 1;
    for (int v : tree[u])
    {
        dfs(v);
        siz[u] += siz[v];
    }
}

signed main()
{
    cin >> n;
    for (int i = 1; i <= n; i++)
    {
        int x;
        while (cin >> x && x)
            add(x, i);
    }
    dominator();
    dfs(0);
    for (int i = 1; i <= n; i++)
        cout << (siz[i] - 1) << "\n";
    return 0;
}