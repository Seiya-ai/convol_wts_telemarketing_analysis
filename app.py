import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(
    page_title="初回架電タイミング分析",
    layout="wide",
)

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

st.subheader("初回架電タイミング別の受注率")

plt.rcParams["font.family"] = "Yu Gothic"

fig, ax = plt.subplots(figsize=(5, 3.0))

bars = ax.bar(
    df_order_rate["架電タイミング"],
    df_order_rate["受注率"],
)

for bar, total, orders, rate in zip(
    bars,
    df_order_rate["顧客数"],
    df_order_rate["受注数"],
    df_order_rate["受注率"],
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{int(orders)}/{int(total)}件\n"
        f"{rate:.1f}%",
        ha="center",
        va="bottom",
        fontsize=11,
    )

ax.set_xlabel(
    "後確OK日から初回架電までの日数",
    fontsize=9,
)

ax.set_ylabel(
    "WTS受注率 (%)",
    fontsize=9,
)

ax.set_ylim(
    0,
    df_order_rate["受注率"].max() + 6,
)

ax.grid(
    axis="y",
    alpha=0.3,
)

st.pyplot(fig, use_container_width=False)


# =========================
# 集計表
# =========================

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
# 比率検定
# =========================

# p_pool = (
#     success_1 + success_2
# ) / (
#     total_1 + total_2
# )

# se = math.sqrt(
#     p_pool
#     * (1 - p_pool)
#     * (
#         1 / total_1
#         + 1 / total_2
#     )
# )

# z_stat = (
#     p1 - p2
# ) / se

# p_value = math.erfc(
#     abs(z_stat)
#     / math.sqrt(2)
# )

# st.write(
#     f"**p値：{p_value:.3f}**"
# )

# if p_value < 0.05:
#     st.success(
#         "1日と2日以降の受注率には、"
#         "統計的に有意な差が確認されました。"
#     )
# else:
#     st.info(
#         "1日の方が受注率は高いものの、"
#         "今回のデータでは統計的に有意な差は"
#         "確認できませんでした。（つまり、サンプルの誤差があるかもしれないは否定できない）"
#     )


# =========================
# 考察
# =========================

st.subheader("考察")

st.markdown(
    """
- **0日：18.5%（5 / 27件）**
- **1日：17.1%（121 / 706件）**
- **2日以降：14.4%（52 / 360件）**

初回架電が2日以降になると、
1日で架電したケースと比較して
**受注率が約2.7ポイント低下**しています。

後確後に電話が入ることを一声干渉しているということで、出来るだけ同日に架電することで受注率の向上が見込めると考えます。

また、0日については27件とサンプル数が少ないため、受注率18.5%は参考値として扱う必要がありますが、逆を言うと、サンプルが増えれば
受注率がもっと上がるかもしれません。
"""
)

# =========================
# 今後の提案
# =========================
# =========================

st.subheader("今後の提案")

st.markdown(
    """
一声干渉から実際に架電時間にラグがあるにはリストにインポートする作業が発生していることが原因と考えられます。

その作業をFile Makerと連携して自動化することで、よりダイナミックに架電が出来受注率の向上につながります。
"""
)
