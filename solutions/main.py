import time
import csv
from multiprocessing import Pool
from library import download_video
from library import read_video_urls
from library import get_video_metadata

if __name__ == "__main__":
    urls = read_video_urls("data/video_urls.csv")

    # serial section - commented out
    # start = time.perf_counter()
    # for url in urls:
    #     download_video(url)
    # end = time.perf_counter()
    # serial_time = round(end - start, 2)
    # print(f"Serial execution: {serial_time}")

    # parallel section
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

    # collect metadata
    metadata_rows = []
    for url in urls:
        metadata = get_video_metadata(url)
        metadata_rows.append(metadata)


    with open("reports/sequential_report.md", "a") as report:
        report.write("\n## Download status\n\n")
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]
        report.write(f"Successful downloads: {len(successful)}\n")
        report.write(f"Failed downloads: {len(failed)}\n")
        for r in failed:
            report.write(f"- {r['url']}: {r['error']}\n")

    # write to CSV
    with open("data/video_metadata.csv", "w", newline="") as file:
        fieldnames = ["title", "duration", "uploader", "view_count", "ext", "url"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_rows)

    print("Metadata saved to data/video_metadata.csv")