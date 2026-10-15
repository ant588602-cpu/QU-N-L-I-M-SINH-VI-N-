
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản lý điểm sinh viên",
                   layout="wide")

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Cau 1: Tao DataFrame
du_lieu = {
    "MSSV": ["SV01", "SV02", "SV03", "SV04", "SV05",
             "SV06", "SV07", "SV08", "SV09", "SV10"],
    "Ten": ["An", "Bảo", "Tuấn", "Vũ", "Hùng",
            "Thắng", "Long", "Nam", "Thành", "Nhân"],
    "Chuyên cần": [6, 7, 4, 6, 9, 3, 8, 5, 7, 10],
    "Giữa kỳ": [7, 5, 6, 9, 3, 5, 9, 10, 7, 5],
    "Cuối kỳ": [7, 5, 3, 8, 9, 6, 7, 4, 7, 10]
}

df = pd.DataFrame(du_lieu)

# Cau 2: Tinh diem tong ket
df["điểm tổng kết"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
).round(2)

# Cau 3: Xep loai sinh vien
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["điểm tổng kết"].apply(xep_loai)

# Cau 4: Thong ke
diem_tb = df["điểm tổng kết"].mean()
sv_cao = df.loc[df["điểm tổng kết"].idxmax()]
sv_thap = df.loc[df["điểm tổng kết"].idxmin()]
so_sv_dat = (df["điểm tổng kết"] >= 5).sum()

st.subheader("1. Bảng điểm sinh viên")

bang = df.rename(columns={
    "Ten": "Họ tên",
    "điểm tổng kết": "Tổng kết",
    "Xep_loai": "Xếp loại"
})

st.dataframe(bang, hide_index=True, use_container_width=True)

st.subheader("2. Thống kê kết quả")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{sv_cao['điểm tổng kết']:.2f}")
c3.metric("Điểm thấp nhất", f"{sv_thap['điểm tổng kết']:.2f}")
c4.metric("Số sinh viên đạt", f"{so_sv_dat}/10")

st.write(f"Sinh viên cao nhất: {sv_cao['Ten']} - {sv_cao['MSSV']}")
st.write(f"Sinh viên thấp nhất: {sv_thap['Ten']} - {sv_thap['MSSV']}")

# Cau 5: Chon sinh vien
st.subheader("3. Tra cứu sinh viên")

ten_sv = st.selectbox("Chọn sinh viên:", df["Ten"])
sv = df[df["Ten"] == ten_sv].iloc[0]

st.write(f"**Họ tên:** {sv['Ten']}")
st.write(f"**MSSV:** {sv['MSSV']}")
st.write(f"**Chuyên cần:** {sv['Chuyên cần']}")
st.write(f"**Giữa kỳ:** {sv['Giữa kỳ']}")
st.write(f"**Cuối kỳ:** {sv['Cuối kỳ']}")
st.write(f"**Điểm tổng kết:** {sv['điểm tổng kết']}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# Cau 6: Bieu do cot
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df["Ten"], df["điểm tổng kết"])
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Cau 7: Thong tin nguoi tao
st.markdown("---")
st.caption("Người tạo: Trương Nguyễn Tường An | MSSV:060208013845")
