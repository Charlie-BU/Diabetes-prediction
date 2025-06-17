import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# I had to do all of this to make sure matplotlib displays Chinese characters in plots correctly. I'm on Linux though, this rcParamas stuff might not be necessary/might not work on Windows PCs.
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
rcParams['axes.unicode_minus'] = False

df = pd.read_excel("Physical_Examination_Data.xlsx")

# The feature that corresponds to the glucose level in the Kaggle dataset is 平均血糖, because Kaggle uses average glucose over time. 空腹血糖 is glucose while fasting, so this is a different feature. We should not just this because it has a different distribution from the glucose feature in kaggle. However, in the Chinese hospitals dataset only 9 people did the 空腹血糖 and 糖化血红蛋白A1C tests, so there are barely any people for who we actually have these super important kaggle features. So just out of curiosity I'm looking at the 空腹血糖 value as well, eventhough it doesn't actually correspond to the right kaggle feature.
# Filter rows where 小项名称 contains any of the four keywords
keywords = ["糖化血红蛋白A1C", "空腹血糖", "平均血糖", "高血压史", "体重指数"]
pattern = "|".join(keywords)
mask = df["小项名称"].str.contains(pattern, na=False)
df = df[mask]

# Keep only the columns containing the same data as the kaggle dataset
cols_to_keep = [
    "ST_MD5(C.SFZH00)", "性别", "年龄", "小项名称",
    "检查结果", "检验结果", "体检结论"
]
df = df[cols_to_keep]

# Merge the 检查结果 column into the 检验结果 column
df["检验结果"] = df.apply(
    lambda r: r["检验结果"]
              if pd.notnull(r["检验结果"]) and str(r["检验结果"]).strip() != ""
              else r["检查结果"],
    axis=1
)
df = df.drop(columns=["检查结果"])

n_tests = df["小项名称"].nunique()
print(f"Found {n_tests} distinct test items in 小项名称")

# Pivot so each 小项名称 is its own column, values from 检验结果
wide = (
    df
    .pivot_table(
        index=["ST_MD5(C.SFZH00)", "性别", "年龄", "体检结论"],
        columns="小项名称",
        values="检验结果",
        aggfunc="first"       # in case of duplicates, take the first
    )
    .reset_index()
)

# Optional: flatten the columns index
wide.columns.name = None
wide = wide.rename_axis(None, axis=1)

# wide = pd.read_excel("reformed_file.xlsx")

# 6. Count unique patients by 身份证
unique_patients = wide["ST_MD5(C.SFZH00)"].nunique()
print(f"Number of remaining unique ST_MD5(C.SFZH00) IDs: {unique_patients}")

# Now `wide` has one row per patient, with a column for each test.
print(wide.shape)  # rows = patients, cols = demographic + tests
print(wide.columns.tolist())
wide.head()
    
# Convert 体重指数, 高血压史 and 性别 columns to numeric data
wide["体重指数"] = (
    wide["体重指数"]
      .str.split(",", n=1).str[0]
      .astype(float, errors="ignore")
)

wide["高血压史"] = wide["高血压史"].map({
    "无": 0,
    "高血压史": 1
})

# Convert 性别: 女 -> 0, 男 -> 1
wide['性别'] = wide['性别'].map({'女': 0, '男': 1})

col = '体检结论'

# Doctors use these 5 phrases for diagnosing/ not diagnosing diabtes
diabetes_phrases_all = [
    '糖尿病',
    '糖尿病性视网膜病变Ⅰ期',
    '糖尿病性视网膜病变Ⅱ期',
    '糖尿病筛查风险评估轻度风险',
    '糖尿病筛查风险评估高风险或糖尿病'
]

# We consider these phrases as diabtes positive
diabetes_phrases_positive = [
    '糖尿病',
    '糖尿病性视网膜病变Ⅰ期',
    '糖尿病性视网膜病变Ⅱ期',
    '糖尿病筛查风险评估高风险或糖尿病'
]

# Function to check for any presence of a set of phrases
def contains_any(entry: str, phrases: list) -> bool:
    if pd.isna(entry):
        return False
    parts = [phrase.strip() for phrase in str(entry).split(',')]
    return any(p in parts for p in phrases)

