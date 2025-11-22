import math
import re
from langchain_community.embeddings import HuggingFaceEmbeddings

EMB = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

def embed_text(text: str):
    if not text:
        return []
    return EMB.embed_query(text)

def cosine_sim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def extract_keywords(text: str, top_n=25):
    tokens = re.findall(r"[A-Za-z+#\.\-]+", text.lower())
    stop = {"the","and","for","with","that","this","from","your","you","have","are","will","his","her","our","a","an","to","in","on","of","by"}
    freq = {}
    for tkn in tokens:
        if len(tkn) < 3: continue
        if tkn in stop: continue
        freq[tkn] = freq.get(tkn,0)+1
    sorted_tokens = sorted(freq.items(), key=lambda x: -x[1])
    return [t for t,_ in sorted_tokens[:top_n]]

def skill_match_score(jd_text: str, resume_text: str):
    jd_keys = set(extract_keywords(jd_text, 40))
    res_keys = set(extract_keywords(resume_text, 80))
    if not jd_keys:
        return 0.0
    over = jd_keys.intersection(res_keys)
    return len(over) / len(jd_keys)

def experience_score(resume_text: str):
    m = re.search(r"(\d{1,2})\s+years?", resume_text.lower())
    if m:
        y = int(m.group(1))
        if y >= 10: return 1.0
        if y >= 5: return 0.8
        if y >= 2: return 0.6
        return 0.4
    if re.search(r"\bsenior\b", resume_text, re.I): return 0.95
    if re.search(r"\bmid[- ]?level\b", resume_text, re.I): return 0.75
    if re.search(r"\bjunior\b|\bentry\b", resume_text, re.I): return 0.35
    return 0.5

def compute_suitability(jd_store, resume_store):
    jd_text = "\n".join(jd_store.get("chunks", [])[:10])
    res_text = "\n".join(resume_store.get("chunks", [])[:20])

    jd_vec = embed_text(jd_text) or []
    res_vec = embed_text(res_text) or []

    sem_sim = cosine_sim(jd_vec, res_vec) if jd_vec and res_vec else 0.0
    skill = skill_match_score(jd_text, res_text)
    exp = experience_score(res_text)

    final = 0.4 * sem_sim + 0.4 * skill + 0.2 * exp
    return {
        "semantic_similarity": round(sem_sim, 4),
        "skill_overlap": round(skill, 4),
        "experience_score": round(exp, 4),
        "suitability_score": round(final * 100, 2)
    }
