<template>
  <view class="page-shell home-page">
    <view class="hero">
      <view class="hero-top">
        <view><view class="eyebrow">GOOD MORNING</view><view class="hello">上午好，{{ state.user.name }}</view></view>
        <image class="avatar" :src="state.user.avatar" mode="aspectFill" />
      </view>
      <view class="hero-copy"><view class="hero-title">今天，也要好好喝咖啡。</view><view class="hero-subtitle">在农大校园，给忙碌留一点香气。</view></view>
      <view class="bean bean-one"></view><view class="bean bean-two"></view>
    </view>

    <view class="store-card card" @click="goStores">
      <view class="store-pin">门店</view>
      <view class="store-copy"><view class="store-label">当前门店 · 营业中</view><view class="store-name">{{ currentStore.name }}</view><view class="store-meta">{{ formatDistance(currentStore.distance) }} · 预计 {{ currentStore.waitMinutes }} 分钟取餐</view></view>
      <view class="arrow">›</view>
    </view>

    <view class="order-panel section">
      <view class="section-heading"><view class="section-title">想怎么喝？</view><view class="section-link" @click="goOrders">查看订单</view></view>
      <view class="mode-grid">
        <view class="mode-card pickup" @click="startOrder('pickup')"><view class="mode-en">PICK UP</view><view><view class="mode-name">到店自取</view><view class="mode-desc">提前点，到店拿</view></view><view class="mode-go">→</view></view>
        <view class="mode-card dine-in" @click="startOrder('dineIn')"><view class="mode-en">DINE IN</view><view><view class="mode-name">到店堂食</view><view class="mode-desc">坐下来，慢慢喝</view></view><view class="mode-go">→</view></view>
      </view>
    </view>

    <view class="section">
      <view class="campaign-card">
        <view class="campaign-tag">CAMPUS SPECIAL</view><view class="campaign-title">农大同学专享</view><view class="campaign-copy">新用户满 20 减 5 元<br/>本地演示优惠已到账</view><view class="campaign-button" @click="startOrder('pickup')">立即尝鲜</view>
        <view class="campaign-value"><text>¥5</text><text>立减</text></view>
      </view>
    </view>

    <view class="section recommend-section">
      <view class="section-heading"><view class="section-title">今日人气</view><view class="section-link" @click="startOrder('pickup')">全部菜单</view></view>
      <scroll-view scroll-x class="recommend-scroll" :show-scrollbar="false">
        <view class="recommend-row">
          <view v-for="product in popularProducts" :key="product.id" class="recommend-card card" @click="openProduct(product.id)">
            <view class="recommend-visual"><image :src="product.image" mode="aspectFill" @error="failedImages[product.id] = true"/><view v-if="failedImages[product.id]" class="recommend-fallback">{{ product.fallback }}</view></view>
            <view class="recommend-name">{{ product.name }}</view><view class="recommend-bottom"><text class="price">{{ formatMoney(product.priceCents) }}</text><text class="recommend-add">+</text></view>
          </view>
        </view>
      </scroll-view>
    </view>

    <view class="member-card section" @click="goMine"><view><view class="member-kicker">LEVEL {{ state.user.level }} · 校园品鉴官</view><view class="member-title">{{ state.user.points }} 积分</view><view class="member-desc">再积 {{ state.user.nextLevelPoints - state.user.points }} 分升级</view></view><view class="member-progress"><view class="member-progress-value" :style="{ width: progress + '%' }"></view></view></view>
  </view>
</template>

<script setup>
import { computed, reactive } from 'vue'
import { PRODUCTS } from '@/data/catalog'
import { useAppStore } from '@/store/app'
import { formatDistance, formatMoney } from '@/utils/format'

const { state, currentStore, setOrderMode } = useAppStore()
const failedImages = reactive({})
const popularProducts = PRODUCTS.filter((product) => product.categoryId === 'popular')
const progress = computed(() => Math.min(100, Math.round(state.user.points / state.user.nextLevelPoints * 100)))
const startOrder = (mode) => { setOrderMode(mode); uni.switchTab({ url: '/pages/order/index' }) }
const goStores = () => uni.switchTab({ url: '/pages/shop/index' })
const goOrders = () => uni.navigateTo({ url: '/pages/my-order/index' })
const goMine = () => uni.switchTab({ url: '/pages/my/index' })
const openProduct = (id) => uni.navigateTo({ url: `/pages/item-detail/index?id=${id}` })
</script>

