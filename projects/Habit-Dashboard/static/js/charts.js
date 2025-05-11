fetch("/api/data")
  .then(r => r.json())
  .then(data => {
    // rolling line
    const dates = data.roll.map(r => r.day);
    Plotly.newPlot("line-roll", [
      {x: dates, y: data.roll.map(r=>r.sleep_hours), name:"Sleep h", mode:"lines"},
      {x: dates, y: data.roll.map(r=>r.weight_kg),  name:"Weight kg", mode:"lines"},
      {x: dates, y: data.roll.map(r=>r.workouts_min), name:"Workout min", mode:"lines"},
      {x: dates, y: data.roll.map(r=>r.code_min), name:"Code min", mode:"lines"}
    ], 
    {
      title:"7‑day rolling averages", 
      template:"plotly_dark",
      paper_bgcolor:"rgba(0,0,0,0)",
      plot_bgcolor:"rgba(0,0,0,0)",
      font:{color:"#f1f3f9"}
    });

    // sleep vs mood scatter
    Plotly.newPlot("scatter-sleep-mood", [{
      x: data.all.map(d=>d.sleep_hours),
      y: data.all.map(d=>d.mood),
      mode:"markers",
      text: data.all.map(d=>d.day)
    }], 
    {
      title:"Sleep vs Mood", 
      template:"plotly_dark",
      xaxis:{title:"Sleep h"},
      yaxis:{title:"Mood"},
      paper_bgcolor:"rgba(0,0,0,0)",
      plot_bgcolor:"rgba(0,0,0,0)",
      font:{color:"#f1f3f9"}
    });

    // mood vs workouts+practice
    const totalActivity = data.all.map(d=>(d.workouts_min||0)+(d.code_min||0));
    Plotly.newPlot("scatter-mood-activity", [{
      x: totalActivity, y: data.all.map(d=>d.mood),
      mode:"markers", text:data.all.map(d=>d.day)
    }], 
    {
      title:"Mood vs Physical+Coding Activity",
      template:"plotly_dark", 
      xaxis:{title:"Total min"}, 
      yaxis:{title:"Mood"},
      paper_bgcolor:"rgba(0,0,0,0)",
      plot_bgcolor:"rgba(0,0,0,0)",
      font:{color:"#f1f3f9"}
    });
});
