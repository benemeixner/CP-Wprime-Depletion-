# CP & W' Calculator (Inverse-Time Model)

- Inputs: 3-, 5-, 12-min mean power (whole watts)
- Outputs: CP (W), W' (kJ), plus target powers to expend 70% and 30% of W' over 3 min each.

Model: **P = W'/t + CP** (inverse-time linear model).

## Run
```bash
pip install -r requirements.txt
streamlit run app_cpwprime.py
```
