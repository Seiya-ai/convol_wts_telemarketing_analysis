import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# ページ設定
# =========================

st.set_page_config(
    page_title="初回架電タイミング分析",
    layout="wide",
)


# =========================
# セクション間の余白
# =========================

def add_section_space(height=40):
    st.markdown(
        f"<div style='height: {height}px;'></div>",
        unsafe_allow_html=True,
    )


# =========================
# タイトル
# =========================

st.title("初回架電タイミングとWTS受注率")

st.write(
    "後確OK日から初回架電までの日数によって、"
    "WTS受注率にどの程度の差があるかを確認します。"
)


# =========================
# 集計データ
# =========================

df_order_rate = pd.DataFrame({
    "架電タイミング": [
        "同じ日に架電",
        "1日経過",
        "2日以降経過",
    ],
    "顧客数": [
        27,
        706,
        360,
    ],
    "受注数": [
        5,
        121,
        52,
    ],
})

df_order_rate["受注率"] = (
    df_order_rate["受注数"]
    / df_order_rate["顧客数"]
    * 100
)


# =========================
# KPI
# =========================

add_section_space()

st.subheader("受注率")

col1, col2, col3 = st.columns(3)

cols = [col1, col2, col3]

for col, (_, row) in zip(
    cols,
    df_order_rate.iterrows(),
):
    col.metric(
        label=row["架電タイミング"],
        value=f'{row["受注率"]:.1f}%',
    )

    col.caption(
        f'{int(row["顧客数"])}件中 '
        f'{int(row["受注数"])}件受注'
    )


# =========================
# グラフ
# =========================

add_section_space()

st.subheader("初回架電タイミング別の受注率")

# Matplotlib内は英語にして
# 日本語フォント問題を完全に回避
plot_labels = [
    "Same day",
    "1 day later",
    "2+ days later",
]

fig, ax = plt.subplots(figsize=(7, 4))

bars = ax.bar(
    plot_labels,
    df_order_rate["受注率"],
    color="#287CB5",
)

# 棒の上に受注数・受注率を表示
for bar, total, orders, rate in zip(
    bars,
    df_order_rate["顧客数"],
    df_order_rate["受注数"],
    df_order_rate["受注率"],
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{int(orders)}/{int(total)}\n"
        f"{rate:.1f}%",
        ha="center",
        va="bottom",
        fontsize=11,
    )

ax.set_xlabel(
    "Days from OK date to first call",
    fontsize=10,
)

ax.set_ylabel(
    "WTS Order Rate (%)",
    fontsize=10,
)

ax.set_ylim(
    0,
    df_order_rate["受注率"].max() + 5,
)

ax.grid(
    axis="y",
    alpha=0.3,
)

# 上と右の枠線を少し薄くする
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=False,
)

plt.close(fig)


# =========================
# 集計表
# =========================

add_section_space()

st.subheader("集計結果")

display_df = df_order_rate.copy()

display_df["受注率"] = (
    display_df["受注率"]
    .map(lambda x: f"{x:.1f}%")
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)


# =========================
# 1日 vs 2日以降
# =========================

add_section_space()

st.subheader("1日と2日以降の比較")

success_1 = 121
total_1 = 706

success_2 = 52
total_2 = 360

p1 = success_1 / total_1
p2 = success_2 / total_2

difference = p1 - p2

col1, col2, col3 = st.columns(3)

col1.metric(
    "1日の受注率",
    f"{p1:.1%}",
)

col2.metric(
    "2日以降の受注率",
    f"{p2:.1%}",
)

col3.metric(
    "受注率の差",
    f"{difference * 100:.1f}pt",
)


# =========================
# 考察
# =========================

add_section_space()

st.subheader("考察")

st.markdown(
    """
- **0日：18.5%（5 / 27件）**
- **1日：17.1%（121 / 706件）**
- **2日以降：14.4%（52 / 360件）**

初回架電が2日以降になると、
1日で架電したケースと比較して
**受注率が約2.7ポイント低下**しています。

後確OK日から実際の架電までにタイムラグが発生すると、
受注率が低下する傾向が見られます。

そのため、できるだけ**同日、遅くとも翌日までに架電することで、
受注率の向上が期待できる**と考えられます。

一方、0日については27件とサンプル数が少ないため、
18.5%という受注率は参考値として扱う必要があります。
今後、同日架電のサンプル数を増やすことで、
この傾向が再現するかを確認する必要があります。
"""
)


# =========================
# 今後の提案
# =========================

add_section_space()

st.subheader("今後の提案")

st.markdown(
    """
現在、後確OKから実際の架電までにタイムラグが発生する要因として、
リストをインポートする作業が発生していることが考えられます。

この作業を**FileMakerと連携して自動化**することで、
後確OKから架電までの時間を短縮し、
よりタイムリーに架電できる仕組みを構築できます。

その結果、初回架電の早期化による
**受注率向上につながる可能性があります。**
"""
)
