<script setup>
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import EmptyState from '@/component/EmptyState.vue'
import { useAppStore } from '@/store/app'
import { formatDateTime, formatMoney } from '@/utils/format'

const store = useAppStore()
const orderId = ref('')
const order = computed(() => store.findOrder(orderId.value))
const steps = [{ id: 'making', name: '制作中' }, { id: 'ready', name: '待取餐' }, { id: 'completed', name: '已完成' }]
const activeIndex = computed(() => Math.max(0, steps.findIndex((step) => step.id === order.value?.status)))

onLoad((query) => { orderId.value = query.id || store.state.orders[0]?.id || '' })

function advance() {
  if (!order.value || order.value.status === 'completed') return
  store.advanceOrder(order.value.id)
  uni.showToast({ title: order.value.statusText, icon: 'none' })
}
function reorder() {
  store.reorder(order.value.id)
  uni.switchTab({ url: '/pages/order/index' })
}
</script>

<template>
  <view class="page-shell settled-page">
    <template v-if="order">
      <view class="status-hero" :class="order.status">
        <button class="top-back" @click="uni.navigateBack()">‹</button>
        <text class="status-kicker">ORDER STATUS</text>
        <text class="status-title">{{ order.status === 'making' ? '咖啡正在制作' : order.status === 'ready' ? '可以来取餐啦' : '这一杯已完成' }}</text>
        <text class="status-copy">{{ order.status === 'making' ? `预计 ${order.pickupTime === '尽快取餐' ? '约 ' + store.currentStore.value.waitMinutes + ' 分钟' : order.pickupTime}` : order.status === 'ready' ? '请向店员出示取餐码' : '感谢光临，期待下一杯见' }}</text>
        <view class="pickup-code"><text>取餐码</text><text>{{ order.pickupCode }}</text></view>
      </view>

      <view class="section progress-section">
        <view class="progress-card card">
          <view class="progress-line"><view class="progress-fill" :style="{ width: `${activeIndex * 50}%` }" /></view>
          <view class="steps"><view v-for="(step,index) in steps" :key="step.id" class="step" :class="{ active: index <= activeIndex }"><text class="step-dot">{{ index < activeIndex ? '✓' : index + 1 }}</text><text>{{ step.name }}</text></view></view>
          <button v-if="order.status !== 'completed'" class="demo-advance" @click="advance">推进演示状态 →</button>
        </view>
      </view>

      <view class="section">
        <view class="section-heading"><text class="section-title">订单详情</text><text class="section-link">{{ formatDateTime(order.createdAt) }}</text></view>
        <view class="detail-card card">
          <view class="store-row"><view><text class="store-name">{{ order.storeName }}</text><text class="order-no">订单号 {{ order.id }}</text></view><text class="mode">{{ order.mode === 'pickup' ? '到店自取' : '门店堂食' }}</text></view>
          <view v-for="item in order.items" :key="item.key" class="order-item"><image class="item-image" :src="item.image" mode="aspectFill" /><view class="item-main"><text>{{ item.name }} × {{ item.quantity }}</text><text>{{ item.selectedOptions.map(option => option.name).join(' · ') || '标准制作' }}</text></view><text>{{ formatMoney(item.unitPriceCents * item.quantity) }}</text></view>
          <view class="bill"><view><text>商品金额</text><text>{{ formatMoney(order.subtotalCents) }}</text></view><view><text>优惠</text><text>-{{ formatMoney(order.discountCents) }}</text></view><view class="bill-total"><text>实付</text><text>{{ formatMoney(order.totalCents) }}</text></view></view>
        </view>
      </view>

      <view class="section actions"><button class="primary-button" @click="reorder">再来一单</button><button class="ghost-button" @click="uni.switchTab({ url: '/pages/home/index' })">返回首页</button></view>
    </template>
    <EmptyState v-else title="没有找到订单" description="去点单页挑一杯喜欢的咖啡吧" action-text="去点单" @action="uni.switchTab({ url: '/pages/order/index' })" />
  </view>
