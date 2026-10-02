<template>
  <view class="product-card" @click="$emit('open', product)">
    <view class="product-image-wrap">
      <image v-if="!imageFailed" class="product-image" :src="product.image" mode="aspectFit" @error="imageFailed = true" />
      <view v-else class="product-fallback">{{ product.fallback }}</view>
      <text v-if="product.badge" class="badge">{{ product.badge }}</text>
    </view>
    <view class="product-info">
      <view class="product-name">{{ product.name }}</view>
      <view class="product-desc">{{ product.subtitle }}</view>
      <view class="product-sales">{{ product.stallName }}</view>
      <view class="product-bottom">
        <view><text class="price">{{ formatMoney(product.priceCents) }}</text><text v-if="product.originalPriceCents" class="original">{{ formatMoney(product.originalPriceCents) }}</text></view>
        <button class="add-button" aria-label="加入购物车" @click.stop="$emit('add', product)"><text>＋</text></button>
      </view>
    </view>
  </view>
</template>
<script setup>
import { ref } from 'vue'
import { formatMoney } from '@/utils/format'
defineProps({ product: { type: Object, required: true } })
defineEmits(['open', 'add'])
const imageFailed = ref(false)
</script>
<style scoped lang="scss">
.product-card { display:flex;gap:14rpx;margin-bottom:12rpx;padding:18rpx 16rpx;border:1rpx solid rgba(7,40,132,.05);border-radius:22rpx;background:#fff;box-shadow:0 8rpx 22rpx rgba(17,38,91,.045) }
.product-image-wrap { position:relative;flex:0 0 150rpx;height:166rpx;border-radius:50%;overflow:visible;background:linear-gradient(145deg,#f7f8fb,#eef1f7) }
.product-image { width:100%;height:100%;transform:scale(1.08) }
.product-fallback { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; color:var(--brand-700);font-size: 24rpx;font-weight:700;letter-spacing:2rpx; background: linear-gradient(145deg, #f5eadb, #e8d3ba); }
.badge { position:absolute;left:-3rpx;top:4rpx;padding:5rpx 10rpx;border-radius:5rpx;color:#fff;background:var(--brand);font-size:16rpx;font-weight:700 }
.product-info { min-width: 0; flex: 1; display: flex; flex-direction: column; }
.product-name { font-size:27rpx;font-weight:760 }
.product-desc { margin-top:7rpx;color:var(--muted);font-size:19rpx;line-height:1.38;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden }
.product-sales { margin-top:7rpx;color:#a5a8b0;font-size:17rpx }
.product-bottom { display: flex; align-items: flex-end; justify-content: space-between; margin-top: auto; }
.price { font-size:28rpx }
.original { margin-left: 10rpx; color: #aaa19a; text-decoration: line-through; font-size: 20rpx; }
.add-button { flex:0 0 52rpx;width:52rpx;height:52rpx;padding:0;display:flex;align-items:center;justify-content:center;border-radius:17rpx;color:white;background:var(--brand);box-shadow:0 7rpx 16rpx rgba(6,55,201,.24);font-size:33rpx;line-height:1; }
.add-button text{display:block;line-height:1;transform:translateY(-1rpx)}
</style>
