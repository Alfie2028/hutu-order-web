<script setup>
import { computed, reactive, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { PRODUCTS } from '@/data/catalog'
import { useAppStore } from '@/store/app'
import { formatMoney } from '@/utils/format'

const store = useAppStore()
const product = ref(PRODUCTS[0])
const selected = reactive({})
const quantity = ref(1)
const imageFailed = ref(false)

onLoad((query) => {
  product.value = PRODUCTS.find((item) => item.id === query.id) || PRODUCTS[0]
  product.value.options.forEach((group) => {
    selected[group.id] = group.multiple ? [] : group.options[0]?.id
  })
})

const favorite = computed(() => store.state.favoriteIds.includes(product.value.id))
const selectedOptions = computed(() => product.value.options.flatMap((group) => {
  const ids = Array.isArray(selected[group.id]) ? selected[group.id] : [selected[group.id]]
  return group.options.filter((option) => ids.includes(option.id)).map((option) => ({ ...option, groupName: group.name }))
}))
const unitPrice = computed(() => product.value.priceCents + selectedOptions.value.reduce((sum, option) => sum + option.extraCents, 0))
const totalPrice = computed(() => unitPrice.value * quantity.value)

function choose(group, optionId) {
  if (!group.multiple) {
    selected[group.id] = optionId
    return
  }
  const values = selected[group.id]
  selected[group.id] = values.includes(optionId) ? values.filter((id) => id !== optionId) : [...values, optionId]
}

function isSelected(groupId, optionId) {
  const value = selected[groupId]
  return Array.isArray(value) ? value.includes(optionId) : value === optionId
}

function add(goCheckout = false) {
  store.addToCart(product.value.id, selectedOptions.value, quantity.value)
  uni.showToast({ title: '已加入购物袋', icon: 'success' })
  if (goCheckout) setTimeout(() => uni.navigateTo({ url: '/pages/confirm-order/index' }), 250)
}
</script>

<template>
  <view class="page-shell detail-page">
    <view class="visual">
      <image v-if="!imageFailed" class="visual-image" :src="product.image" mode="aspectFill" @error="imageFailed = true" />
      <text v-else class="visual-fallback">{{ product.fallback }}</text>
      <button class="back-button" @click="uni.navigateBack()">‹</button>
      <button class="favorite-button" :class="{ active: favorite }" @click="store.toggleFavorite(product.id)">{{ favorite ? '♥' : '♡' }}</button>
      <view class="visual-glow" />
    </view>

    <view class="content">
      <view class="headline">
        <view>
          <text class="badge">{{ product.badge }}</text>
          <text class="title">{{ product.name }}</text>
          <text class="subtitle">{{ product.subtitle }}</text>
        </view>
        <view class="price-block">
          <text class="price">{{ formatMoney(unitPrice) }}</text>
          <text class="sales">已售 {{ product.sales }}</text>
        </view>
      </view>

      <view v-if="product.options.length" class="option-card card">
        <view v-for="group in product.options" :key="group.id" class="option-group">
          <view class="option-heading">
            <text class="option-title">{{ group.name }}</text>
            <text class="option-tip">{{ group.multiple ? '可多选' : '单选' }}</text>
          </view>
          <view class="option-grid">
            <button v-for="option in group.options" :key="option.id" class="option" :class="{ selected: isSelected(group.id, option.id) }" @click="choose(group, option.id)">
              <text>{{ option.name }}</text>
              <text v-if="option.extraCents" class="option-extra">+{{ formatMoney(option.extraCents) }}</text>
            </button>
          </view>
        </view>
      </view>

      <view class="notice card"><view><text class="notice-title">门店现制</text><text class="notice-copy">饮品下单后开始制作，建议在预计时间内到店取餐。</text></view></view>
    </view>

    <view class="action-bar">
      <view class="stepper">
        <button @click="quantity = Math.max(1, quantity - 1)">−</button><text>{{ quantity }}</text><button @click="quantity += 1">＋</button>
      </view>
      <button class="secondary-action" @click="add(false)">加入购物袋</button>
      <button class="primary-action" @click="add(true)">去结算 · {{ formatMoney(totalPrice) }}</button>
    </view>
  </view>
</template>

<style scoped lang="scss">
.detail-page { padding-bottom: 170rpx; }
.visual { height: 600rpx; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; background: radial-gradient(circle at 50% 42%, #f9ead6 0, #e8c79d 42%, #aa7656 100%); }
.visual-image { width: 100%; height: 100%; }
.visual-fallback { position: relative; z-index: 2; font-size: 230rpx; filter: drop-shadow(0 28rpx 24rpx rgba(53, 35, 27, .25)); }
.visual-glow { position: absolute; width: 380rpx; height: 90rpx; bottom: 72rpx; border-radius: 50%; background: rgba(53, 35, 27, .17); filter: blur(22rpx); }
.back-button,.favorite-button { position: absolute; top: calc(24rpx + env(safe-area-inset-top)); z-index: 4; width: 72rpx; height: 72rpx; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,.9); color: var(--coffee-900); box-shadow: 0 8rpx 24rpx rgba(53,35,27,.12); }
.back-button { left: 26rpx; font-size: 54rpx; padding-bottom: 8rpx; }
.favorite-button { right: 26rpx; font-size: 42rpx; }.favorite-button.active{color:var(--danger)}
.content { position: relative; z-index: 3; margin-top: -44rpx; padding: 36rpx 28rpx 0; border-radius: 40rpx 40rpx 0 0; background: var(--oat-50); }
.headline { display:flex; justify-content:space-between; gap:24rpx; }.headline>view:first-child{flex:1;min-width:0}
.badge { display:inline-block; margin-bottom:14rpx; padding:7rpx 14rpx; border-radius:10rpx; background:#ead7bd; color:var(--coffee-700); font-size:20rpx; font-weight:700; }
.title,.subtitle,.sales,.notice-title,.notice-copy { display:block; }.title{font-size:44rpx;font-weight:800;color:var(--coffee-950)}.subtitle{margin-top:12rpx;color:var(--muted);font-size:25rpx;line-height:1.6}
.price-block{text-align:right;padding-top:34rpx}.price{font-size:34rpx}.sales{margin-top:8rpx;font-size:20rpx;color:var(--muted)}
.option-card{margin-top:32rpx;padding:8rpx 26rpx}.option-group{padding:26rpx 0;border-bottom:1rpx solid var(--line)}.option-group:last-child{border-bottom:0}.option-heading{display:flex;align-items:center;justify-content:space-between;margin-bottom:18rpx}.option-title{font-weight:750;font-size:29rpx}.option-tip{font-size:21rpx;color:var(--muted)}
.option-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14rpx}.option{min-height:74rpx;padding:0 16rpx;border:1rpx solid var(--line);border-radius:16rpx;color:var(--ink);background:#fff;font-size:25rpx}.option.selected{border-color:var(--coffee-700);background:var(--oat-100);color:var(--coffee-800);font-weight:700}.option-extra{margin-left:6rpx;font-size:19rpx;color:var(--muted)}
.notice{display:flex;gap:18rpx;margin-top:22rpx;padding:24rpx;border-left:5rpx solid var(--caramel-500)}.notice-title{font-size:25rpx;font-weight:700}.notice-copy{margin-top:6rpx;font-size:22rpx;color:var(--muted);line-height:1.5}
.action-bar{position:fixed;left:0;right:0;bottom:0;z-index:20;display:flex;align-items:center;gap:12rpx;padding:18rpx 24rpx calc(18rpx + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);box-shadow:0 -10rpx 30rpx rgba(53,35,27,.08)}
.stepper{display:flex;align-items:center;gap:8rpx}.stepper button{width:52rpx;height:52rpx;padding:0;display:flex;align-items:center;justify-content:center;border:1rpx solid var(--line);border-radius:50%;font-size:27rpx;line-height:1}.stepper text{min-width:28rpx;text-align:center;font-weight:700}.secondary-action,.primary-action{height:78rpx;padding:0 22rpx;border-radius:39rpx;font-size:24rpx;font-weight:750}.secondary-action{border:1rpx solid var(--coffee-700);color:var(--coffee-700)}.primary-action{flex:1;background:var(--coffee-900);color:white;white-space:nowrap}
@media screen and (min-width:760px){.action-bar{max-width:750px;margin:0 auto}}
</style>