</template>

<style scoped lang="scss">
.settled-page{padding-bottom:60rpx}.status-hero{position:relative;padding:calc(105rpx + env(safe-area-inset-top)) 30rpx 100rpx;text-align:center;color:white;background:radial-gradient(circle at 50% 8%,#9b6d4f,#3c281f 62%)}.top-back{position:absolute;left:26rpx;top:calc(22rpx + env(safe-area-inset-top));width:66rpx;height:66rpx;display:flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(255,255,255,.12);color:white;font-size:48rpx;padding-bottom:8rpx}.status-hero.ready{background:radial-gradient(circle at 50% 8%,#789379,#304535 62%)}.status-hero.completed{background:radial-gradient(circle at 50% 8%,#827c77,#393532 62%)}.status-kicker,.status-title,.status-copy{display:block}.status-kicker{font-size:18rpx;letter-spacing:5rpx;color:#dfbd91}.status-title{margin-top:18rpx;font-size:46rpx;font-weight:800}.status-copy{margin-top:12rpx;font-size:24rpx;color:rgba(255,255,255,.7)}.pickup-code{width:260rpx;margin:38rpx auto 0;padding:20rpx;border:1rpx solid rgba(255,255,255,.25);border-radius:20rpx;background:rgba(255,255,255,.08)}.pickup-code text{display:block}.pickup-code text:first-child{font-size:20rpx;color:rgba(255,255,255,.65)}.pickup-code text:last-child{margin-top:5rpx;font-size:64rpx;font-weight:850;letter-spacing:9rpx}.progress-section{margin-top:-48rpx}.progress-card{padding:30rpx 28rpx}.progress-line{position:relative;height:5rpx;margin:24rpx 60rpx -27rpx;background:var(--line)}.progress-fill{height:100%;background:var(--green);transition:width .3s}.steps{position:relative;display:flex;justify-content:space-between}.step{display:flex;flex-direction:column;align-items:center;gap:10rpx;color:var(--muted);font-size:20rpx}.step-dot{width:48rpx;height:48rpx;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#eee8e0;border:5rpx solid white;font-weight:700}.step.active{color:var(--coffee-800);font-weight:700}.step.active .step-dot{background:var(--green);color:white}.demo-advance{margin:28rpx auto 0;color:var(--coffee-700);font-size:22rpx;text-decoration:underline}.detail-card{padding:0 24rpx}.store-row{display:flex;align-items:flex-start;justify-content:space-between;padding:25rpx 0;border-bottom:1rpx solid var(--line)}.store-name,.order-no{display:block}.store-name{font-size:27rpx;font-weight:750}.order-no{margin-top:7rpx;color:var(--muted);font-size:19rpx}.mode{padding:8rpx 13rpx;border-radius:10rpx;background:var(--oat-100);font-size:20rpx;color:var(--coffee-700)}.order-item{display:flex;align-items:center;gap:14rpx;padding:21rpx 0;border-bottom:1rpx solid var(--line);font-size:23rpx}.item-image{width:58rpx;height:58rpx;border-radius:14rpx}.item-main{flex:1}.item-main text{display:block}.item-main text:first-child{font-weight:650}.item-main text:last-child{margin-top:5rpx;color:var(--muted);font-size:19rpx}.bill{padding:16rpx 0}.bill>view{display:flex;justify-content:space-between;padding:9rpx 0;color:var(--muted);font-size:22rpx}.bill .bill-total{margin-top:8rpx;padding-top:18rpx;border-top:1rpx solid var(--line);font-size:28rpx;font-weight:800;color:var(--coffee-900)}.actions{display:grid;grid-template-columns:1fr 1fr;gap:14rpx}.ghost-button{display:flex;align-items:center;justify-content:center;border:1rpx solid var(--coffee-700);border-radius:46rpx;color:var(--coffee-700);font-size:27rpx}
</style>
