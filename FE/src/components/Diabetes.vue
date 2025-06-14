<template>
    <div class="patient-table-container">
        <div class="table-header">
            <h2>Diabetes Predition</h2>
            <el-button type="primary" @click="openFilterDialog" class="filter-button">
                <el-icon>
                    <Filter />
                </el-icon>
                Input
            </el-button>
        </div>

        <!-- 弹窗 -->
        <el-dialog v-model="filterDialogVisible" title="Input" width="1000" class="filter-dialog"
            :close-on-click-modal="false">
            <el-form :model="filterForm" label-width="120px" label-position="left">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="Gender">
                            <el-select v-model="filterForm.gender" placeholder="Select Gender" clearable>
                                <el-option label="Male" value="Male" />
                                <el-option label="Female" value="Female" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Age">
                            <el-input-number v-model="filterForm.age" placeholder="Enter Age" :min="0" :max="120"
                                :precision="0" />
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Hypertension">
                            <el-select v-model="filterForm.hypertension" placeholder="Select" clearable>
                                <el-option label="Yes" :value="1" />
                                <el-option label="No" :value="0" />
                                <template #loading></template>
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Heart Disease">
                            <el-select v-model="filterForm.heart_disease" placeholder="Select" clearable>
                                <el-option label="Yes" :value="1" />
                                <el-option label="No" :value="0" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Smoking History">
                            <el-select v-model="filterForm.smoking_history" placeholder="Select" clearable>
                                <el-option label="Never" value="never" />
                                <el-option label="Former" value="former" />
                                <el-option label="Ever" value="ever" />
                                <el-option label="Not Current" value="not current" />
                                <el-option label="Current" value="current" />
                                <el-option label="No Info" value="No Info" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="BMI">
                            <el-input-number v-model="filterForm.bmi" placeholder="Enter BMI" :min="0" :max="100"
                                :precision="1" :step="0.1" />
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="HbA1c Level">
                            <el-input-number v-model="filterForm.HbA1c_level" placeholder="Enter HbA1c Level" :min="0"
                                :max="20" :precision="1" :step="0.1" />
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Blood Glucose">
                            <el-input-number v-model="filterForm.blood_glucose_level"
                                placeholder="Enter Blood Glucose Level" :min="0" :max="500" :precision="0" />
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="resetFilter" class="reset-button">Reset</el-button>
                    <el-button type="primary" @click="predict" class="apply-button">Start</el-button>
                </div>
            </template>
        </el-dialog>

        <!-- 结果展示区域 -->
        <div v-if="Object.keys(result).length > 0" class="result-container">
            <div class="result-card">
                <div class="result-header">
                    <h3>Prediction Result</h3>
                    <div class="result-icon">
                        <el-icon size="24">
                            <TrendCharts />
                        </el-icon>
                    </div>
                </div>

                <div class="result-content">
                    <!-- 风险等级展示 -->
                    <div class="risk-level-section">
                        <div class="risk-level-card" :class="getRiskLevelClass(result.risk_level || '')">
                            <div class="risk-icon">
                                <el-icon size="32">
                                    <component :is="getRiskIcon(result.risk_level || '')" />
                                </el-icon>
                            </div>
                            <div class="risk-content">
                                <h4>Risk Level</h4>
                                <span class="risk-value">{{ result.risk_level || 'Unknown' }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- 预测结果和概率 -->
                    <div class="prediction-section">
                        <div class="prediction-card">
                            <div class="prediction-item">
                                <div class="prediction-label">Prediction</div>
                                <div class="prediction-value"
                                    :class="(result.prediction ?? 0) === 1 ? 'positive' : 'negative'">
                                    {{ (result.prediction ?? 0) === 1 ? 'Diabetes' : 'No Diabetes' }}
                                </div>
                            </div>

                            <div class="probability-item">
                                <div class="probability-label">Probability</div>
                                <div class="probability-display">
                                    <div class="probability-circle">
                                        <svg class="progress-ring" width="120" height="120">
                                            <circle class="progress-ring-circle-bg" stroke="#2a2a40" stroke-width="8"
                                                fill="transparent" r="52" cx="60" cy="60" />
                                            <circle class="progress-ring-circle"
                                                :stroke="getProbabilityColor(result.probability ?? 0)" stroke-width="8"
                                                fill="transparent" r="52" cx="60" cy="60"
                                                :stroke-dasharray="`${getProbabilityPercentage(result.probability ?? 0) * 3.27} 327`"
                                                stroke-linecap="round" />
                                        </svg>
                                        <div class="probability-text">
                                            <span class="percentage">{{ ((result.probability ?? 0) * 100).toFixed(4)
                                            }}%</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 详细信息 -->
                    <div class="details-section">
                        <div class="details-card">
                            <h5>Analysis Details</h5>
                            <div class="details-grid">
                                <div class="detail-item">
                                    <span class="detail-label">Raw Probability:</span>
                                    <span class="detail-value">{{ ((result.probability ?? 0) * 100).toFixed(6)
                                    }}%</span>
                                </div>
                                <div class="detail-item">
                                    <span class="detail-label">Confidence:</span>
                                    <span class="detail-value">{{ getConfidenceLevel(result.probability ?? 0) }}</span>
                                </div>
                                <div class="detail-item">
                                    <span class="detail-label">Recommendation:</span>
                                    <span class="detail-value">{{ getRecommendation(result.risk_level || '') }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="result-actions">
                    <el-button @click="resetResult" class="reset-result-btn">
                        <el-icon>
                            <Refresh />
                        </el-icon>
                        New Prediction
                    </el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import * as request from "../utils/request"
import { Filter, TrendCharts, Refresh, SuccessFilled, WarningFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Result {
    probability?: number,
    risk_level?: string,
    prediction?: number,
}

const filterDialogVisible = ref(true)
const filterForm = reactive({
    gender: '',
    age: null as number | null,
    hypertension: null as number | null,
    heart_disease: null as number | null,
    smoking_history: '',
    bmi: null as number | null,
    HbA1c_level: null as number | null,
    blood_glucose_level: null as number | null,
})

// 打开筛选弹窗
const openFilterDialog = () => {
    filterDialogVisible.value = true
}

// 重置筛选条件
const resetFilter = () => {
    Object.keys(filterForm).forEach(key => {
        (filterForm as any)[key] = null
    })
    filterForm.gender = ''
    filterForm.smoking_history = ''
}


// 构建筛选参数
const buildFilterParams = () => {
    const params: Record<string, any> = {}
    const mustFields = ["gender", "age", "hypertension", "heart_disease", "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"] as const
    for (const field of mustFields) {
        if ((filterForm as any)[field] === null || (filterForm as any)[field] === '' || (filterForm as any)[field] === undefined) {
            ElMessage.error(`Please fill in the ${field}`)
            return null;
        }
    }
    // 添加筛选条件
    if (filterForm.gender) params.gender = filterForm.gender
    if (filterForm.age !== null) params.age = filterForm.age
    if (filterForm.hypertension !== null) params.hypertension = filterForm.hypertension
    if (filterForm.heart_disease !== null) params.heart_disease = filterForm.heart_disease
    if (filterForm.smoking_history) params.smoking_history = filterForm.smoking_history
    if (filterForm.bmi !== null) params.bmi = filterForm.bmi
    if (filterForm.HbA1c_level !== null) params.HbA1c_level = filterForm.HbA1c_level
    if (filterForm.blood_glucose_level !== null) params.blood_glucose_level = filterForm.blood_glucose_level

    return params;
}

const result = ref<Result>({})

const predict = async () => {
    const data = buildFilterParams();
    if (!data) {
        return;
    }
    const res = await request.post("/api/predict", data, { disease: "diabetes" });
    if (res.status !== 200) {
        ElMessage.error("Predict failed, please try again later.");
        return;
    }
    result.value = res.result;
    filterDialogVisible.value = false
}

// 重置结果
const resetResult = () => {
    result.value = {}
    resetFilter()
    openFilterDialog()
}

// 获取风险等级样式类
const getRiskLevelClass = (riskLevel: string) => {
    switch (riskLevel?.toLowerCase()) {
        case 'low':
            return 'risk-low'
        case 'medium':
            return 'risk-medium'
        case 'high':
            return 'risk-high'
        default:
            return 'risk-unknown'
    }
}

// 获取风险等级图标
const getRiskIcon = (riskLevel: string) => {
    switch (riskLevel?.toLowerCase()) {
        case 'low':
            return SuccessFilled
        case 'medium':
            return WarningFilled
        case 'high':
            return CircleCloseFilled
        default:
            return WarningFilled
    }
}

// 获取概率颜色
const getProbabilityColor = (probability: number) => {
    if (probability < 0.3) {
        return '#67C23A' // 绿色
    } else if (probability < 0.7) {
        return '#E6A23C' // 橙色
    } else {
        return '#F56C6C' // 红色
    }
}

// 获取概率百分比（用于圆形进度条）
const getProbabilityPercentage = (probability: number) => {
    return Math.min(probability * 100, 100)
}

// 获取置信度等级
const getConfidenceLevel = (probability: number) => {
    if (probability < 0.1) {
        return 'Very Low'
    } else if (probability < 0.3) {
        return 'Low'
    } else if (probability < 0.7) {
        return 'Medium'
    } else if (probability < 0.9) {
        return 'High'
    } else {
        return 'Very High'
    }
}

// 获取建议
const getRecommendation = (riskLevel: string) => {
    switch (riskLevel?.toLowerCase()) {
        case 'low':
            return 'Maintain healthy lifestyle'
        case 'medium':
            return 'Regular monitoring recommended'
        case 'high':
            return 'Consult healthcare provider'
        default:
            return 'Follow medical advice'
    }
}

</script>

<style scoped>
.patient-table-container {
    margin: 20px;
    border-radius: 12px;
    padding: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    animation: fadeIn 0.5s ease-out;
    min-height: 70vh;
}

.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.filter-button {
    background: linear-gradient(135deg, #8a2be2, #9370db);
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    transition: all 0.3s;
    box-shadow: 0 4px 12px rgba(138, 43, 226, 0.2);
}

.filter-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(138, 43, 226, 0.3);
}

.filter-button .el-icon {
    margin-right: 6px;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

h2 {
    margin-bottom: 0;
    color: #ffffff;
    font-weight: 600;
    letter-spacing: 1px;
    position: relative;
    display: inline-block;
    padding-bottom: 8px;
}

h2::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, #409EFF, #a855f7);
    border-radius: 3px;
}

.custom-table {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #2a2a40;
    transition: all 0.3s ease;
}

:deep(.custom-table .el-table__inner-wrapper) {
    border-radius: 10px;
    overflow: hidden;
}

:deep(.custom-table .el-table__header-wrapper) {
    border-radius: 10px 10px 0 0;
}

:deep(.custom-table .el-table__body-wrapper) {
    background-color: #1a1a2e;
}

:deep(.custom-table .even-row) {
    background-color: #1a1a2e !important;
}

:deep(.custom-table .odd-row) {
    background-color: #22223a !important;
}

:deep(.custom-table tr:hover > td) {
    background-color: rgba(103, 78, 167, 0.15) !important;
    transform: scale(1.01);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.custom-table td) {
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.status-tag {
    border-radius: 20px;
    padding: 2px 10px;
    font-weight: 500;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.status-tag:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* 分页组件样式 */
.pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
}

:deep(.custom-pagination) {
    --el-pagination-bg-color: #1a1a2e;
    --el-pagination-text-color: #e0e0e0;
    --el-pagination-button-color: #e0e0e0;
    --el-pagination-button-bg-color: #2a2a40;
    --el-pagination-button-disabled-color: #606266;
    --el-pagination-button-disabled-bg-color: #1a1a2e;
    --el-pagination-hover-color: #409EFF;
    --el-pagination-font-size: 14px;
}

:deep(.custom-pagination .el-pagination__total) {
    color: #e0e0e0;
}

:deep(.custom-pagination .el-input__inner) {
    background-color: #2a2a40;
    color: #e0e0e0;
    border-color: #3a3a50;
}

:deep(.custom-pagination .el-select .el-input .el-select__caret) {
    color: #e0e0e0;
}

:deep(.custom-pagination .el-pagination__jump) {
    color: #e0e0e0;
}

:deep(.custom-pagination .btn-prev),
:deep(.custom-pagination .btn-next),
:deep(.custom-pagination .el-pager li) {
    background-color: #2a2a40;
    color: #e0e0e0;
    border: none;
    transition: all 0.3s;
}

:deep(.custom-pagination .el-pager li:hover),
:deep(.custom-pagination .btn-prev:hover),
:deep(.custom-pagination .btn-next:hover) {
    background-color: #3a3a50;
    color: #ffffff;
}

:deep(.custom-pagination .el-pager li.is-active) {
    background-color: #409EFF;
    color: #ffffff;
}

/* 筛选弹窗样式 */
:deep(.filter-dialog) {
    border-radius: 12px;
    overflow: hidden;
    background-color: #2a2a40;
}

:deep(.filter-dialog .el-dialog__header) {
    background-color: #2a2a40;
    padding: 15px 20px;
    margin: 0;
}

:deep(.filter-dialog .el-dialog__title) {
    color: #ffffff;
    font-weight: 600;
    font-size: 18px;
}

:deep(.filter-dialog .el-dialog__headerbtn .el-dialog__close) {
    color: #ffffff;
}

:deep(.filter-dialog .el-dialog__body) {
    background-color: #1a1a2e;
    color: #e0e0e0;
    padding: 20px;
}

:deep(.filter-dialog .el-dialog__footer) {
    background-color: #1a1a2e;
    border-top: 1px solid #2a2a40;
    padding: 15px 20px;
}

:deep(.filter-dialog .el-form-item__label) {
    color: #e0e0e0;
}

/* 去除select和input的背景色 */
:deep(.filter-dialog .el-select .el-select__wrapper) {
    background-color: transparent !important;
}

:deep(.filter-dialog .el-input .el-input__wrapper) {
    background-color: transparent !important;
}

:deep(.filter-dialog .el-input-number .el-input__wrapper) {
    background-color: transparent !important;
}

/* 保持输入框内部元素的样式 */
:deep(.filter-dialog .el-input__inner) {
    background-color: #2a2a40;
    color: #e0e0e0;
    border: 1px solid #3a3a50;
    border-radius: 6px;
}

:deep(.filter-dialog .el-input-number__decrease),
:deep(.filter-dialog .el-input-number__increase) {
    background-color: #2a2a40;
    color: #e0e0e0;
    border-color: #3a3a50;
}

:deep(.filter-dialog .el-select .el-input .el-select__caret) {
    color: #e0e0e0;
}

/* 下拉菜单样式 */
:deep(.el-select-dropdown) {
    background-color: #2a2a40;
    border: 1px solid #3a3a50;
}

:deep(.el-select-dropdown__item) {
    color: #e0e0e0;
}

:deep(.el-select-dropdown__item.hover),
:deep(.el-select-dropdown__item:hover) {
    background-color: #3a3a50;
}

:deep(.el-select-dropdown__item.selected) {
    color: #409EFF;
    background-color: rgba(64, 158, 255, 0.1);
}

.text-center {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #e0e0e0;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.reset-button {
    background-color: #2a2a40;
    color: #e0e0e0;
    border: 1px solid #3a3a50;
    transition: all 0.3s;
}

.reset-button:hover {
    background-color: #3a3a50;
    color: #ffffff;
}

.apply-button {
    background: linear-gradient(135deg, #8a2be2, #9370db);
    border: none;
    transition: all 0.3s;
    box-shadow: 0 4px 12px rgba(138, 43, 226, 0.2);
}

.apply-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(138, 43, 226, 0.3);
}

/* 结果展示区域样式 */
.result-container {
    margin-top: 30px;
    animation: slideInUp 0.6s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.result-card {
    background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(42, 42, 64, 0.95));
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #409EFF, #a855f7, #8a2be2);
    border-radius: 20px 20px 0 0;
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.result-header h3 {
    color: #ffffff;
    font-size: 24px;
    font-weight: 600;
    margin: 0;
    letter-spacing: 1px;
}

.result-icon {
    background: linear-gradient(135deg, #409EFF, #a855f7);
    border-radius: 12px;
    padding: 12px;
    color: white;
    box-shadow: 0 8px 16px rgba(64, 158, 255, 0.3);
}

.result-content {
    display: grid;
    grid-template-columns: 1fr;
    gap: 25px;
}

/* 风险等级卡片 */
.risk-level-section {
    display: flex;
    justify-content: center;
}

.risk-level-card {
    display: flex;
    align-items: center;
    padding: 20px 30px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 2px solid;
    transition: all 0.3s ease;
    min-width: 280px;
}

.risk-level-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.risk-low {
    background: linear-gradient(135deg, rgba(103, 194, 58, 0.2), rgba(103, 194, 58, 0.1));
    border-color: #67C23A;
    box-shadow: 0 10px 20px rgba(103, 194, 58, 0.2);
}

.risk-medium {
    background: linear-gradient(135deg, rgba(230, 162, 60, 0.2), rgba(230, 162, 60, 0.1));
    border-color: #E6A23C;
    box-shadow: 0 10px 20px rgba(230, 162, 60, 0.2);
}

.risk-high {
    background: linear-gradient(135deg, rgba(245, 108, 108, 0.2), rgba(245, 108, 108, 0.1));
    border-color: #F56C6C;
    box-shadow: 0 10px 20px rgba(245, 108, 108, 0.2);
}

.risk-unknown {
    background: linear-gradient(135deg, rgba(144, 147, 153, 0.2), rgba(144, 147, 153, 0.1));
    border-color: #909399;
    box-shadow: 0 10px 20px rgba(144, 147, 153, 0.2);
}

.risk-icon {
    margin-right: 20px;
    padding: 15px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.1);
}

.risk-content h4 {
    margin: 0 0 8px 0;
    color: #e0e0e0;
    font-size: 16px;
    font-weight: 500;
}

.risk-value {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* 预测结果和概率 */
.prediction-section {
    display: flex;
    justify-content: center;
}

.prediction-card {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    width: 100%;
    max-width: 600px;
}

.prediction-item,
.probability-item {
    text-align: center;
    padding: 25px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.prediction-item:hover,
.probability-item:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    background: rgba(255, 255, 255, 0.08);
}

.prediction-label,
.probability-label {
    color: #b0b0b0;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.prediction-value {
    font-size: 20px;
    font-weight: 700;
    padding: 12px 20px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.prediction-value.positive {
    background: linear-gradient(135deg, rgba(245, 108, 108, 0.2), rgba(245, 108, 108, 0.1));
    color: #F56C6C;
    border: 2px solid rgba(245, 108, 108, 0.3);
}

.prediction-value.negative {
    background: linear-gradient(135deg, rgba(103, 194, 58, 0.2), rgba(103, 194, 58, 0.1));
    color: #67C23A;
    border: 2px solid rgba(103, 194, 58, 0.3);
}

/* 概率圆形进度条 */
.probability-display {
    display: flex;
    justify-content: center;
    align-items: center;
}

.probability-circle {
    position: relative;
    display: inline-block;
}

.progress-ring {
    transform: rotate(-90deg);
    filter: drop-shadow(0 0 10px rgba(64, 158, 255, 0.3));
}

.progress-ring-circle {
    transition: stroke-dasharray 0.8s ease-in-out;
    animation: progressAnimation 1.5s ease-out;
}

@keyframes progressAnimation {
    from {
        stroke-dasharray: 0 327;
    }
}

.probability-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

.percentage {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* 详细信息 */
.details-section {
    margin-top: 10px;
}

.details-card {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    padding: 25px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.details-card h5 {
    color: #ffffff;
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 20px 0;
    text-align: center;
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    border-left: 4px solid #409EFF;
    transition: all 0.3s ease;
}

.detail-item:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(5px);
}

.detail-label {
    color: #b0b0b0;
    font-weight: 500;
    font-size: 14px;
}

.detail-value {
    color: #ffffff;
    font-weight: 600;
    font-size: 14px;
    text-align: right;
}

/* 操作按钮 */
.result-actions {
    margin-top: 30px;
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.reset-result-btn {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border: none;
    border-radius: 12px;
    padding: 12px 30px;
    font-weight: 600;
    color: white;
    transition: all 0.3s ease;
    box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3);
}

.reset-result-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 24px rgba(99, 102, 241, 0.4);
    background: linear-gradient(135deg, #5855f7, #7c3aed);
}

.reset-result-btn .el-icon {
    margin-right: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .prediction-card {
        grid-template-columns: 1fr;
        gap: 20px;
    }

    .details-grid {
        grid-template-columns: 1fr;
    }

    .risk-level-card {
        min-width: auto;
        width: 100%;
    }

    .result-card {
        padding: 20px;
    }
}
</style>