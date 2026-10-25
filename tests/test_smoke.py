#!/usr/bin/env python3
"""skill-finder-zh 离线冒烟测试：不依赖 GitHub / skills.sh 是否可用。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPT = os.path.join(ROOT, "scripts", "find.py")
PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("  PASS " if cond else "  FAIL ") + name + ((" :: " + str(detail)[:300]) if detail and not cond else ""))


def main():
    py = sys.executable

    r = subprocess.run([py, SCRIPT, "--help"], capture_output=True, encoding="utf-8",
                       errors="replace", timeout=60, cwd=ROOT)
    check("--help exit=0", r.returncode == 0, r.stderr)
    check("--help 含 usage", "usage" in (r.stdout or "").lower(), r.stdout[:200])

    r = subprocess.run([py, "-m", "py_compile", SCRIPT], capture_output=True, encoding="utf-8")
    check("find.py 可编译", r.returncode == 0, r.stderr)

    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    try:
        import find
    except Exception as exc:  # noqa: BLE001
        check("可 import find 模块", False, repr(exc))
        print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
        return 1
    check("可 import find 模块", True)

    base = {"name": "a/b", "description": "", "updated": "", "source": "github", "stars": 10,
            "url": "https://github.com/a/b"}
    no_url = {"name": "x", "description": "", "updated": "", "source": "skills.sh", "stars": 0,
              "installs": 100, "url": ""}
    sh_same = {"name": "a/b", "description": "", "updated": "", "source": "skills.sh", "stars": 0,
               "installs": 50, "url": "https://github.com/a/b"}
    merged = find.aggregate([[dict(base)], [dict(no_url)], [dict(sh_same)]])

    check("空 URL 条目被丢弃", len(merged) == 1, [m.get("url") for m in merged])
    check("同 URL 跨源合并且命中去重", merged[0]["cross_source_hits"] == 2, merged[0])
    check("installs 不被当成 star 排序", merged[0]["stars"] == 10, merged[0])

    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        find.print_results("t", [merged[0]], 1)
    out = buf.getvalue()
    check("输出含 npx skills add", "npx skills add a/b" in out, out[:200])
    check("输出不再出现 mavis", "mavis" not in out.lower(), out[:200])

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
