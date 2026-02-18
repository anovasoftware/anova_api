# debug_speed_test.py
from time import perf_counter

def f(x: int) -> int:
    return x + 1

def main() -> None:
    loops = 5_000_000

    t0 = perf_counter()
    n = 0

    # Do a little progress printing (not too often)
    step = 1_000_000

    for i in range(loops):
        n = f(n)
        if (i + 1) % step == 0:
            elapsed = perf_counter() - t0
            rate = (i + 1) / elapsed if elapsed else 0
            print(f'{i+1:,} loops  elapsed={elapsed:.2f}s  rate={rate:,.0f}/s')

    elapsed = perf_counter() - t0
    print(f'DONE n={n}  loops={loops:,}  elapsed={elapsed:.3f}s  rate={loops/elapsed:,.0f}/s')

if __name__ == '__main__':
    main()
