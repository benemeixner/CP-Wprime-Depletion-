# app_cpwprime.py
import streamlit as st
import pandas as pd

from cp_core import fit_inverse_time_model, power_for_fraction_wprime

st.set_page_config(page_title="CP & W' (Inverse-Time)", layout="centered")
st.title("CP & W' from 3 / 5 / 12-min mean power")

st.write(
    "Enter mean power values (W) for **3, 5, and 12 min** time trials. "
    "The app fits the inverse-time model: **P = W'/t + CP**."
)

with st.form("inputs"):
    c1, c2, c3 = st.columns(3)
    with c1:
        p3 = st.number_input("3-min mean power (W)", min_value=0.0, value=0.0, step=1.0)
    with c2:
        p5 = st.number_input("5-min mean power (W)", min_value=0.0, value=0.0, step=1.0)
    with c3:
        p12 = st.number_input("12-min mean power (W)", min_value=0.0, value=0.0, step=1.0)

    st.caption("Durations are fixed at 180 s, 300 s, 720 s.")
    submitted = st.form_submit_button("Calculate")

if submitted:
    try:
        powers = [p3, p5, p12]
        durations = [180, 300, 720]
        res = fit_inverse_time_model(powers, durations)

        cp = res.cp_w
        wprime_j = res.wprime_j
        wprime_kj = wprime_j / 1000.0

        st.subheader("Results")
        m1, m2, m3 = st.columns(3)
        m1.metric("CP (W)", f"{cp:.1f}")
        m2.metric("W' (kJ)", f"{wprime_kj:.2f}")
        m3.metric("Fit R²", f"{res.r2:.3f}" if pd.notna(res.r2) else "n/a")

        st.subheader("Target powers to deplete W' in 3 + 3 minutes")
        p_70 = power_for_fraction_wprime(cp, wprime_j, fraction=0.70, duration_s=180)
        p_30 = power_for_fraction_wprime(cp, wprime_j, fraction=0.30, duration_s=180)

        r1, r2 = st.columns(2)
        r1.metric("Power for 70% W' in 3 min (W)", f"{p_70:.1f}")
        r2.metric("Power for remaining 30% W' in 3 min (W)", f"{p_30:.1f}")

        st.caption(
            "Formula: (P − CP) × duration = fraction × W'  →  P = CP + fraction·W'/duration. "
            "This ignores any W' reconstitution during the effort."
        )

        st.subheader("Fit details")
        df = pd.DataFrame({
            "Duration (s)": res.durations_s,
            "Mean Power (W)": res.powers_w,
            "Residual (W)": res.residuals_w
        })
        st.dataframe(df, use_container_width=True)

        st.subheader("Copy-friendly summary")
        st.code(
            f"CP = {cp:.1f} W\n"
            f"W' = {wprime_kj:.2f} kJ\n"
            f"P(70% W' over 180 s) = {p_70:.1f} W\n"
            f"P(30% W' over 180 s) = {p_30:.1f} W\n"
            f"R² = {res.r2:.3f}",
            language="text"
        )

    except Exception as e:
        st.error(f"Could not compute CP/W': {e}")

st.divider()
st.markdown("""### Deploy (Streamlit Community Cloud)
Repo contents:
- `app_cpwprime.py`
- `cp_core.py`
- `requirements.txt`

Run locally:
```bash
pip install -r requirements.txt
streamlit run app_cpwprime.py
```
""")
