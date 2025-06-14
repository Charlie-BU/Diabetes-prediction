<template>
    <div class="app-container">
        <!-- 左侧菜单栏 -->
        <div class="sidebar">
            <div class="logo-container">
                <h2 class="logo">DISEASE PREDICTION</h2>
            </div>
            <div class="menu">
                <div class="menu-item" :class="{ active: activeComponent === 'table' }"
                    @click="activeComponent = 'table'">
                    <el-icon>
                        <DataLine />
                    </el-icon>
                    <span>Data Browser</span>
                </div>
                <div class="menu-item" :class="{ active: activeComponent === 'Diabetes' }"
                    @click="activeComponent = 'Diabetes'">
                    <el-icon>
                        <Monitor />
                    </el-icon>
                    <span>Diabetes Prediction</span>
                </div>
                <div class="menu-item" :class="{ active: activeComponent === 'Heart Disease' }"
                    @click="activeComponent = 'Heart Disease'">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                    <span>Heart Disease Prediction</span>
                </div>
                <div class="menu-item" :class="{ active: activeComponent === 'Hypertension' }"
                    @click="activeComponent = 'Hypertension'">
                    <el-icon>
                        <TrendCharts />
                    </el-icon>
                    <span>Hypertension Prediction</span>
                </div>
            </div>
        </div>

        <!-- 主内容区域 -->
        <div class="main-content">
            <div class="header">
                <h1>{{ activeComponent === 'table' ? 'Data Browser' : `${activeComponent} Prediction` }}</h1>
            </div>
            <div class="content-area">
                <Table v-if="activeComponent === 'table'" />
                <Diabetes v-else-if="activeComponent === 'Diabetes'" />
                <HeartDisease v-else-if="activeComponent === 'Heart Disease'" />
                <Hypertension v-else-if="activeComponent === 'Hypertension'" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Table from './components/Table.vue'
import Diabetes from './components/Diabetes.vue'
import Hypertension from './components/Hypertension.vue'
import HeartDisease from './components/HeartDisease.vue'
import { DataLine, Monitor, Promotion, TrendCharts } from '@element-plus/icons-vue'

const activeComponent = ref('table')
</script>

<style>
:root {
    --primary-color: #8a2be2;
    /* 紫色主题色 */
    --secondary-color: #9370db;
    --dark-bg: #1a1a2e;
    --darker-bg: #16213e;
    --accent-color: #ff6b6b;
    --text-color: #f0f0f0;
    --menu-hover: rgba(147, 112, 219, 0.2);
    --menu-active: rgba(147, 112, 219, 0.4);
    --card-bg: rgba(26, 26, 46, 0.7);
    --border-radius: 12px;
    --transition-speed: 0.3s;
}

body {
    margin: 0;
    padding: 0;
    background-color: var(--dark-bg);
    color: var(--text-color);
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

.app-container {
    display: flex;
    min-height: 100vh;
    background: linear-gradient(-45deg, #6a0dad, #9370db, #4b0082, #8a2be2);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
}


@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.sidebar {
    width: 240px;
    background-color: var(--darker-bg);
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    transition: all var(--transition-speed);
    z-index: 10;
}

.logo-container {
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
    color: var(--primary-color);
    margin: 0;
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 10px rgba(138, 43, 226, 0.3);
}

.menu {
    padding: 20px 0;
}

.menu-item {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    color: var(--text-color);
    cursor: pointer;
    transition: all var(--transition-speed);
    margin: 8px 10px;
    border-radius: var(--border-radius);
}

.menu-item:hover {
    background-color: var(--menu-hover);
    transform: translateX(5px);
}

.menu-item.active {
    background-color: var(--menu-active);
    border-left: 4px solid var(--primary-color);
}

.menu-item .el-icon {
    margin-right: 10px;
    font-size: 1.2rem;
    color: var(--secondary-color);
}

.menu-item span {
    font-size: 1rem;
    font-weight: 500;
}

.main-content {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: linear-gradient(135deg, rgba(138, 43, 226, 0.05), rgba(147, 112, 219, 0.1));
}

.header {
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--secondary-color);
}

.header h1 {
    font-size: 2rem;
    color: var(--text-color);
    margin: 0;
    font-weight: 600;
    position: relative;
    display: inline-block;
}

.header h1::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 50%;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-color), transparent);
    border-radius: 3px;
}

.content-area {
    background-color: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 20px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease-out;
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

/* 响应式设计 */
@media (max-width: 768px) {
    .app-container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        height: auto;
    }

    .menu {
        display: flex;
        padding: 10px;
    }

    .menu-item {
        margin: 0 5px;
        padding: 8px 12px;
    }
}
</style>
