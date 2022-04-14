import pi2go
import time

def main():
    pi2go.init()
    start = time.time()
    pi2go.go(20, 0)

    time.sleep(0.0005)

    while not pi2go.irCentre():
        pass
    pi2go.go(0, 0)
    print("Wall detected")

    end = time.time()
    print(f"Elapsed time: {end - start}")

    pi2go.cleanup()

if __name__ == '__main__':
    main()