<style scoped lang="scss">
.home-page { overflow: hidden; }
.hero { position: relative; height: 430rpx; padding: calc(80rpx + env(safe-area-inset-top)) 34rpx 40rpx; overflow: hidden; color: white; background: radial-gradient(circle at 88% 12%, #4f7663 0, #214f3e 38%, #102f25 100%); }
.hero::after { content: ''; position: absolute; right: -90rpx; bottom: -150rpx; width: 360rpx; height: 360rpx; border: 2rpx solid rgba(255,255,255,.12); border-radius: 50%; }
.hero-top { position: relative; z-index: 2; display: flex; justify-content: space-between; align-items: center; }.eyebrow { color: var(--caramel-300); font-size: 20rpx; letter-spacing: 5rpx; }.hello { margin-top: 8rpx; font-size: 26rpx; }.avatar { width: 76rpx; height: 76rpx; border: 4rpx solid rgba(255,255,255,.5); border-radius: 50%; }
.hero-copy { position: relative; z-index: 2; margin-top: 62rpx; }.hero-title { font-size: 46rpx; font-weight: 750; letter-spacing: 1rpx; }.hero-subtitle { margin-top: 16rpx; color: rgba(255,255,255,.72); font-size: 24rpx; }
.bean { position: absolute; width: 48rpx; height: 70rpx; border-radius: 55% 45%; background: rgba(10,34,25,.3); transform: rotate(35deg); }.bean::after { content:''; position:absolute; left:23rpx; top:8rpx; width:2rpx; height:54rpx; background:rgba(255,255,255,.12); transform:rotate(-8deg); }.bean-one { right: 80rpx; top: 205rpx; }.bean-two { right: 165rpx; top: 290rpx; transform: rotate(-25deg) scale(.72); }
.store-card { position: relative; z-index: 3; display: flex; align-items: center; gap: 18rpx; margin: -54rpx 28rpx 0; padding: 26rpx; }.store-pin { display: flex; align-items:center; justify-content:center; width:64rpx; height:64rpx; border-radius:20rpx; color:white; background:var(--coffee-700); font-size:18rpx; font-weight:700; }.store-copy { min-width:0; flex:1; }.store-label { color:var(--green); font-size:20rpx; font-weight:650; }.store-name { margin-top:5rpx; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:28rpx; font-weight:700; }.store-meta { margin-top:6rpx; color:var(--muted); font-size:21rpx; }.arrow { color:var(--muted); font-size:42rpx; }
.mode-grid { display:grid; grid-template-columns:1fr 1fr; gap:18rpx; }.mode-card { min-height:180rpx; padding:26rpx 22rpx; border-radius:26rpx; position:relative; }.pickup { color:white; background:linear-gradient(145deg,#2c634e,#173f31); }.dine-in { color:#3b3128; background:linear-gradient(145deg,#f4e8d5,#e5c89c); }.mode-en{font-size:17rpx;letter-spacing:3rpx;opacity:.65}.mode-name { margin-top:28rpx; font-size:30rpx; font-weight:750; }.mode-desc { margin-top:7rpx; opacity:.72; font-size:21rpx; }.mode-go { position:absolute; right:20rpx; bottom:20rpx; font-size:30rpx; }
.campaign-card { position:relative; min-height:250rpx; padding:30rpx; overflow:hidden; border-radius:28rpx; color:#fff; background:linear-gradient(120deg,#6e7c57,#384a38); }.campaign-tag { color:#dce8c8; font-size:18rpx; letter-spacing:3rpx; }.campaign-title { margin-top:12rpx; font-size:36rpx; font-weight:750; }.campaign-copy { margin-top:10rpx; color:rgba(255,255,255,.75); font-size:22rpx; line-height:1.6; }.campaign-button { display:inline-flex; margin-top:18rpx; padding:12rpx 24rpx; border-radius:25rpx; color:#3f513e; background:#fff; font-size:22rpx; font-weight:700; }.campaign-value{position:absolute;right:38rpx;top:50%;transform:translateY(-42%);text-align:right}.campaign-value text{display:block}.campaign-value text:first-child{font-size:74rpx;font-weight:800;letter-spacing:-3rpx}.campaign-value text:last-child{margin-top:-6rpx;font-size:19rpx;letter-spacing:5rpx;color:rgba(255,255,255,.7)}
.recommend-section { padding-right:0; }.recommend-scroll { width:100%; white-space:nowrap; }.recommend-row { display:flex; gap:18rpx; padding:2rpx 28rpx 18rpx 0; }.recommend-card { display:inline-flex; flex-direction:column; width:250rpx; padding:14rpx; }.recommend-visual { position:relative; height:190rpx; overflow:hidden; border-radius:18rpx; background:var(--oat-100); }.recommend-visual image { width:100%; height:100%; }.recommend-fallback { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:82rpx; background:linear-gradient(145deg,#f4e8d9,#e3c8a7); }.recommend-name { margin-top:15rpx; overflow:hidden; text-overflow:ellipsis; font-size:26rpx; font-weight:700; }.recommend-bottom { display:flex; align-items:center; justify-content:space-between; margin-top:12rpx; }.recommend-add { display:flex; align-items:center; justify-content:center; width:42rpx; height:42rpx; border-radius:50%; color:#fff; background:var(--coffee-700); font-size:28rpx; }
.member-card { margin-bottom:20rpx; padding:30rpx; border-radius:28rpx; color:#fff; background:linear-gradient(120deg,#183d31,#35644f); }.member-kicker { color:var(--caramel-300); font-size:19rpx; letter-spacing:2rpx; }.member-title { margin-top:12rpx; font-size:34rpx; font-weight:750; }.member-desc { margin-top:5rpx; color:rgba(255,255,255,.65); font-size:21rpx; }.member-progress { height:8rpx; margin-top:22rpx; overflow:hidden; border-radius:4rpx; background:rgba(255,255,255,.18); }.member-progress-value { height:100%; border-radius:4rpx; background:var(--caramel-300); }
</style>
