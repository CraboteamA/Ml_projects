// ---------- slider builders per algo -----------------
function sliderHTML(id, label, min, max, step, val) {
    return `<label class="form-label">${label}: <span id="${id}-val">${val}</span></label>
            <input type="range" class="form-range" min="${min}" max="${max}"
                   step="${step}" value="${val}" id="${id}">
            <hr>`;
  }
  
  function buildControls(algo){
    let html = "";
    if (algo === "logreg"){
      html += sliderHTML("Cexp","log10(C)",-3,3,0.5,0);
      html += `<div>Penalty:
        <input type="radio" name="penalty" value="l2" checked> L2
        <input type="radio" name="penalty" value="l1"> L1</div>`;
    }
    else if (algo === "svm"){
      html += sliderHTML("Cexp","log10(C)",-3,3,0.5,0);
      html += sliderHTML("gammaexp","log10(gamma)",-4,1,0.5,-1);
    }
    else if (algo === "knn"){
      html += sliderHTML("k","k (neighbors)",1,20,1,5);
    }
    else if (algo === "gb"){
      html += sliderHTML("n_estimators","Trees",50,500,50,100);
      html += sliderHTML("lr","Learning‑rate x1000",1,100,1,10);
      html += sliderHTML("max_depth","Max depth",1,5,1,3);
    }
    $("#dynamic-controls").html(html);             // container div
  }
  
  // ---------- helper to read current params ----------
  function collectHyperParams(algo){
    if (algo === "logreg"){
      return {
        C: Math.pow(10, parseFloat($("#Cexp").val())),
        penalty: $("input[name=penalty]:checked").val()
      };
    }
    if (algo === "svm"){
      return {
        C: Math.pow(10, parseFloat($("#Cexp").val())),
        gamma: Math.pow(10, parseFloat($("#gammaexp").val()))
      };
    }
    if (algo === "knn"){
      return { k: $("#k").val() };
    }
    if (algo === "gb"){
      return {
        n_estimators: $("#n_estimators").val(),
        lr: (parseFloat($("#lr").val())/1000).toFixed(3),
        max_depth: $("#max_depth").val()
      };
    }
  }
  
  // ---------- initialize page ----------
  buildControls($("#algo").val());
  
  // change control set when algo changes
  $("#algo").on("change", () => buildControls($("#algo").val()));
  
  // update slider value labels live
  $(document).on("input", "input[type=range]", function(){
    $("#"+this.id+"-val").text(this.value);
  });
  
  // ---------- Plotly history figure ----------
  let runIdx = 0;
  Plotly.newPlot("history",
    [{x:[],y:[],mode:"lines+markers",name:"AUC"}],
    {title:"Run history",yaxis:{range:[0.5,1]}}
  );
  
  // ---------- Train button ----------
  $("#trainBtn").off("click").on("click", () => {
    const algo = $("#algo").val();
    const hp   = collectHyperParams(algo);
  
    $.ajax({
      url: "/train",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({algo: algo, hyperparams: hp}),
      success: (res) => {
        $("#auc").text(res.auc.toFixed(3));
        $("#acc").text(res.accuracy.toFixed(3));
        $("#roc-img").attr("src","data:image/png;base64," + res.roc_plot);
        console.log(res.roc_plot);
  
        // append point to Plotly chart
        runIdx += 1;
        Plotly.extendTraces("history",{x:[[runIdx]],y:[[res.auc]]},[0]);
      },
      error: (xhr) => alert("Server error: "+xhr.responseText)
    });
  });
  

// function currentC() {
//     // slider exponent → 10 ** exponent
//     const exp = parseFloat($("#c‑slider").val());
//     return Math.pow(10, exp).toFixed(3);
//   }
  
//   $("#c‑slider").on("input", () => {
//     $("#c‑val").text(currentC());
//   });
  
//   $("#trainBtn").on("click", () => {
//     const C       = currentC();
//     const penalty = $("input[name=penalty]:checked").val();
  
//     $.ajax({
//       url: "/train",
//       method: "POST",
//       contentType: "application/json",
//       data: JSON.stringify({ C: C, penalty: penalty }),
//       success: (res) => {
//         $("#auc").text(res.auc.toFixed(3));
//         $("#acc").text(res.accuracy.toFixed(3));
//         $("#roc‑img").attr("src", "data:image/png;base64," + res.roc_plot);
//       },
//       error: (xhr) => alert("Server error: " + xhr.responseText)
//     });
//   });
  