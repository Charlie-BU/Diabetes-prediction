<template>
    <div class="patient-table-container">
        <div class="table-header">
            <h2>Patient Information</h2>
            <el-button type="primary" @click="openFilterDialog" class="filter-button">
                <el-icon>
                    <Filter />
                </el-icon>
                Filter
            </el-button>
        </div>

        <el-table :data="patients" style="width: 100%" class="custom-table" :header-cell-style="headerCellStyle"
            :cell-style="cellStyle" :row-class-name="tableRowClassName" border>
            <el-table-column prop="id" label="ID" width="90" />
            <el-table-column prop="gender" label="Gender" width="120" />
            <el-table-column prop="age" label="Age" min-width="80" />
            <el-table-column prop="hypertension" label="Hypertension" min-width="120">
                <template #default="scope">
                    <el-tag :type="scope.row.hypertension ? 'danger' : 'success'" effect="dark" size="medium"
                        class="status-tag">
                        {{ scope.row.hypertension ? 'Yes' : 'No' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="heart_disease" label="Heart Disease" width="120">
                <template #default="scope">
                    <el-tag :type="scope.row.heart_disease ? 'danger' : 'success'" effect="dark" size="small"
                        class="status-tag">
                        {{ scope.row.heart_disease ? 'Yes' : 'No' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="smoking_history" label="Smoking History" width="150" />
            <el-table-column prop="bmi" label="BMI" width="100" />
            <el-table-column prop="HbA1c_level" label="HbA1c Level" width="120" />
            <el-table-column prop="blood_glucose_level" label="Blood Glucose Level" width="180" />
            <el-table-column prop="diabetes" label="Diabetes" width="120">
                <template #default="scope">
                    <el-tag :type="scope.row.diabetes ? 'danger' : 'success'" effect="dark" size="small"
                        class="status-tag">
                        {{ scope.row.diabetes ? 'Yes' : 'No' }}
                    </el-tag>
                </template>
            </el-table-column>
        </el-table>

        <!-- 分页组件 -->
        <div class="pagination-container">
            <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total"
                @size-change="handleSizeChange" @current-change="handleCurrentChange" background
                class="custom-pagination" />
        </div>

        <!-- 筛选弹窗 -->
        <el-dialog v-model="filterDialogVisible" title="Filter" width="1000" class="filter-dialog"
            :close-on-click-modal="false">
            <el-form :model="filterForm" label-width="120px" label-position="left">
                <el-row :gutter="20">
                    <!-- 性别筛选 -->
                    <el-col :span="12">
                        <el-form-item label="Gender">
                            <el-select v-model="filterForm.gender" placeholder="Select Gender" clearable>
                                <el-option label="Male" value="Male" />
                                <el-option label="Female" value="Female" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <!-- 年龄筛选 -->
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

                    <!-- 高血压筛选 -->
                    <el-col :span="12">
                        <el-form-item label="Hypertension">
                            <el-select v-model="filterForm.hypertension" placeholder="Select" clearable>
                                <el-option label="Yes" :value="1" />
                                <el-option label="No" :value="0" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <!-- 心脏病筛选 -->
                    <el-col :span="12">
                        <el-form-item label="Heart Disease">
                            <el-select v-model="filterForm.heart_disease" placeholder="Select" clearable>
                                <el-option label="Yes" :value="1" />
                                <el-option label="No" :value="0" />
                            </el-select>
                        </el-form-item>
                    </el-col>

                    <!-- 吸烟史筛选 -->
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

                    <!-- BMI筛选 -->
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

                    <!-- HbA1c筛选 -->
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

                    <!-- 糖尿病筛选 -->
                    <el-col :span="12">
                        <el-form-item label="Diabetes">
                            <el-select v-model="filterForm.diabetes" placeholder="Select" clearable>
                                <el-option label="Yes" :value="1" />
                                <el-option label="No" :value="0" />
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="resetFilter" class="reset-button">Reset</el-button>
                    <el-button type="primary" @click="applyFilter" class="apply-button">Apply</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import * as request from "../utils/request"
import { Filter } from '@element-plus/icons-vue'

interface Patient {
    id: number
    gender: string
    age: number
    hypertension: number
    heart_disease: number
    smoking_history: string
    bmi: number
    HbA1c_level: number
    blood_glucose_level: number
    diabetes: number
}

// 分页相关状态
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 患者数据
const patients = ref<Patient[]>([])

// 筛选弹窗相关
const filterDialogVisible = ref(false)
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
    diabetes: null as number | null
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
    currentPage.value = 1 // 重置到第一页
    await getPatientData()
    filterDialogVisible.value = false
}

onMounted(async () => {
    await getPatientData();
})

// 处理页码变化
const handleCurrentChange = async (page: number) => {
    currentPage.value = page
    await getPatientData()
}

// 处理每页数量变化
const handleSizeChange = async (size: number) => {
    pageSize.value = size
    currentPage.value = 1 // 重置到第一页
    await getPatientData()
}

// 构建筛选参数
const buildFilterParams = () => {
    const params: Record<string, any> = {
        page: currentPage.value,
        pageSize: pageSize.value
    }

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
    if (filterForm.diabetes !== null) params.diabetes = filterForm.diabetes

    return params
}

const getPatientData = async () => {
    try {
        const params = buildFilterParams()
        const res = await request.get("/api/getPatientData", params)
        if (res.status !== 200) {
            console.error(res.message);
            return;
        }
        patients.value = res.patients;
        total.value = res.total || res.patients.length; // 设置总数据量
    } catch (error) {
        console.error(error)
    }
}

// 表头样式
const headerCellStyle = {
    backgroundColor: '#2a2a40',
    color: '#ffffff',
    fontWeight: '600',
    borderBottom: '2px solid #3a3a50',
    fontSize: '14px',
    padding: '12px 8px',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    "text-align": "center"
}

// 单元格样式
const cellStyle = {
    backgroundColor: '#1a1a2e',
    color: '#e0e0e0',
    borderBottom: '1px solid #2a2a40',
    transition: 'all 0.3s',
    padding: '10px 8px',
    'text-align': "center",
}

// 行样式
const tableRowClassName = ({ rowIndex }: { rowIndex: number }) => {
    return rowIndex % 2 === 0 ? 'even-row' : 'odd-row'
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
    box-shadow: none;
}

:deep(.filter-dialog .el-input .el-input__wrapper) {
    background-color: transparent !important;
    box-shadow: none;
}

:deep(.filter-dialog .el-input-number .el-input__wrapper) {
    background-color: transparent !important;
    box-shadow: none;
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