import time
from multiprocessing import Pool
from library import download_video
from library import read_video_urls

if __name__ == "__main__":
    urls = read_video_urls("data/video_urls.csv")

    start = time.perf_counter()
    with Pool() as pool:
        results = pool.map(download_video, urls)
    end = time.perf_counter()
    parallel_time = round(end - start, 2)
    print(f"Parallel execution: {parallel_time}")

    with open("reports/sequential_report.md", "a") as report:
        report.write("\n## Parallel execution\n\n")
        report.write(f"Total time: {parallel_time} seconds\n\n")
        report.write("## Comparison\n\n")
        speed_improvement = round((6.3 - parallel_time) / 6.3 * 100, 1)
        report.write(f"Speed improvement: {speed_improvement}%\n")