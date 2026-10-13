<script setup>
import { computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useAppStore } from '@/store/app'
import { formatMoney } from '@/utils/format'

const store = useAppStore()
const d = computed(() => store.state.dashboard || {})

function load() { store.loadDashboard().catch(() => {}) }
onShow(() => {
  if (!store.state.user || store.state.user.role !== 'merchant') { uni.redirectTo({ url: '/pages/login/index' }); return }
  load()
})

const cards = computed(() => [
  { label: '待支付', value: d.value.pending_count || 0, color: '#8b8e97' },
  { label: '待接单', value: d.value.paid_count || 0, color: '#98642f' },
  { label: '制作中', value: d.value.making_count || 0, color: '#2458c8' },
  { label: '待取餐', value: d.value.ready_count || 0, color: '#0637c9' },
  { label: '已完成', value: d.value.completed_count || 0, color: '#2f8f4e' },
])
function back() { uni.navigateBack() }
</script>

<template>
  <view class="page-shell merchant-sub">
    <view class="sub-header">
      <button class="top-back" @click="back">‹</button>
      <text class="eyebrow">BUSINESS DASHBOARD</text>
      <text class="title">营业看板</text>
      <text class="subtitle">今日营业概览与订单状态分布</text>
    </view>

    <view class="hero">
      <view class="hero-card card">
        <text class="hero-number">{{ d.today_orders || 0 }}</text>
        <text class="hero-label">今日订单</text>
      </view>
      <view class="hero-card card">
        <text class="hero-number">{{ formatMoney(d.today_sales_cents || 0) }}</text>
        <text class="hero-label">今日流水</text>
      </view>
    </view>

    <view class="grid">
      <view v-for="c in cards" :key="c.label" class="grid-card card">
        <text class="grid-number" :style="{ color: c.color }">{{ c.value }}</text>
        <text class="grid-label">{{ c.label }}</text>
      </view>
    </view>

    <view class="note">数据按「今日 0 点至今」统计，实时刷新可在工作台查看。</view>
  </view>
</template>

<style scoped lang="scss">
.merchant-sub { padding-bottom: 80rpx; }
.sub-header { padding: calc(70rpx + env(safe-area-inset-top)) 30rpx 36rpx; background: linear-gradient(145deg, #0637c9, #071a62); color: #fff; }
.top-back { position: absolute; left: 26rpx; top: calc(24rpx + env(safe-area-inset-top)); width: 62rpx; height: 62rpx; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: rgba(255,255,255,.12); color: #fff; font-size: 46rpx; padding-bottom: 8rpx; }
.eyebrow, .title, .subtitle { display: block; }
.eyebrow { font-size: 17rpx; letter-spacing: 5rpx; color: #edcf91; }
.title { margin-top: 12rpx; font-size: 42rpx; font-weight: 800; }
.subtitle { margin-top: 8rpx; font-size: 21rpx; color: rgba(255,255,255,.65); }
.hero { display: flex; gap: 20rpx; margin: -30rpx 28rpx 0; }
.hero-card { flex: 1; display: flex; flex-direction: column; gap: 10rpx; padding: 34rpx 28rpx; }
.hero-number { font-size: 52rpx; font-weight: 850; color: var(--brand-900); }
.hero-label { font-size: 22rpx; color: var(--muted); }
.grid { display: flex; flex-wrap: wrap; padding: 26rpx 28rpx; }
.grid-card { width: calc(33.33% - 14rpx); margin-right: 20rpx; margin-bottom: 20rpx; display: flex; flex-direction: column; padding: 28rpx 24rpx; }
.grid-card:nth-child(3n) { margin-right: 0; }
.grid-number { margin-bottom: 10rpx; }
.grid-number { font-size: 44rpx; font-weight: 850; }
.grid-label { font-size: 22rpx; color: var(--muted); }
.note { margin: 10rpx 28rpx 0; font-size: 20rpx; color: var(--muted); text-align: center; }
</style>
