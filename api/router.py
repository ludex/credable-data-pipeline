from fastapi import APIRouter, Depends, Query, Request, HTTPException
from api.auth import verify_token
from api.limits import limiter
import pandas as pd
import os
import glob

router = APIRouter()

@router.get("/")
@limiter.limit("100/minute")
async def get_data(
    request: Request,
    dataset: str = Query("FINDEXData"),
    start_date: int = Query(None),
    end_date: int = Query(None),
    cursor: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    token: str = Depends(verify_token)
):
    data_path = f"./processed-data/cleaned-{dataset}"
    try:
        file = glob.glob(os.path.join(data_path, "part-*.csv"))[0]
        df = pd.read_csv(file)
    except IndexError:
        raise HTTPException(status_code=500, detail=f"Cleaned dataset for '{dataset}' not found.")
    
    if "year" not in df.columns:
        raise HTTPException(status_code=500, detail="Dataset missing 'year' column.")

    if start_date:
        df = df[df['year'].astype(str) >= str(start_date)]
    if end_date:
        df = df[df['year'].astype(str) <= str(end_date)]

    df = df.sort_values("year")
    data_page = df.iloc[cursor:cursor+limit]

    return {
        "dataset": dataset,
        "cursor": cursor,
        "next_cursor": cursor + limit if cursor + limit < len(df) else None,
        "records": data_page.to_dict(orient="records")
    }


@router.get("/analytics")
@limiter.limit("100/minute")
async def get_analytics(
    request: Request,
    dataset: str = Query("FINDEXData"),
    token: str = Depends(verify_token)
):
    data_path = f"./processed-data/cleaned-{dataset}"
    try:
        file = glob.glob(os.path.join(data_path, "part-*.csv"))[0]
        df = pd.read_csv(file)
    except IndexError:
        raise HTTPException(status_code=500, detail=f"Cleaned dataset for '{dataset}' not found.")

    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "year_range": sorted(df['year'].dropna().unique().tolist()) if 'year' in df.columns else [],
        "sample_countries": df['country_name'].dropna().unique().tolist()[:5] if 'country_name' in df.columns else []
    }

    return summary

@router.get("/datasets")
@limiter.limit("100/minute")
async def list_datasets(
    request: Request,
    token: str = Depends(verify_token)
):
    base_path = "./processed-data"
    try:
        folders = [
            f.replace("cleaned-", "")
            for f in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, f)) and f.startswith("cleaned-")
        ]
    except Exception:
        raise HTTPException(status_code=500, detail="Could not list datasets.")

    return {"datasets": folders}