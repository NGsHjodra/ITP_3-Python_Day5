# import libraries
import numpy as np
import time
import threading
import multiprocessing
import asyncio
import io

def mult_matrices_numpy(A, B):
    return A @ B


def mult_matrices_loops(A, B):
    n = A.shape[0]
    m = B.shape[0]
    C = np.zeros((n, m))

    for i in range(n):
        for j in range(m):
            for k in range(m):
                C[i, j] += A[i, k] * B[k, j]

    return C
    
def mult_matrices_threads(A, B):
    n = A.shape[0]
    m = B.shape[0]
    C = np.zeros((n, m))

    num_cores = threading.active_count()
    threads = []
    for i in range(num_cores):
        t = threading.Thread(target=mult_matrices_loops, args=(A[i * n // num_cores:(i + 1) * n // num_cores], B))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return C
            
def mult_matrices_multiprocessing(A, B):
    n = A.shape[0]
    m = B.shape[0]
    C = np.zeros((n, m))

    num_cores = multiprocessing.cpu_count()
    k = 8
    pool = multiprocessing.Pool(num_cores)
    res = pool.starmap(mult_matrices_loops, [(A[i * n // k:(i + 1) * n // k], B) for i in range(k)])
    
    for i in range(k):
        C[i * n // k:(i + 1) * n // k] = res[i]

    return C

async def mult_matrices_asyncio(A, B):
    n = A.shape[0]
    m = B.shape[0]
    C = np.zeros((n, m))

    num_cores = multiprocessing.cpu_count()
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, mult_matrices_loops, A[i * n // num_cores:(i + 1) * n // num_cores], B) for i in range(num_cores)]
    res = await asyncio.gather(*tasks)

    for i in range(num_cores):
        C[i * n // num_cores:(i + 1) * n // num_cores] = res[i]

    return C

async def mult_matrices_subprocess(A, B):
    n = A.shape[0]

    proc = await asyncio.create_subprocess_shell("cpp_matmult\\cmake-build-debug\\cpp_matmult.exe",
                                                stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    
    stringwriter = io.StringIO()

    stringwriter.write(f"{n} {n}\n")
    for i in range(n):
        stringwriter.write(' '.join([str(x) for x in A[i, :]]))
        stringwriter.write("\n")

    stringwriter.write(f"{n} {n}\n")
    for i in range(n):
        stringwriter.write(' '.join([str(x) for x in B[i, :]]))
        stringwriter.write("\n")

    stdout, stderr = await proc.communicate(stringwriter.getvalue().encode())
    
    if stdout:
        C = np.zeros((n, n))
        stringreader = io.StringIO(stdout.decode())
        for i in range(n):
            C[i, :] = [int(x) for x in stringreader.readline().split(' ')]
        return C
   

# main
if __name__ == "__main__":
    # large matrix
    # a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    N = 8
    a = np.random.randint(0, 10, (N, N))
    b = np.random.randint(0, 10, (N, N))
    

    start = time.time()
    c = mult_matrices_numpy(a, b)
    end = time.time()
    print("Numpy:", end - start)
    print(c)

    # start = time.time()
    # c = mult_matrices_loops(a, b)
    # end = time.time()
    # print("Loops:", end - start)
    # print(c)

    # start = time.time()
    # c = mult_matrices_threads(a, b)
    # end = time.time()
    # print("Threads:", end - start)
    # print(c)

    start = time.time()
    c = mult_matrices_multiprocessing(a, b)
    end = time.time()
    print("Multiprocessing:", end - start)
    print(c)

    # start = time.time()
    # c = asyncio.run(mult_matrices_asyncio(a, b))
    # end = time.time()
    # print("Asyncio:", end - start)
    # print(c)

    start = time.time()
    c = asyncio.run(mult_matrices_subprocess(a, b))
    end = time.time()
    print("Subprocess:", end - start)
    print(c)