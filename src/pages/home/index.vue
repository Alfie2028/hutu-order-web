<template>
  <view class="page-shell home-page">
    <view class="hero">
      <view class="hero-top">
        <view><view class="eyebrow">CAMPUS DINING</view><view class="hello">欢迎使用校园点餐服务</view></view>
        <image class="avatar" :src="state.user.avatar" mode="aspectFill" />
      </view>
      <view class="hero-copy"><view class="hero-title">多档口聚合<br/>一站式校园点餐</view><view class="hero-subtitle">餐品现制 · 支持自取与堂食</view><view class="hero-button" @click="startOrder('pickup')">开始点餐</view></view>
    </view>

    <view class="store-card card" @click="goStores">
      <view class="store-pin">餐厅</view>
      <view class="store-copy"><view class="store-label">当前餐厅 · 营业中</view><view class="store-name">{{ currentStore.name }}</view><view class="store-meta">{{ formatDistance(currentStore.distance) }} · {{ STALLS.length }} 个档口 · 预计 {{ currentStore.waitMinutes }} 分钟取餐</view></view>
      <view class="arrow">›</view>
    </view>

    <view class="order-panel section">
      <view class="section-heading"><view class="section-title">选择取餐方式</view><view class="section-link" @click="goOrders">查看订单</view></view>
      <view class="mode-grid">
        <view class="mode-card pickup" @click="startOrder('pickup')"><view class="mode-icon">取</view><view><view class="mode-name">到店自取</view><view class="mode-desc">提前下单，到店即取</view></view><view class="mode-go">›</view></view>
        <view class="mode-card dine-in" @click="startOrder('dineIn')"><view class="mode-icon">享</view><view><view class="mode-name">到店堂食</view><view class="mode-desc">到店下单，店内用餐</view></view><view class="mode-go">›</view></view>
      </view>
    </view>

    <view class="section stall-section">
      <view class="section-heading"><view class="section-title">档口导航</view><view class="section-link" @click="startOrder('pickup')">全部餐品</view></view>
      <view class="stall-grid">
        <view v-for="stall in stallEntries" :key="stall.id" class="stall-card" @click="startOrder('pickup', stall.id)">
          <image :src="stall.image" mode="aspectFit" />
          <view><text class="stall-name">{{ stall.name }}</text><text class="stall-desc">{{ stall.description }}</text></view>
        </view>
      </view>
    </view>

    <view class="section">
      <view class="campaign-card">
        <view class="campaign-tag">NEW MEMBER OFFER</view><view class="campaign-title">新用户优惠</view><view class="campaign-copy">单笔订单满 20 元<br/>结算时可减 5 元</view><view class="campaign-button" @click="startOrder('pickup')">前往点单</view>
        <view class="campaign-value"><text>¥5</text><text>立减</text></view>
      </view>
    </view>

    <view class="section recommend-section">
      <view class="section-heading"><view class="section-title">人气餐品</view><view class="section-link" @click="startOrder('pickup')">查看菜单</view></view>
      <scroll-view scroll-x class="recommend-scroll" :show-scrollbar="false">
        <view class="recommend-row">
          <view v-for="product in popularProducts" :key="product.id" class="recommend-card card" @click="openProduct(product.id)">
            <view class="recommend-visual"><image :src="product.image" mode="aspectFit" @error="failedImages[product.id] = true"/><view v-if="failedImages[product.id]" class="recommend-fallback">{{ product.fallback }}</view></view>
            <view class="recommend-name">{{ product.name }}</view><view class="recommend-bottom"><text class="price">{{ formatMoney(product.priceCents) }}</text><text class="recommend-add">+</text></view>
          </view>
        </view>
      </scroll-view>
    </view>

    <view class="member-card section" @click="goMine"><view><view class="member-kicker">LEVEL {{ state.user.level }} · 会员等级</view><view class="member-title">{{ state.user.points }} 会员积分</view><view class="member-desc">还需 {{ state.user.nextLevelPoints - state.user.points }} 积分升级</view></view><view class="member-progress"><view class="member-progress-value" :style="{ width: progress + '%' }"></view></view></view>
  </view>
</template>

