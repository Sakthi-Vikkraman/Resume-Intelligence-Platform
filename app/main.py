import os
import tempfile
import shutil

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from app.rag_utils import create_rag_store_from_pdf
from app.scoring import compute_suitability
from app.memory_store import get_memory, update_memory, add_history
from app.schemas import EvaluateResponse, SuitabilityMetrics
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="JD-Resume RAG Evaluator")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OR replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(
    jd_name: str = Form(...),
    jd_file: UploadFile = File(...),
    resume_file: UploadFile = File(...),
    replace_if_better: bool = Form(True)
):
    tmp_dir = tempfile.mkdtemp(prefix="eval_")

    try:
        jd_path = os.path.join(tmp_dir, f"jd_{jd_file.filename}")
        resume_path = os.path.join(tmp_dir, f"resume_{resume_file.filename}")

        with open(jd_path, "wb") as f:
            f.write(await jd_file.read())

        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())

        jd_store = create_rag_store_from_pdf(jd_path)
        resume_store = create_rag_store_from_pdf(resume_path)

        metrics = compute_suitability(jd_store, resume_store)
        score = metrics["suitability_score"]

        memory = get_memory(jd_name)
        prev_best = memory["best"] if memory else None
        verdict = "first_for_jd"
        replaced = False

        if not memory:
            update_memory(
                jd_name,
                best_record={"suitability_score": score, "resume_file": resume_path, "metrics": metrics},
                history_record={"suitability_score": score, "resume_file": resume_path, "metrics": metrics}
            )
            verdict = "stored_as_best"
            replaced = True

        else:
            prev_score = prev_best["suitability_score"]

            if score > prev_score:
                verdict = "better_than_previous"
                if replace_if_better:
                    update_memory(
                        jd_name,
                        best_record={"suitability_score": score, "resume_file": resume_path, "metrics": metrics},
                        history_record={"suitability_score": score, "resume_file": resume_path, "metrics": metrics}
                    )
                    replaced = True
            elif score < prev_score:
                verdict = "worse_than_previous"
                add_history(jd_name, {"suitability_score": score, "resume_file": resume_path, "metrics": metrics})
            else:
                verdict = "same_as_previous"
                add_history(jd_name, {"suitability_score": score, "resume_file": resume_path, "metrics": metrics})

        memory_after = get_memory(jd_name)

        return {
            "jd_name": jd_name,
            "metrics": metrics,
            "verdict": verdict,
            "replaced_best": replaced,
            "previous_best": prev_best,
            "memory_summary": {
                "best_score": memory_after["best"]["suitability_score"],
                "history_count": len(memory_after["history"])
            }
        }

    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        # cleanup only if not storing this file as best
        pass