# Create diabetes binary label (1 if any positive phrase found)
wide['糖尿病'] = wide[col].apply(lambda x: 1 if contains_any(x, diabetes_phrases_positive) else 0)

# Count how many patients have NONE of the 5 diabetes-related phrases
no_diabetes_terms = (~wide[col].apply(lambda x: contains_any(x, diabetes_phrases_all))).sum()
print(f"Number of patients with none of the 5 diabetes phrases: {no_diabetes_terms}")

num_negative = (wide['糖尿病'] == 0).sum()
print(f"Number of patients without diabetes (labeled 0): {num_negative}")

wide.to_excel('reformed_file.xlsx', index=False, engine='openpyxl')

# # Here I wanted to extract all types of phrases that the doctors use for diagnois in the 体检结论 column. I had this idea that I could go through them by hand to categorize who has heart disease and who hasn't, but that is aboslutely not worth my time, since this dataset is alaready missing important features like average Glucose and glycated Hemoglboin A1c
# # Initialize a set to collect unique phrases
# unique_phrases = set()

# # Iterate over each cell in the column
# for entry in wide[col].dropna():
#     # Split by comma and strip whitespace
#     parts = [phrase.strip() for phrase in str(entry).split(',') if phrase.strip()]
#     unique_phrases.update(parts)

# # Output the total number of unique phrases
# print(f"Total unique phrases: {len(unique_phrases)}")

# # Write the unique phrases to a text file, one phrase per line
# output_path = 'unique_phrases.txt'
# with open(output_path, 'w', encoding='utf-8') as f:
#     for phrase in sorted(unique_phrases):
#         f.write(f"{phrase}\n")

# print(f"Unique phrases written to: {output_path}")

# This whole section is just printing distributions of the features.

numeric_cols = ['年龄','体重指数','平均血糖','空腹血糖','糖化血红蛋白A1C']

for col in numeric_cols:
    # Coerce; anything unparseable → NaN
    coerced = pd.to_numeric(wide[col], errors='coerce')
    
    # Report the ones that *didn’t* convert
    bad = wide[col][wide[col].notna() & coerced.isna()]
    if not bad.empty:
        print(f"Column “{col}” has {len(bad)} non-numeric entries:")
        print(bad.unique())
    
    # **Crucial step**: overwrite the column
    wide[col] = coerced

# This multiplication by 18 is necessary because the Kaggle datset uses a different unit of measurement for blood glucose levels.
wide['平均血糖'] = wide['平均血糖'] * 18
wide['空腹血糖'] = wide['空腹血糖'] * 18

# # Identify columns to analyze
# exclude = ['ST_MD5(C.SFZH00)', '性别', '高血压史', '糖尿病', '体检结论']
# all_columns = wide.columns.tolist()
# numeric_cols = [col for col in all_columns if col not in exclude]

# Calculate missing value stats
total = len(wide)
missing_stats = pd.DataFrame({
    'column': wide.columns,
    'missing_count': wide.isna().sum().values,
    'missing_pct': (wide.isna().mean() * 100).values
})
print("Missing Values:")
print(missing_stats)

# Numeric columns: descriptive stats and histograms
descriptive = pd.DataFrame(columns=['mean', 'median', 'min', 'max', 'std'])
for col in numeric_cols:
    series = wide[col]
    descriptive.loc[col] = [
        series.mean(),
        series.median(),
        series.min(),
        series.max(),
        series.std()
    ]
    # Plot distribution
    plt.figure()
    plt.hist(series.dropna(), bins=30)
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

print("Descriptive Statistics for Numeric Variables:")
print(descriptive)

# Bar charts for binary features
binary_cols = ['性别', '高血压史', '糖尿病']
total_patients = len(wide)
for col in binary_cols:
    counts = wide[col].value_counts(dropna=False).sort_index()
    plt.figure()
    counts.plot(kind='bar')
    plt.title(f"Bar Chart of {col}")
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

    # counts = wide[col].value_counts(dropna=False)
    percentages = counts / total_patients * 100
    print(f"\nDistribution for {col}:")
    for value, count in counts.items():
        pct = percentages.loc[value]
        print(f"  Value={value!r}: {count} patients ({pct:.2f}%)")
