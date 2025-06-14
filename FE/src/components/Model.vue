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

        <!-- 筛选弹窗 -->
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
                            <el-row :gutter="10">
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.ageMin" placeholder="Min" :min="0"
                                        :max="120" />
                                </el-col>
                                <el-col :span="2" class="text-center">-</el-col>
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.ageMax" placeholder="Max" :min="0"
                                        :max="120" />
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Hypertension">
                            <el-select v-model="filterForm.hypertension" placeholder="Select" clearable>
                                <el-option label="Yes" :value="1" />
                                <el-option label="No" :value="0" />
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
                            <el-row :gutter="10">
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.bmiMin" placeholder="Min" :min="0" :max="100"
                                        :precision="1" :step="0.1" />
                                </el-col>
                                <el-col :span="2" class="text-center">-</el-col>
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.bmiMax" placeholder="Max" :min="0" :max="100"
                                        :precision="1" :step="0.1" />
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="HbA1c Level">
                            <el-row :gutter="10">
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.HbA1c_levelMin" placeholder="Min" :min="0"
                                        :max="20" :precision="1" :step="0.1" />
                                </el-col>
                                <el-col :span="2" class="text-center">-</el-col>
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.HbA1c_levelMax" placeholder="Max" :min="0"
                                        :max="20" :precision="1" :step="0.1" />
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>

                    <el-col :span="12">
                        <el-form-item label="Blood Glucose">
                            <el-row :gutter="10">
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.blood_glucose_levelMin" placeholder="Min"
                                        :min="0" :max="500" />
                                </el-col>
                                <el-col :span="2" class="text-center">-</el-col>
                                <el-col :span="11">
                                    <el-input-number v-model="filterForm.blood_glucose_levelMax" placeholder="Max"
                                        :min="0" :max="500" />
                                </el-col>
                            </el-row>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="resetFilter" class="reset-button">Reset</el-button>
                    <el-button type="primary" @click="applyFilter" class="apply-button">Start</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import * as request from "../utils/request"
import { Filter } from '@element-plus/icons-vue'


const filterDialogVisible = ref(true)
const filterForm = reactive({
    gender: '',
    ageMin: null as number | null,
    ageMax: null as number | null,
    hypertension: null as number | null,
    heart_disease: null as number | null,
    smoking_history: '',
    bmiMin: null as number | null,
    bmiMax: null as number | null,
    HbA1c_levelMin: null as number | null,
    HbA1c_levelMax: null as number | null,
    blood_glucose_levelMin: null as number | null,
    blood_glucose_levelMax: null as number | null,
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

// 应用筛选条件
const applyFilter = async () => {
    await predict()
    filterDialogVisible.value = false
}

const predict = async () => {
    const params = buildFilterParams()
    const res = await request.get("/api/predict", params)
    console.log(res)
}

// 构建筛选参数
const buildFilterParams = () => {
    const params: Record<string, any> = {}
    // 添加筛选条件
    if (filterForm.gender) params.gender = filterForm.gender
    if (filterForm.ageMin !== null) params.ageMin = filterForm.ageMin
    if (filterForm.ageMax !== null) params.ageMax = filterForm.ageMax
    if (filterForm.hypertension !== null) params.hypertension = filterForm.hypertension
    if (filterForm.heart_disease !== null) params.heart_disease = filterForm.heart_disease
    if (filterForm.smoking_history) params.smoking_history = filterForm.smoking_history
    if (filterForm.bmiMin !== null) params.bmiMin = filterForm.bmiMin
    if (filterForm.bmiMax !== null) params.bmiMax = filterForm.bmiMax
    if (filterForm.HbA1c_levelMin !== null) params.HbA1c_levelMin = filterForm.HbA1c_levelMin
    if (filterForm.HbA1c_levelMax !== null) params.HbA1c_levelMax = filterForm.HbA1c_levelMax
    if (filterForm.blood_glucose_levelMin !== null) params.blood_glucose_levelMin = filterForm.blood_glucose_levelMin
    if (filterForm.blood_glucose_levelMax !== null) params.blood_glucose_levelMax = filterForm.blood_glucose_levelMax

    return params
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
    background-color: #1a1a2e;
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
</style>