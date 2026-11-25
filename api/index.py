"""Research Navigator API (Flask, SQLite in-memory, pure-Python TF-IDF + cosine). Vercel entry point: `app`."""
import math, re, sqlite3
from collections import Counter
from flask import Flask, jsonify, request
from data import PAPERS, TOPICS, OPPORTUNITIES

app = Flask(__name__)

# ---------- database: in-memory SQLite, seeded on every cold start (Vercel disk is read-only) ----------
_c = sqlite3.connect(":memory:", check_same_thread=False)
_c.row_factory = sqlite3.Row
_c.executescript("""
CREATE TABLE papers(id INTEGER PRIMARY KEY, title, authors, year INT, method, kind, keywords, abstract, url);
CREATE TABLE topics(id INTEGER PRIMARY KEY, branch, title, keywords, skills, level);
CREATE TABLE opportunities(id INTEGER PRIMARY KEY, name, kind, eligibility, deadline, support, url, verified INT);""")
_c.executemany("INSERT INTO papers(title,authors,year,method,kind,keywords,abstract,url) VALUES(?,?,?,?,?,?,?,?)", PAPERS)
_c.executemany("INSERT INTO topics(branch,title,keywords,skills,level) VALUES(?,?,?,?,?)", TOPICS)
_c.executemany("INSERT INTO opportunities(name,kind,eligibility,deadline,support,url,verified) VALUES(?,?,?,?,?,?,?)", OPPORTUNITIES)
_c.commit()
q_all = lambda sql: [dict(r) for r in _c.execute(sql).fetchall()]

# ---------- AI layer: TF-IDF + cosine similarity (no heavy libraries -> small, fast serverless bundle) ----------
STOP = set("a an the of and or to in on for with is are be by as at it this that from using use based its their we our can not does do".split())
def tok(t): return [w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP and len(w) > 1]

def vectors(texts):
    toks = [tok(t) for t in texts]; n = len(toks); df = Counter(w for t in toks for w in set(t))
    idf = {w: math.log((1 + n) / (1 + d)) + 1 for w, d in df.items()}
    out = []
    for t in toks:
        v = {w: c * idf[w] for w, c in Counter(t).items()}; norm = math.sqrt(sum(x * x for x in v.values())) or 1
        out.append({w: x / norm for w, x in v.items()})
    return out

def cos(a, b): return sum(x * b.get(w, 0) for w, x in a.items())

def rank(query, docs, n=5):
    """Return [(index, score)] best first; only positive scores."""
    if not docs or not query.strip(): return []
    vs = vectors(docs + [query]); q = vs[-1]
    r = sorted(((i, cos(q, vs[i])) for i in range(len(docs))), key=lambda x: -x[1])
    return [(i, s) for i, s in r[:n] if s > 0]

def sentences(t): return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if len(s.strip()) > 15]

CUES = {"problem": r"\b(problem|aim|goal|challenge|propose|address|objective)\b",
        "method": r"\b(method|model|approach|algorithm|architecture|framework|using|based on|trained)\b",
        "dataset": r"\b(dataset|corpus|data set|benchmark|samples|collected)\b",
        "results": r"\b(result|achiev|outperform|improv|show[s]? that|obtain)\w*",
        "metrics": r"\b(accuracy|f1|precision|recall|bleu|rouge|auc|rmse|mae|score)\b",
        "limitations": r"\b(limitation|however|but|does not|do not|only|lack|fail|future work|cannot|not designed)\b"}

def understand(text):
    out = {k: [] for k in CUES}; ss = sentences(text)
    for s in ss:
        for k, p in CUES.items():
            if re.search(p, s, re.I): out[k].append(s)
    out["summary"] = " ".join(ss[:2]); return out

# ---------- routes ----------
@app.post("/api/topics")
def topics():
    d = request.get_json(silent=True) or {}; rows = q_all("SELECT * FROM topics")
    res = rank(f"{d.get('interest','')} {d.get('branch','')}", [f"{r['title']} {r['keywords']} {r['branch']}" for r in rows])
    return jsonify([{**rows[i], "score": round(s, 3), "fits_level": rows[i]["level"] == d.get("level")} for i, s in res])

@app.get("/api/papers")
def papers():
    yr = request.args.get("year", type=int)
    rows = [r for r in q_all("SELECT * FROM papers") if not yr or r["year"] >= yr]
    res = rank(request.args.get("q", ""), [f"{r['title']} {r['keywords']} {r['abstract']}" for r in rows], 10)
    out = [{**rows[i], "score": round(s, 3)} for i, s in res]
    return jsonify(sorted(out, key=lambda p: (p["kind"] != "review", -p["score"])))  # review papers first

@app.post("/api/understand")
def api_understand(): return jsonify(understand((request.get_json(silent=True) or {}).get("text", "")))

@app.post("/api/gaps")
def gaps():
    ids = (request.get_json(silent=True) or {}).get("ids", [])
    rows = [r for r in q_all("SELECT * FROM papers") if r["id"] in ids]
    lims = [(r["title"], s) for r in rows for s in understand(r["abstract"])["limitations"]]
    groups, seen = [], set()
    if len(lims) > 1:
        vs = vectors([l[1] for l in lims])
        for i in range(len(lims)):
            if i in seen: continue
            g = [j for j in range(len(lims)) if cos(vs[i], vs[j]) > 0.25 and j not in seen]
            if len(g) > 1: seen.update(g); groups.append({"theme": lims[i][1], "papers": sorted({lims[j][0] for j in g})})
    methods = sorted({r["method"] for r in rows}); kws = sorted({k for r in rows for k in r["keywords"].split()})
    return jsonify({"limitations": [{"paper": a, "text": b} for a, b in lims], "repeated": groups,
        "unexplored": [f"{m} + {k}" for m in methods for k in kws[:6] if not any(m in r["method"] and k in r["keywords"] for r in rows)][:8],
        "note": "AI only suggests a gap. Student and guide must verify novelty from the original papers."})

@app.get("/api/opportunities")
def opps(): return jsonify(q_all("SELECT * FROM opportunities"))

@app.get("/api/ethics")
def ethics():
    return jsonify({"do": ["Cite every source you use", "Verify claims in the original paper", "Keep data and code reproducible", "Get faculty guide approval", "Respect privacy and consent"],
        "dont": ["Copy text or figures without credit", "Fabricate or tweak data", "Rely on AI summaries without reading the paper", "Share personal data of participants", "Submit the same work twice"],
        "resources": [{"name": "How to Read a Paper (S. Keshav)", "url": "https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf"}, {"name": "NPTEL", "url": "https://nptel.ac.in"}]})

@app.post("/api/roadmap")
def roadmap():
    d = request.get_json(silent=True) or {}; ids = d.get("ids", [])
    rows = [r for r in q_all("SELECT * FROM papers") if r["id"] in ids]
    return jsonify({"topic": d.get("topic", ""), "steps": ["1. Read review/survey papers first", "2. Summarise each paper (problem, method, dataset, metrics, limitations)",
        "3. Shortlist a gap and write a research question", "4. Verify novelty with your faculty guide", "5. Plan experiments, dataset and metrics", "6. Write, cite properly and follow ethics"],
        "sources": [{"title": r["title"], "year": r["year"], "url": r["url"]} for r in rows],
        "validation": ["Sources verified", "Novelty checked", "Ethics reviewed", "Feasibility confirmed by guide"]})

if __name__ == "__main__":  # local run: python api/index.py  (then open public/index.html via a static server, or use `vercel dev`)
    app.run(debug=True)
