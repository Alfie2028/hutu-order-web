<template>
  <view class="page-shell order-page">
    <view class="order-header">
      <view class="header-top"><view><view class="header-kicker">{{ state.orderMode === 'pickup' ? '到店自取' : '到店堂食' }}</view><view class="header-store" @click="goStores">{{ currentStore.shortName }} <text>›</text></view></view><view class="mode-switch"><text :class="{ active: state.orderMode === 'pickup' }" @click="setOrderMode('pickup')">自取</text><text :class="{ active: state.orderMode === 'dineIn' }" @click="setOrderMode('dineIn')">堂食</text></view></view>
      <view class="search-box"><text>⌕</text><input v-model="keyword" placeholder="搜索咖啡、茶饮或烘焙"/><text v-if="keyword" @click="keyword = ''">×</text></view>
      <scroll-view scroll-x class="category-scroll" :show-scrollbar="false"><view class="category-row"><text v-for="category in CATEGORIES" :key="category.id" :class="['category-item', { active: activeCategory === category.id }]" @click="activeCategory = category.id">{{ category.name }}</text></view></scroll-view>
    </view>

    <view class="menu-content">
      <view v-if="!keyword" class="category-banner"><view><view class="banner-kicker">{{ activeCategoryInfo.name }}</view><view class="banner-copy">每一杯都认真制作，预计 {{ currentStore.waitMinutes }} 分钟取餐</view></view><text class="banner-meta">FRESHLY MADE</text></view>
      <view class="menu-title"><text>{{ keyword ? `“${keyword}”的搜索结果` : activeCategoryInfo.name }}</text><text>{{ filteredProducts.length }} 件</text></view>
      <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" @open="openProduct" @add="quickAdd" />
      <EmptyState v-if="!filteredProducts.length" title="没有找到相关商品" description="换个关键词试试吧" action="清空搜索" @action="keyword = ''" />
    </view>

    <view v-if="cartCount" class="cart-bar">
      <view class="cart-round" @click="showCart = true"><text class="cart-label">购物袋</text><text class="cart-count">{{ cartCount }}</text></view>
      <view class="cart-price" @click="showCart = true"><view>{{ formatMoney(cartSubtotal) }}</view><text>已选 {{ cartCount }} 件</text></view>
      <button class="checkout" @click="checkout">去结算</button>
    </view>

    <view v-if="showCart" class="drawer-mask" @click="showCart = false"></view>
    <view class="cart-drawer" :class="{ show: showCart }">
      <view class="drawer-handle"></view><view class="drawer-header"><view><text class="drawer-title">购物袋</text><text class="drawer-sub">{{ currentStore.shortName }}</text></view><text class="clear-cart" @click="clearCart">清空</text></view>
      <scroll-view scroll-y class="drawer-list">
        <view v-for="item in state.cart" :key="item.key" class="cart-item">
          <image class="cart-visual" :src="item.image" mode="aspectFill" /><view class="cart-info"><view class="cart-name">{{ item.name }}</view><view class="cart-options">{{ optionText(item) || '默认规格' }}</view><view class="price">{{ formatMoney(item.unitPriceCents) }}</view></view>
          <view class="stepper"><button @click="updateCartQuantity(item.key, item.quantity - 1)">−</button><text>{{ item.quantity }}</text><button @click="updateCartQuantity(item.key, item.quantity + 1)">＋</button></view>
        </view>
      </scroll-view>
      <view class="drawer-footer"><view><text class="muted">合计 </text><text class="drawer-total">{{ formatMoney(cartSubtotal) }}</text></view><button class="primary-button" @click="checkout">确认结算</button></view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import ProductCard from '@/component/ProductCard.vue'
import EmptyState from '@/component/EmptyState.vue'
import { CATEGORIES, PRODUCTS } from '@/data/catalog'
import { useAppStore } from '@/store/app'
import { formatMoney } from '@/utils/format'

const keyword = ref('')
const activeCategory = ref(CATEGORIES[0].id)
const showCart = ref(false)
const { state, currentStore, cartCount, cartSubtotal, setOrderMode, addToCart, updateCartQuantity, clearCart } = useAppStore()
const activeCategoryInfo = computed(() => CATEGORIES.find((item) => item.id === activeCategory.value) || CATEGORIES[0])
const filteredProducts = computed(() => { const key = keyword.value.trim().toLowerCase(); return key ? PRODUCTS.filter((product) => `${product.name}${product.subtitle}${product.badge}`.toLowerCase().includes(key)) : PRODUCTS.filter((product) => product.categoryId === activeCategory.value) })
const quickAdd = (product) => { if (product.options.length) openProduct(product); else { addToCart(product.id); uni.showToast({ title: '已加入购物车', icon: 'success' }) } }
const openProduct = (product) => uni.navigateTo({ url: `/pages/item-detail/index?id=${product.id}` })
const optionText = (item) => item.selectedOptions.map((option) => option.name).join(' / ')
const checkout = () => { if (!state.cart.length) return; showCart.value = false; uni.navigateTo({ url: '/pages/confirm-order/index' }) }
const goStores = () => uni.switchTab({ url: '/pages/shop/index' })
</script>

