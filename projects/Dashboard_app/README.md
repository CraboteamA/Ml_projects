# Hyper‑parameter Playground

Interactive **Flask** dashboard for _real‑time_ model tuning and experiment tracking.  
Tweak hyper‑parameters for multiple scikit‑learn algorithms, watch live ROC curves, keep a run‑by‑run AUC history, and log everything to **MLflow** locally.

---

## ✨ Features

| Capability          | Details                                                                                  |
|---------------------|------------------------------------------------------------------------------------------|
| **Algorithms**      | Logistic Regression · SVM · k‑NN · Gradient Boosting                                     |
| **Dynamic UI**      | Slider / radio panel generated automatically for the chosen algorithm                    |
| **Live metrics**    | Instant ROC image + AUC & accuracy tiles (AJAX refresh—no page reload)                   |
| **Run history**     | Plotly line chart accumulates AUC across runs                                            |
| **Experiment log**  | MLflow stores every run’s parameters, metrics, and ROC PNG artefact                      |
| **Responsive UX**   | Bootstrap 5 dashboard: sidebar controls, soft‑shadow cards, subtle fade‑in animations    |

---
## Project start
### 1 · Create env
```conda create -n playground python=3.12 -y```
```conda activate playground```

### 2 · Install deps
```pip install -r requirements.txt```

### 3 · Run Flask dev server
```python app.py # http://127.0.0.1:5000```

## How it works

1. **Front‑end** sends ```{ algo, hyperparams }``` via AJAX → ```/train```.
2. **Back‑end** rebuilds a scikit‑learn ```Pipeline```, fits on a fixed train split.
3. Metrics (AUC, accuracy) computed on the held‑out test set.
4. Matplotlib (Agg backend) renders the ROC to PNG → base64.
5. Response updates metric tiles, the ```<img>``` source, and Plotly chart.
6. MLflow logs parameters, metrics, and the ROC image artefact.
