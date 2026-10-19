import os, time, json, pprint
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime


FIFO_PATH = "/tmp/therunsync.fifo"

def convert_time(time: str) -> str:
    text = time.strip()
    main, _, frac = text.partition(".")

    fields = main.split(":")

    hours = int(fields[-3]) if len(fields) == 3 else 0
    minutes = int(fields[-2]) if len(fields) >= 2 else 0
    seconds = int(fields[-1])
    frac = frac.ljust(7, "0")

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{frac}"

def convert_date(date: str) -> str:
    dt = datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")
    return dt.strftime("%m/%d/%Y %H:%M:%S")

def elem(tag, text=None, **attrib):
    e = ET.Element(tag, attrib)
    if text is not None:
        e.text = str(text)
    return e

def do_work(path: Path) -> None:
    print("Waiting a lil bit")
    # time.sleep(3)
    print(f"working on {path}")

    with open(path, "r", encoding="utf-8") as f:
        source = json.load(f)
    source_history_path = path.parent / path.stem

    source["history"] = []
    
    for file in sorted(source_history_path.iterdir()):
        if file.is_file():
            with file.open(encoding="utf-8") as f:
                a = json.load(f)
                for item in a:
                    source["history"].append(item)
    
    # pprint.pprint(source)
    prep = {"AttemptHistory": {}, "Segments": {}}
    for item in source["splits"]:
        prep["Segments"][item["id"]] = { "Name": item["title"],
                                        #Icon TBI
                                        "PersonalBest": convert_time(item["best_time"]["real_time"]),
                                        "BestSegmentTime": convert_time(item["best_segment"]["real_time"]),
                                        "SegmentHistory": {}}
    attempt_id = 1
    for item in source["history"]:
        prep["AttemptHistory"][attempt_id] = {"started": convert_date(item["start_time"]),
                                                "ended": convert_date(item["end_time"])}
        if item["reason"] == "FINISHED":
            prep["AttemptHistory"][attempt_id]["FinalTime"] = convert_time(item["final_time"]["real_time"])
        for split in item["splits"]:
            if split["id"] in prep["Segments"]:
                prep["Segments"][split["id"]]["SegmentHistory"][attempt_id] = convert_time(split["segment"]["real_time"])
        attempt_id += 1


    

    run = ET.Element("Run", {"version": "1.7.0"})
    # GameIcon TBI
    run.append(elem("GameName", source["name"]))
    run.append(elem("CategoryName", source["category"]))
    # LayoutPath not needed?
    # Metadata does TheRun support this? We can add this is its supported
    run.append(elem("Offset", source["start_delay"] if "start_delay" in source else "00:00:00")) #Check which way does offset goes in LiveSplit vs. LibreSplit, formatting!
    run.append(elem("AttemptCount", source["attempt_count"]))
    attempthistory = ET.Element("AttemptHistory")
    segments = ET.Element("Segments")
    for id, item in prep["AttemptHistory"].items():
        attempt = ET.Element("Attempt", {"id": str(id),
                                         "started": item["started"],
                                         "isStartedSynced": str(False),
                                         "ended": item["ended"],
                                         "isEndedSynced": str(False)})
        if "FinalTime" in item:
            attempt.append(elem("RealTime", item["FinalTime"]))
        attempthistory.append(attempt)
    for id, item in prep["Segments"].items():
        segment = ET.Element("Segment")
        segment.append(elem("Name", item["Name"]))
        #Icon TBI
        splittimes = ET.Element("SplitTimes")
        pb = ET.Element("SplitTime", {"name": "Personal Best"})
        pb.append(elem("RealTime", item["PersonalBest"]))
        splittimes.append(pb)
        segment.append(splittimes)
        bst = (ET.Element("BestSegmentTime"))
        bst.append(elem("RealTime", item["BestSegmentTime"]))
        segment.append(bst)
        segmenthistory = ET.Element("SegmentHistory")
        for runid, segmenttime in item["SegmentHistory"].items():
            timi = ET.Element("Time", {"id": str(runid)})
            timi.append(elem("RealTime", segmenttime))
            segmenthistory.append(timi)
        segment.append(segmenthistory)
        segments.append(segment)
    run.append(attempthistory)
    run.append(segments)
    tree = ET.ElementTree(run)
    ET.indent(tree, space="  ")
    tree.write("test.lss", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    # try:
    #     os.mkfifo(FIFO_PATH, 0o600)
    # except FileExistsError:
    #     pass

    # while True:
    #     with open(FIFO_PATH) as fifo:
    #         for line in fifo:
    #             path = line.strip()
    #             if path:
    #                 do_work(path)
    #     # all writers closed -> loop and reopen
    # # intentionally not unlinking: a stale FIFO is harmless,
    # # and unlinking on exit would widen the race window for writers
    do_work(Path("/home/tepiloxtl/speedrunning/splits/test.json"))