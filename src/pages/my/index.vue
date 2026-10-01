<script setup>
import { computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import ProductCard from '@/component/ProductCard.vue'
import { COUPONS, PRODUCTS } from '@/data/catalog'
import { useAppStore } from '@/store/app'

const store = useAppStore()
const favorites = computed(() => PRODUCTS.filter((product) => store.state.favoriteIds.includes(product.id)))
const availableCoupons = computed(() => COUPONS.filter((coupon) => store.state.couponIds.includes(coupon.id)))
const activeOrder = computed(() => store.state.orders.find((order) => ['making','ready'].includes(order.status)))
const levelProgress = computed(() => Math.min(100, Math.round(store.state.user.points / store.state.user.nextLevelPoints * 100)))
onShow(() => {})

function openProduct(product) { uni.navigateTo({ url: `/pages/item-detail/index?id=${product.id}` }) }
function quickAdd(product) { product.options.length ? openProduct(product) : (store.addToCart(product.id), uni.showToast({ title: '已加入购物袋', icon: 'success' })) }
function showFeature(message) { uni.showToast({ title: message, icon: 'none' }) }
</script>

<template>
  <view class="page-shell my-page">
    <view class="profile-hero">
      <view class="brand-line"><text>MEMBER CENTER</text><button @click="uni.navigateTo({ url: '/pages/setting/index' })">设置</button></view>
      <view class="profile-row">
        <view class="avatar">学</view>
        <view class="profile-main"><text class="user-name">{{ store.state.user.name }}</text><text class="user-title">{{ store.state.user.title }} · LV.{{ store.state.user.level }}</text></view>
        <view class="points"><text>{{ store.state.user.points }}</text><text>成长豆</text></view>
      </view>
      <view class="level-bar"><view :style="{ width: `${levelProgress}%` }" /></view>
      <text class="level-copy">距离下一等级还差 {{ Math.max(0, store.state.user.nextLevelPoints - store.state.user.points) }} 成长豆</text>
    </view>

    <view class="quick-panel card">
      <view class="quick-item" @click="uni.navigateTo({ url: '/pages/my-order/index' })"><text class="quick-number">{{ store.state.orders.length }}</text><text>全部订单</text></view>
      <view class="quick-item" @click="showFeature('优惠券已在结算页可用')"><text class="quick-number">{{ availableCoupons.length }}</text><text>优惠券</text></view>
      <view class="quick-item" @click="showFeature('收藏商品见下方')"><text class="quick-number">{{ favorites.length }}</text><text>我的收藏</text></view>
      <view class="quick-item" @click="showFeature('成长体系为本地演示')"><text class="quick-number">{{ store.state.user.level }}</text><text>会员等级</text></view>
    </view>

    <view v-if="activeOrder" class="section">
      <view class="section-heading"><text class="section-title">进行中的订单</text><text class="section-link" @click="uni.navigateTo({ url: '/pages/my-order/index' })">全部订单</text></view>
      <view class="active-order card" @click="uni.navigateTo({ url: `/pages/settled/index?id=${activeOrder.id}` })">
        <view class="active-symbol">{{ activeOrder.status === 'ready' ? '待取' : '制作' }}</view>
        <view class="active-main"><text>{{ activeOrder.statusText }} · 取餐码 {{ activeOrder.pickupCode }}</text><text>{{ activeOrder.storeName }}</text></view>
        <text class="arrow">›</text>
      </view>
    </view>

    <view class="section">
      <view class="section-heading"><text class="section-title">常用服务</text></view>
      <view class="services card">
        <view class="service-item" @click="uni.navigateTo({ url: '/pages/my-order/index' })"><text>订单记录</text><text>查看历史订单</text></view>
        <view class="service-item" @click="uni.switchTab({ url: '/pages/shop/index' })"><text>门店地图</text><text>查找附近门店</text></view>
        <view class="service-item" @click="showFeature('开票服务为展示入口')"><text>申请开票</text><text>管理开票信息</text></view>
        <view class="service-item" @click="showFeature('客服工作时间 08:00-22:00')"><text>帮助客服</text><text>服务时间 08:00-22:00</text></view>
      </view>
    </view>

    <view class="section favorite-section">
      <view class="section-heading"><text class="section-title">我的常点</text><text class="section-link">{{ favorites.length }} 款收藏</text></view>
      <view v-if="favorites.length" class="favorite-list"><ProductCard v-for="product in favorites" :key="product.id" :product="product" @open="openProduct" @add="quickAdd" /></view>
      <view v-else class="empty-favorite card">还没有收藏，去点单页发现喜欢的口味吧</view>
    </view>

    <view class="footer-mark">本地交互原型 · 数据仅作展示</view>
  </view>
</template>

<style scoped lang="scss">
.my-page{padding-bottom:60rpx}.profile-hero{padding:calc(54rpx + env(safe-area-inset-top)) 30rpx 74rpx;color:white;background:linear-gradient(145deg,#302019,#6e4c3a)}.brand-line{display:flex;align-items:center;justify-content:space-between;color:var(--caramel-300);font-size:18rpx;letter-spacing:5rpx}.brand-line button{width:auto;height:52rpx;padding:0 20rpx;display:flex;align-items:center;justify-content:center;border:1rpx solid rgba(255,255,255,.25);border-radius:26rpx;background:transparent;color:white;font-size:19rpx;letter-spacing:1rpx}.profile-row{display:flex;align-items:center;margin-top:34rpx}.avatar{width:104rpx;height:104rpx;display:flex;align-items:center;justify-content:center;border:2rpx solid rgba(255,255,255,.45);border-radius:36rpx;background:#d4ad7e;color:#4a3025;font-size:43rpx;font-weight:850}.profile-main{flex:1;margin-left:22rpx}.user-name,.user-title,.points text{display:block}.user-name{font-size:38rpx;font-weight:800}.user-title{margin-top:7rpx;color:rgba(255,255,255,.64);font-size:21rpx}.points{text-align:right}.points text:first-child{font-size:38rpx;font-weight:800}.points text:last-child{margin-top:3rpx;font-size:19rpx;color:rgba(255,255,255,.6)}.level-bar{height:8rpx;margin-top:30rpx;overflow:hidden;border-radius:8rpx;background:rgba(255,255,255,.15)}.level-bar view{height:100%;border-radius:8rpx;background:linear-gradient(90deg,#c99457,#f0d7b2)}.level-copy{display:block;margin-top:10rpx;text-align:right;font-size:18rpx;color:rgba(255,255,255,.55)}.quick-panel{display:grid;grid-template-columns:repeat(4,1fr);margin:-38rpx 28rpx 0;padding:24rpx 8rpx;position:relative}.quick-item{position:relative;text-align:center;font-size:20rpx;color:var(--muted)}.quick-item:not(:last-child)::after{content:'';position:absolute;right:0;top:10rpx;bottom:10rpx;width:1rpx;background:var(--line)}.quick-item text{display:block}.quick-number{margin-bottom:8rpx;color:var(--coffee-900);font-size:31rpx;font-weight:800}.active-order{display:flex;align-items:center;gap:16rpx;padding:23rpx}.active-symbol{width:64rpx;height:64rpx;display:flex;align-items:center;justify-content:center;border-radius:18rpx;background:#e4eee4;color:var(--green);font-size:19rpx;font-weight:700}.active-main{flex:1}.active-main text{display:block}.active-main text:first-child{font-size:25rpx;font-weight:700}.active-main text:last-child{margin-top:6rpx;color:var(--muted);font-size:20rpx}.arrow{color:var(--coffee-600);font-size:38rpx}.services{display:grid;grid-template-columns:1fr 1fr;padding:8rpx 24rpx}.service-item{display:flex;flex-direction:column;align-items:flex-start;gap:7rpx;padding:24rpx 10rpx;border-bottom:1rpx solid var(--line);color:var(--ink)}.service-item:nth-last-child(-n+2){border-bottom:0}.service-item text:first-child{font-size:24rpx;font-weight:700}.service-item text:last-child{color:var(--muted);font-size:18rpx}.favorite-list{display:flex;flex-direction:column;gap:14rpx}.empty-favorite{padding:40rpx;text-align:center;color:var(--muted);font-size:22rpx}.footer-mark{padding:62rpx 20rpx 20rpx;text-align:center;color:#b3a89f;font-size:18rpx}
</style>
