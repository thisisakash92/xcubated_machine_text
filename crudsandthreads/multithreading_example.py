import multiprocessing
import random


def add_two_numbers(i, return_dict):
    """
    worker function
    """
    total = random.random() + random.random()
    return_dict[i + 1] = total
    return total


def start_multiprocessing():
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    process_count = 52
    for i in range(process_count):
        p = multiprocessing.Process(target=add_two_numbers, args=(i, return_dict))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()
    assert len(return_dict.keys()) == process_count
    return return_dict.copy()


if __name__ == '__main__':
    data = start_multiprocessing()
    print(data)
