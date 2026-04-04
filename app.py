import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Car Sales Analyzer", layout="centered")

st.title("🚗 Car Sales Analyzer Dashboard")

# -------------------------------
# Generate Sales Data
# -------------------------------
st.header("🎲 Generate Sales Data")

n = st.number_input("Number of Salespeople", min_value=1, value=8)

if st.button("Generate Sales Data"):
    names = np.array([f"Salesperson {i+1}" for i in range(int(n))])
    sales = np.random.randint(0, 21, size=(int(n), 3))

    df = pd.DataFrame(sales, columns=["SUV", "Sedan", "Hatchback"])
    df.insert(0, "Salesperson", names)

    st.session_state["data"] = df

# Display Data
if "data" in st.session_state:
    st.subheader("📋 Sales Data")
    st.dataframe(st.session_state["data"], use_container_width=True)


# -------------------------------
# Salesperson Totals
# -------------------------------
st.header("📊 Salesperson Totals")

if st.button("Compute Totals"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"].copy()

        df["Total"] = df[["SUV", "Sedan", "Hatchback"]].sum(axis=1)

        st.dataframe(df[["Salesperson", "Total"]])

        # 📊 Bar Chart
        st.subheader("📊 Total Sales per Salesperson")
        plt.figure()
        plt.bar(df["Salesperson"], df["Total"])
        plt.xticks(rotation=45)
        st.pyplot(plt)


# -------------------------------
# Category Totals
# -------------------------------
st.header("📈 Category Totals")

if st.button("Compute Category Totals"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"]

        totals = df[["SUV", "Sedan", "Hatchback"]].sum()

        st.write(totals)

        # 📊 Bar Chart
        st.subheader("📊 Total Sales by Category")
        plt.figure()
        plt.bar(totals.index, totals.values)
        st.pyplot(plt)


# -------------------------------
# Rankings
# -------------------------------
st.header("🏆 Rankings")

if st.button("Rank Salespeople"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"].copy()

        df["Total"] = df[["SUV", "Sedan", "Hatchback"]].sum(axis=1)
        df = df.sort_values(by="Total", ascending=False)
        df["Rank"] = np.arange(1, len(df) + 1)

        st.dataframe(df[["Rank", "Salesperson", "Total"]])

        # 📊 Ranking Chart
        st.subheader("🏆 Sales Rankings")
        plt.figure()
        plt.bar(df["Salesperson"], df["Total"])
        plt.xticks(rotation=45)
        st.pyplot(plt)


# -------------------------------
# Filter Top Performers
# -------------------------------
st.header("🔍 Filter Top Performers")

threshold = st.number_input("Total Sales Threshold", value=25)

if st.button("Filter"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"].copy()

        df["Total"] = df[["SUV", "Sedan", "Hatchback"]].sum(axis=1)
        filtered = df[df["Total"] > threshold].sort_values(by="Total", ascending=False)

        if filtered.empty:
            st.warning("No results found.")
        else:
            st.dataframe(filtered[["Salesperson", "Total"]])

            # 📊 Filter Chart
            st.subheader("📊 Top Performers")
            plt.figure()
            plt.bar(filtered["Salesperson"], filtered["Total"])
            plt.xticks(rotation=45)
            st.pyplot(plt)
