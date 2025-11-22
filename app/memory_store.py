MEMORY_STORE = {}

def get_memory(jd_name: str):
    return MEMORY_STORE.get(jd_name)

def update_memory(jd_name: str, best_record: dict, history_record: dict):
    if jd_name not in MEMORY_STORE:
        MEMORY_STORE[jd_name] = {
            "best": best_record,
            "history": [history_record]
        }
    else:
        MEMORY_STORE[jd_name]["best"] = best_record
        MEMORY_STORE[jd_name]["history"].append(history_record)

def add_history(jd_name: str, record: dict):
    if jd_name not in MEMORY_STORE:
        MEMORY_STORE[jd_name] = {"best": None, "history": []}
    MEMORY_STORE[jd_name]["history"].append(record)
