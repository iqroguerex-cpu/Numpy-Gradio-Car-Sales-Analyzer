import numpy as np
import gradio as gr


def generate_sales(n):
    n = int(n)

    names = np.array([f"Salesperson {i+1}" for i in range(n)])
    sales = np.random.randint(0, 21, size=(n, 3))

    table = np.column_stack((names, sales))

    return table, table


def salesperson_totals(data):
    data = np.array(data)

    names = data[:, 0]
    totals = np.sum(data[:, 1:].astype(float), axis=1)

    return np.column_stack((names, totals))


def category_totals(data):
    data = np.array(data)

    categories = np.array(["SUV", "Sedan", "Hatchback"])
    totals = np.sum(data[:, 1:].astype(float), axis=0)

    return np.column_stack((categories, totals))


def rank_salespeople(data):
    data = np.array(data)

    names = data[:, 0]
    totals = np.sum(data[:, 1:].astype(float), axis=1)

    idx = np.argsort(totals)[::-1]

    ranked_names = names[idx]
    ranked_totals = totals[idx]

    ranks = np.arange(1, len(ranked_names) + 1)

    return np.column_stack((ranks, ranked_names, ranked_totals))


def filter_top_performers(data, threshold):
    data = np.array(data)
    threshold = float(threshold)

    names = data[:, 0]
    totals = np.sum(data[:, 1:].astype(float), axis=1)

    mask = totals > threshold

    filtered_names = names[mask]
    filtered_totals = totals[mask]

    if len(filtered_totals) == 0:
        return np.array([["No results", ""]])

    idx = np.argsort(filtered_totals)[::-1]

    filtered_names = filtered_names[idx]
    filtered_totals = filtered_totals[idx]

    return np.column_stack((filtered_names, filtered_totals))


with gr.Blocks(title="Car Sales Analyzer") as demo:

    gr.Markdown("# 🚗 Car Sales Analyzer")

    data_state = gr.State()

    with gr.Row():
        count_input = gr.Number(value=8, label="Number of Salespeople")
        generate_btn = gr.Button("Generate Sales Data", variant="primary")

    sales_table = gr.Dataframe(
        headers=["Salesperson", "SUV", "Sedan", "Hatchback"],
        interactive=False
    )

    generate_btn.click(
        generate_sales,
        inputs=count_input,
        outputs=[data_state, sales_table]
    )

    gr.Markdown("---")

    with gr.Tab("📊 Salesperson Totals"):
        total_btn = gr.Button("Compute Totals", variant="primary")
        total_output = gr.Dataframe(
            headers=["Salesperson", "Total Units"],
            interactive=False
        )
        total_btn.click(salesperson_totals, inputs=data_state, outputs=total_output)

    with gr.Tab("📈 Category Totals"):
        category_btn = gr.Button("Compute Category Totals", variant="primary")
        category_output = gr.Dataframe(
            headers=["Category", "Total Units"],
            interactive=False
        )
        category_btn.click(category_totals, inputs=data_state, outputs=category_output)

    with gr.Tab("🏆 Rankings"):
        rank_btn = gr.Button("Rank Salespeople", variant="primary")
        rank_output = gr.Dataframe(
            headers=["Rank", "Salesperson", "Total Units"],
            interactive=False
        )
        rank_btn.click(rank_salespeople, inputs=data_state, outputs=rank_output)

    with gr.Tab("🔍 Filter Top Performers"):
        threshold_input = gr.Number(value=25, label="Total Sales Threshold")
        filter_btn = gr.Button("Filter", variant="primary")
        filter_output = gr.Dataframe(
            headers=["Salesperson", "Total Units"],
            interactive=False
        )
        filter_btn.click(
            filter_top_performers,
            inputs=[data_state, threshold_input],
            outputs=filter_output
        )

demo.launch(theme=gr.themes.Soft())
