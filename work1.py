import struct
INPUT_TXT  = "random_numbers.txt"  
OUTPUT_BIN = "random_numbers.bin"        
with open(INPUT_TXT, "r", encoding="utf-8") as f_txt, \
     open(OUTPUT_BIN, "wb") as f_bin:
    for line in f_txt:
        line = line.strip()
        if not line:
            continue
        num = int(line)
        f_bin.write(struct.pack("<I", num))
print("Преобразовать в двоичный файл с 32-битными целыми числами стандартного формата")

import struct
import threading
import os

INPUT_FILE ='random_numbers.bin'
CHUNK_SIZE = 5000000   
INT_SIZE = 4        
lock = threading.Lock()
current_chunk = 0   
sorted_chunks=[]
outputpath='output'
os.makedirs(outputpath,exist_ok=True)
def process_chunk(chunk_num, total_numbers):
   
    start_idx =chunk_num* CHUNK_SIZE
    offset = start_idx * INT_SIZE
    remaining = total_numbers - start_idx
    if remaining <= 0:
        return
    current_read = min(CHUNK_SIZE, remaining) 


    with open(INPUT_FILE, "rb") as f:
        f.seek(offset)
        data = f.read(current_read * INT_SIZE)
    numbers = list(struct.unpack(f"<{current_read}I", data))
    numbers.sort()
    tmp_path = os.path.join(outputpath, f"chunk_{chunk_num}.txt")
    with open(tmp_path, "w", encoding="utf-8") as fw:
        fw.write("\n".join(map(str, numbers)))

def worker(total_numbers, total_chunks):
    global current_chunk
    while True:
        with lock:
            if current_chunk > total_chunks:
                break
            my_chunk = current_chunk
            current_chunk += 1

        process_chunk(my_chunk, total_numbers)

if __name__ == "__main__":
    file_size = os.path.getsize(INPUT_FILE)
    total_numbers = file_size // INT_SIZE      
    total_chunks = (total_numbers + CHUNK_SIZE - 1) // CHUNK_SIZE  

    print(f"Общее количество：{total_numbers}")
    print(f"Количество групп：{total_chunks}")

    t1 = threading.Thread(target=worker, args=(total_numbers, total_chunks), name="0")
    t2 = threading.Thread(target=worker, args=(total_numbers, total_chunks), name="1")
    t3 = threading.Thread(target=worker, args=(total_numbers, total_chunks), name="2")
    t4 = threading.Thread(target=worker, args=(total_numbers, total_chunks), name="3")
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print("\n Все группы обработаны.")
    
    
import heapq

filenames = [f"output/chunk_{i}.txt" for i in range(0,20)]

files = [open(f, 'r', encoding='utf-8') for f in filenames]
heap = []


for i, f in enumerate(files):
    line = f.readline()
    if line:
        num = int(line.strip())  
        heapq.heappush(heap, (num, i))


with open("sorted_output.txt", "w", encoding='utf-8') as out:
    while heap:
        num, idx = heapq.heappop(heap)
        out.write(f"{num}\n")

        next_line = files[idx].readline()
        if next_line:
            next_num = int(next_line.strip()) 
            heapq.heappush(heap, (next_num, idx))

for f in files:
    f.close()

print("Сортировка завершена.")
