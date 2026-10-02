<template><view class="empty-state"><view class="empty-line" /><view class="empty-title">{{ title }}</view><view class="empty-desc">{{ description }}</view><button v-if="action || actionText" class="empty-action" @click="$emit('action')">{{ action || actionText }}</button></view></template>
<script setup>
defineProps({ title: { type: String, default: '暂无内容' }, description: { type: String, default: '' }, action: { type: String, default: '' }, actionText: { type: String, default: '' } })
defineEmits(['action'])
</script>
<style scoped>
.empty-state { padding: 100rpx 40rpx; text-align: center; }.empty-line{width:72rpx;height:5rpx;margin:0 auto 28rpx;border-radius:3rpx;background:var(--caramel-500)}.empty-title { font-size: 32rpx; font-weight: 700; }.empty-desc { margin-top: 10rpx; color: var(--muted); font-size: 24rpx; }.empty-action { display: inline-flex; margin-top: 30rpx; padding: 18rpx 32rpx; border-radius: 32rpx; color: white; background: var(--brand-700); font-size: 24rpx; }
</style>
