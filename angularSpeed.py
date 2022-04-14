import pi2go
import time

def main():
    pi2go.init()
    start = time.time()
    pi2go.go(20, 0)
    while not pi2go.irCentre():
        print("Waiting...")
    print("Wall detected")
    end = time.time()
    print(f"Elapsed time: {end - start}")

if __name__ == '__main__':
    main()