<style scoped lang="scss">
.order-page { padding-bottom:170rpx; }.order-header { position:sticky; z-index:8; top:0; padding:calc(70rpx + env(safe-area-inset-top)) 26rpx 0; background:rgba(251,248,243,.97); backdrop-filter:blur(16rpx); }.header-top { display:flex; align-items:center; justify-content:space-between; }.header-kicker { color:var(--green); font-size:20rpx; font-weight:700; }.header-store { margin-top:6rpx; font-size:31rpx; font-weight:750; }.header-store text { color:var(--muted); }.mode-switch { display:flex; padding:5rpx; border-radius:30rpx; background:var(--oat-100); }.mode-switch text { padding:13rpx 22rpx; border-radius:25rpx; color:var(--muted); font-size:22rpx; }.mode-switch .active { color:#fff; background:var(--coffee-700); }.search-box { display:flex; align-items:center; gap:14rpx; height:76rpx; margin-top:24rpx; padding:0 22rpx; border-radius:38rpx; background:#fff; box-shadow:0 7rpx 24rpx rgba(53,35,27,.06); }.search-box input { flex:1; font-size:24rpx; }.category-scroll { margin-top:25rpx; white-space:nowrap; }.category-row { display:flex; gap:34rpx; padding-right:30rpx; }.category-item { position:relative; padding-bottom:19rpx; color:var(--muted); font-size:25rpx; }.category-item.active { color:var(--coffee-900); font-weight:750; }.category-item.active::after { content:''; position:absolute; left:50%; bottom:7rpx; width:32rpx; height:5rpx; border-radius:3rpx; background:var(--caramel-500); transform:translateX(-50%); }
.menu-content { padding:24rpx 28rpx; }.category-banner { display:flex; align-items:center; justify-content:space-between; min-height:150rpx; padding:26rpx 30rpx; border-radius:24rpx; color:#fff; background:linear-gradient(120deg,#2d654f,#173e30);box-shadow:0 12rpx 28rpx rgba(22,64,48,.14) }.banner-kicker { font-size:31rpx; font-weight:750; }.banner-copy { margin-top:8rpx; color:rgba(255,255,255,.7); font-size:21rpx; }.banner-meta{color:rgba(255,255,255,.5);font-size:17rpx;letter-spacing:3rpx}.menu-title { display:flex; justify-content:space-between; margin-top:30rpx; padding-bottom:5rpx; font-size:30rpx; font-weight:750; }.menu-title text:last-child { color:var(--muted); font-size:20rpx; font-weight:400; }
.cart-bar { position:fixed; z-index:20; left:24rpx; right:24rpx; bottom:calc(110rpx + env(safe-area-inset-bottom)); display:flex; align-items:center; height:102rpx; padding:10rpx 10rpx 10rpx 22rpx; border-radius:54rpx; color:#fff; background:var(--coffee-950); box-shadow:0 18rpx 40rpx rgba(39,26,20,.28); }.cart-round { position:relative;min-width:82rpx }.cart-label{font-size:20rpx;font-weight:700}.cart-count { position:absolute; right:-2rpx; top:-20rpx; display:flex; align-items:center; justify-content:center; min-width:30rpx; height:30rpx; padding:0 7rpx; border-radius:15rpx; background:var(--danger); font-size:17rpx; }.cart-price { flex:1; margin-left:16rpx; font-size:30rpx; font-weight:750; }.cart-price text { display:block; margin-top:2rpx; color:rgba(255,255,255,.6); font-size:18rpx; font-weight:400; }.checkout { height:80rpx; padding:0 34rpx; border-radius:40rpx; color:var(--coffee-900); background:var(--caramel-300); font-size:27rpx; font-weight:750; }
.drawer-mask { position:fixed; z-index:30; inset:0; background:rgba(39,26,20,.45); }.cart-drawer { position:fixed; z-index:31; left:0; right:0; bottom:0; max-height:74vh; padding:14rpx 28rpx calc(28rpx + env(safe-area-inset-bottom)); border-radius:34rpx 34rpx 0 0; background:#fff; transform:translateY(110%); transition:transform .25s ease; }.cart-drawer.show { transform:translateY(0); }.drawer-handle { width:80rpx; height:8rpx; margin:0 auto 18rpx; border-radius:4rpx; background:#ddd4cc; }.drawer-header { display:flex; justify-content:space-between; align-items:center; padding:10rpx 0 20rpx; }.drawer-title { font-size:34rpx; font-weight:750; }.drawer-sub { margin-left:14rpx; color:var(--muted); font-size:20rpx; }.clear-cart { color:var(--muted); font-size:22rpx; }.drawer-list { max-height:46vh; }.cart-item { display:flex; align-items:center; gap:18rpx; padding:20rpx 0; border-bottom:1rpx solid var(--line); }.cart-visual { width:100rpx;height:100rpx;flex:0 0 100rpx;border-radius:20rpx;background:var(--oat-100) }.cart-info { min-width:0; flex:1; }.cart-name { font-size:26rpx; font-weight:700; }.cart-options { margin:7rpx 0; overflow:hidden; color:var(--muted); font-size:19rpx; text-overflow:ellipsis; white-space:nowrap; }.stepper { display:flex; align-items:center; gap:16rpx; }.stepper button { width:46rpx;height:46rpx;padding:0;display:flex;align-items:center;justify-content:center;border:1rpx solid var(--line);border-radius:50%;line-height:1;font-size:25rpx }.stepper text { min-width:24rpx; text-align:center; }.drawer-footer { display:flex; align-items:center; justify-content:space-between; padding-top:24rpx; }.drawer-total { font-size:36rpx; font-weight:750; }.drawer-footer .primary-button { min-height:76rpx; font-size:25rpx; }
@media screen and (min-width:760px) { .cart-bar { left:50%; right:auto; width:700px; transform:translateX(-50%); }.cart-drawer { left:50%; right:auto; width:750px; transform:translate(-50%,110%); }.cart-drawer.show { transform:translate(-50%,0); } }
</style>
