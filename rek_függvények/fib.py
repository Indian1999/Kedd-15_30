import time

def fib(n):
    if n < 1:
        return "ERROR"
    elif n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
    
#print(fib(100))

#memoization: A korábban kiszámolt függvény értékeket elmentjük
def fib_memo(n):
    memo = {1: 1, 2: 1}
    def f(n):
        if n in memo.keys():
            return memo[n]
        result = f(n-1) + f(n-2)
        memo[n] = result
        return result
    return f(n)

from functools import cache

@cache
def fib_cache(n):
    if n < 1:
        return "ERROR"
    elif n == 1 or n == 2:
        return 1
    else:
        return fib_cache(n-1) + fib_cache(n-2)

start = time.perf_counter()
print("Sima fib(30) =", fib(30))
end = time.perf_counter()
print("Eltelt idő:", end-start)

start = time.perf_counter()
print("fib_memo(30) =", fib_memo(30))
end = time.perf_counter()
print("Eltelt idő:", end-start)

start = time.perf_counter()
print("fib_cache(30) =", fib_cache(30))
end = time.perf_counter()
print("Eltelt idő:", end-start)