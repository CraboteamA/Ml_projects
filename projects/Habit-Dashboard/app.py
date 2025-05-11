from flask import Flask, render_template, request, redirect, jsonify
from models import SessionLocal, DailyEntry
from datetime import date, datetime
from utils import df_from_db, rolling_metrics, current_streak

app = Flask(__name__)

NUM_FLOATS = {"sleep_hours", "weight_kg"}
NUM_INTS   = {"mood", "workouts_min", "code_min"}


@app.route("/", methods=["GET", "POST"])
def index():
    db = SessionLocal()
    if request.method == "POST":
        raw = request.form
     # ---------- parse each field ----------
        day_val = raw.get("day") or date.today().isoformat()
        parsed  = {"day": datetime.fromisoformat(day_val).date()}

        for k in NUM_FLOATS:
            v = raw.get(k)
            parsed[k] = float(v) if v else None

        for k in NUM_INTS:
            v = raw.get(k)
            parsed[k] = int(v) if v else None

        # ---------- upsert ----------
        entry = DailyEntry(**parsed)
        db.merge(entry)   # unique on 'day' => update if exists
        db.commit()
        return redirect("/")
    
    df = df_from_db(db)
    day_q = request.args.get("day")    # comes from ?day=YYYY‑MM‑DD (History → Edit)
    
    if day_q:
        last_row = (
            df.loc[[day_q]].to_dict("records")[0]     # pre‑fill with that date
            if day_q in df.index else {}
        )
    else:
        last_row = df.tail(1).to_dict("records")[0] if not df.empty else {}

    roll = rolling_metrics(df)
    streaks = {
        "workouts": current_streak(df["workouts_min"].fillna(0)),
        "code"    : current_streak(df["code_min"].fillna(0))
    }
    return render_template("index.html",
                           last_row=last_row,
                           streaks=streaks,
                           roll_json=roll.tail(30).reset_index().to_json(orient="records"))

@app.route("/api/data")
def api_data():
    db   = SessionLocal()

    df   = df_from_db(db)            # keep DatetimeIndex
    roll = rolling_metrics(df)       # OK now

    # convert to plain records *after* calculations
    return jsonify({
        "all":  df.reset_index().to_dict(orient="records"),
        "roll": roll.reset_index().to_dict(orient="records")
    })

@app.route("/history")
def history():
    db   = SessionLocal()
    rows = df_from_db(db).reset_index().to_dict(orient="records")
    return render_template("history.html", rows=rows)


@app.route("/charts")
def charts():
    db  = SessionLocal()
    df  = df_from_db(db)
    roll = rolling_metrics(df).reset_index()
    return render_template(
        "charts.html",
        roll_json=roll.to_json(orient="records"),
        all_json=df.reset_index().to_json(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)
