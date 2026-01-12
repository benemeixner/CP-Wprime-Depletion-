# CP & W' Calculator (Inverse-Time Model)

This Streamlit app computes **Critical Power (CP)** and **W'** from mean powers
in 3-, 5-, and 12-minute time trials using the inverse-time model:

> **P = W'/t + CP**

It also computes the constant power required to expend:
- **70% of W'** in **3 minutes**, and then
- **30% of W'** in another **3 minutes**,

via:

> (P − CP) × duration = fraction × W'  
> → **P = CP + fraction·W'/duration**

## Files
- `app_cpwprime.py` – Streamlit UI
- `cp_core.py` – model + calculations
- `requirements.txt`

## Local run
```bash
pip install -r requirements.txt
streamlit run app_cpwprime.py
```

## Streamlit Cloud
Create a GitHub repo with these files and deploy using `app_cpwprime.py` as the main file.