<script setup>
import { computed, reactive } from 'vue'
import { PRODUCTS, STALLS } from '@/data/catalog'
import { useAppStore } from '@/store/app'
import { formatDistance, formatMoney } from '@/utils/format'

const { state, currentStore, setOrderMode, setStall } = useAppStore()
const failedImages = reactive({})
const popularProducts = PRODUCTS.filter((product) => product.featured)
const stallEntries = STALLS.map((stall) => ({ ...stall, image: PRODUCTS.find((product) => product.stallId === stall.id)?.image }))
const progress = computed(() => Math.min(100, Math.round(state.user.points / state.user.nextLevelPoints * 100)))
const startOrder = (mode, stallId = '') => { setOrderMode(mode); if (stallId) setStall(stallId); uni.switchTab({ url: '/pages/order/index' }) }
const goStores = () => uni.switchTab({ url: '/pages/shop/index' })
const goOrders = () => uni.navigateTo({ url: '/pages/my-order/index' })
const goMine = () => uni.switchTab({ url: '/pages/my/index' })
const openProduct = (id) => uni.navigateTo({ url: `/pages/item-detail/index?id=${id}` })
</script>

<style scoped lang="scss">
.home-page{overflow:hidden;background:#f6f7f9}.hero{position:relative;height:470rpx;padding:calc(52rpx + env(safe-area-inset-top)) 34rpx 40rpx;overflow:hidden;color:var(--ink);background:#fff url('/static/image/hero-campus-dining.webp') right center/cover no-repeat}.hero::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.99) 0%,rgba(255,255,255,.94) 34%,rgba(255,255,255,.58) 54%,rgba(255,255,255,0) 76%)}.hero-top{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center}.eyebrow{color:var(--brand);font-size:18rpx;font-weight:800;letter-spacing:4rpx}.hello{margin-top:7rpx;color:#777b85;font-size:22rpx}.avatar{width:66rpx;height:66rpx;border:3rpx solid #fff;border-radius:50%;box-shadow:0 6rpx 20rpx rgba(16,38,111,.14)}.hero-copy{position:relative;z-index:2;margin-top:55rpx}.hero-title{color:#10266f;font-size:47rpx;font-weight:850;line-height:1.2;letter-spacing:1rpx}.hero-subtitle{margin-top:13rpx;color:#7b7e87;font-size:22rpx}.hero-button{display:inline-flex;margin-top:23rpx;padding:13rpx 28rpx;border-radius:8rpx;color:#fff;background:var(--brand);font-size:21rpx;font-weight:750;box-shadow:0 9rpx 22rpx rgba(6,55,201,.22)}
.store-card{position:relative;z-index:3;display:flex;align-items:center;gap:18rpx;margin:-30rpx 28rpx 0;padding:23rpx 25rpx}.store-pin{display:flex;align-items:center;justify-content:center;width:62rpx;height:62rpx;border-radius:18rpx;color:#fff;background:var(--brand);font-size:18rpx;font-weight:750}.store-copy{min-width:0;flex:1}.store-label{color:var(--brand);font-size:18rpx;font-weight:700}.store-name{margin-top:5rpx;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:26rpx;font-weight:760}.store-meta{margin-top:6rpx;color:var(--muted);font-size:19rpx}.arrow{color:var(--brand);font-size:40rpx}
.mode-grid{display:grid;grid-template-columns:1fr 1fr;gap:18rpx}.mode-card{position:relative;min-height:194rpx;padding:22rpx;border:1rpx solid #e7eaf1;border-radius:24rpx;background:#fff;box-shadow:0 8rpx 24rpx rgba(18,39,92,.05)}.pickup,.dine-in{color:var(--ink);background:#fff}.mode-icon{display:flex;align-items:center;justify-content:center;width:64rpx;height:64rpx;border-radius:18rpx;color:#fff;background:linear-gradient(145deg,#0b4ee7,#062b9e);font-size:27rpx;font-weight:850;box-shadow:0 8rpx 18rpx rgba(6,55,201,.2)}.dine-in .mode-icon{color:#785719;background:linear-gradient(145deg,#f4d99e,#d6a95c);box-shadow:0 8rpx 18rpx rgba(199,149,69,.18)}.mode-name{margin-top:16rpx;font-size:27rpx;font-weight:800}.mode-desc{margin-top:5rpx;color:var(--muted);font-size:18rpx}.mode-go{position:absolute;right:18rpx;top:30rpx;color:#a1a5ae;font-size:32rpx}
.campaign-card{position:relative;min-height:232rpx;padding:28rpx;overflow:hidden;border:1rpx solid #e5e9f2;border-radius:26rpx;color:var(--ink);background:linear-gradient(120deg,#fff 0%,#f7f9ff 72%,#edf2ff 100%);box-shadow:0 9rpx 28rpx rgba(16,40,101,.06)}.campaign-card::after{content:'';position:absolute;right:-55rpx;bottom:-80rpx;width:250rpx;height:250rpx;border:32rpx solid rgba(6,55,201,.08);border-radius:50%}.campaign-tag{color:var(--brand);font-size:17rpx;font-weight:800;letter-spacing:3rpx}.campaign-title{margin-top:10rpx;color:#10266f;font-size:34rpx;font-weight:850}.campaign-copy{margin-top:8rpx;color:#858891;font-size:20rpx;line-height:1.55}.campaign-button{display:inline-flex;margin-top:15rpx;padding:10rpx 22rpx;border-radius:7rpx;color:#fff;background:#d21f28;font-size:20rpx;font-weight:750}.campaign-value{position:absolute;z-index:2;right:38rpx;top:50%;transform:translateY(-42%);text-align:right}.campaign-value text{display:block}.campaign-value text:first-child{color:#d21f28;font-size:70rpx;font-weight:850;letter-spacing:-3rpx}.campaign-value text:last-child{margin-top:-6rpx;color:#10266f;font-size:18rpx;font-weight:700;letter-spacing:5rpx}
.recommend-section{padding-right:0}.recommend-scroll{width:100%;white-space:nowrap}.recommend-row{display:flex;gap:18rpx;padding:2rpx 28rpx 18rpx 0}.recommend-card{display:inline-flex;flex-direction:column;width:244rpx;padding:14rpx}.recommend-visual{position:relative;height:190rpx;overflow:visible;border-radius:50%;background:linear-gradient(145deg,#f7f8fb,#edf1f8)}.recommend-visual image{width:100%;height:100%;transform:scale(1.04)}.recommend-fallback{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:82rpx;background:#f2f4f8}.recommend-name{margin-top:15rpx;overflow:hidden;text-overflow:ellipsis;font-size:25rpx;font-weight:750}.recommend-bottom{display:flex;align-items:center;justify-content:space-between;margin-top:12rpx}.recommend-add{display:flex;align-items:center;justify-content:center;width:42rpx;height:42rpx;border-radius:13rpx;color:#fff;background:var(--brand);font-size:28rpx}.member-card{margin-bottom:20rpx;padding:30rpx;border-radius:28rpx;color:#fff;background:linear-gradient(120deg,#071a62,#123aa8)}.member-kicker{color:var(--caramel-300);font-size:19rpx;letter-spacing:2rpx}.member-title{margin-top:12rpx;font-size:34rpx;font-weight:750}.member-desc{margin-top:5rpx;color:rgba(255,255,255,.65);font-size:21rpx}.member-progress{height:8rpx;margin-top:22rpx;overflow:hidden;border-radius:4rpx;background:rgba(255,255,255,.18)}.member-progress-value{height:100%;border-radius:4rpx;background:var(--caramel-300)}
.hero{background-image:url('/static/image/hero-campus-dining.webp')}
.stall-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14rpx}.stall-card{display:flex;align-items:center;min-width:0;min-height:128rpx;padding:12rpx 14rpx;border:1rpx solid #e6e9f0;border-radius:20rpx;background:#fff;box-shadow:0 7rpx 20rpx rgba(17,38,91,.045)}.stall-card image{width:84rpx;height:84rpx;flex:0 0 84rpx;margin-right:11rpx;border-radius:50%;background:#f2f4f8}.stall-card>view{min-width:0}.stall-name,.stall-desc{display:block}.stall-name{font-size:22rpx;font-weight:780;white-space:nowrap}.stall-desc{margin-top:5rpx;overflow:hidden;color:var(--muted);font-size:16rpx;text-overflow:ellipsis;white-space:nowrap}
</style>
