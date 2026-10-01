<template>
  <view class="product-card" @click="$emit('open', product)">
    <view class="product-image-wrap">
      <image v-if="!imageFailed" class="product-image" :src="product.image" mode="aspectFill" @error="imageFailed = true" />
      <view v-else class="product-fallback">{{ product.fallback }}</view>
      <text v-if="product.badge" class="badge">{{ product.badge }}</text>
    </view>
    <view class="product-info">
      <view class="product-name">{{ product.name }}</view>
      <view class="product-desc">{{ product.subtitle }}</view>
      <view class="product-sales">月售 {{ product.sales }}</view>
      <view class="product-bottom">
        <view><text class="price">{{ formatMoney(product.priceCents) }}</text><text v-if="product.originalPriceCents" class="original">{{ formatMoney(product.originalPriceCents) }}</text></view>
        <button class="add-button" aria-label="加入购物袋" @click.stop="$emit('add', product)"><text>＋</text></button>
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
.product-card { display: flex; gap: 20rpx; padding: 22rpx 0; border-bottom: 1rpx solid var(--line); }
.product-image-wrap { position: relative; flex: 0 0 174rpx; height: 174rpx; border-radius: 22rpx; overflow: hidden; background: var(--oat-100); }
.product-image { width: 100%; height: 100%; }
.product-fallback { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; color:var(--coffee-700);font-size: 24rpx;font-weight:700;letter-spacing:2rpx; background: linear-gradient(145deg, #f5eadb, #e8d3ba); }
.badge { position: absolute; left: 10rpx; top: 10rpx; padding: 7rpx 12rpx; border-radius: 14rpx; color: white; background: rgba(53,35,27,.82); font-size: 18rpx; }
.product-info { min-width: 0; flex: 1; display: flex; flex-direction: column; }
.product-name { font-size: 30rpx; font-weight: 700; }
.product-desc { margin-top: 8rpx; color: var(--muted); font-size: 22rpx; line-height: 1.45; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden; }
.product-sales { margin-top: 8rpx; color: #b0a69d; font-size: 19rpx; }
.product-bottom { display: flex; align-items: flex-end; justify-content: space-between; margin-top: auto; }
.price { font-size: 30rpx; }
.original { margin-left: 10rpx; color: #aaa19a; text-decoration: line-through; font-size: 20rpx; }
.add-button { flex:0 0 54rpx;width:54rpx;height:54rpx;padding:0;display:flex;align-items:center;justify-content:center;border-radius:50%;color:white;background:var(--brand);box-shadow:0 7rpx 16rpx rgba(26,75,58,.2);font-size:34rpx;line-height:1; }
.add-button text{display:block;line-height:1;transform:translateY(-1rpx)}
</style>
