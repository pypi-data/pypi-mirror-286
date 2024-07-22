#### pkgsize

CLI for finding size of Python libraries on PyPi, and comparing size with other libraries.

---

Useful for keeping dependencies lightweight in Python projects.

---

Example usage:

```
C:\>pkgsize https://pypi.org/project/sanic/

Size of https://pypi.org/project/sanic/: 17.62 MB
```

```
C:\>pkgsize https://pypi.org/project/Eel/ https://pypi.org/project/pywebview/

Size of https://pypi.org/project/Eel/: 0.52 MB
Size of https://pypi.org/project/pywebview/: 278.48 MB

----------------------------
Size difference: 277.96 MB
----------------------------
```
