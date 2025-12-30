import streamlit as st
from main import run_analysis

st.set_page_config(page_title="AI Board of Directors", layout="wide")

st.title("🧠 AI Board of Directors – Stock Research System")

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT)")

if st.button("Run Board Analysis"):
    if not symbol:
        st.warning("Please enter a stock symbol.")
    else:
        with st.spinner("Running multi-agent analysis..."):
            results = run_analysis(symbol.upper())

        st.success("Analysis Complete")

        with st.expander("🅰️ Fundamental Analysis"):
            st.write(results["Fundamental Analysis"])

        with st.expander("🧠 Management Quality Analysis"):
            st.write(results["Management Analysis"])

        with st.expander("📈 Technical Analysis"):
            st.write(results["Technical Analysis"])

        with st.expander("🧨 Contrarian View"):
            st.write(results["Contrarian View"])

        st.markdown("---")
        st.subheader("📌 FINAL BOARD CONSENSUS")
        st.write(results["Final Decision"])

        st.markdown("""
        ---
        ⚠️ This tool is for educational and research purposes only.
        Not financial advice.
        """)
