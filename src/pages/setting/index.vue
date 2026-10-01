<script setup>
import { CAMPUS } from '@/data/catalog'
import { useAppStore } from '@/store/app'

const store = useAppStore()
function reset() {
  uni.showModal({ title: '重置演示数据', content: '购物袋、订单和偏好将恢复初始状态。', confirmColor: '#654536', success: ({ confirm }) => {
    if (!confirm) return
    store.resetDemo()
    uni.showToast({ title: '已恢复初始状态', icon: 'success' })
  } })
}
function toast(text) { uni.showToast({ title: text, icon: 'none' }) }
</script>

<template>
  <view class="page-shell setting-page">
    <view class="setting-header"><button class="top-back" @click="uni.navigateBack()">‹</button><text>PROJECT SETTINGS</text><text>设置</text><text>管理本地演示与项目信息</text></view>
    <view class="section">
      <view class="section-heading"><text class="section-title">演示环境</text></view>
      <view class="settings card">
        <view class="setting-row"><view><text class="row-title">默认位置</text><text class="row-copy">{{ CAMPUS.name }} · {{ CAMPUS.campus }}</text></view><text class="tag">已启用</text></view>
        <view class="setting-row"><view><text class="row-title">数据模式</text><text class="row-copy">浏览器与小程序本地存储</text></view><text class="tag">LOCAL</text></view>
        <view class="setting-row"><view><text class="row-title">网络依赖</text><text class="row-copy">核心流程无需接口、登录或地图密钥</text></view><text class="safe">✓</text></view>
      </view>
    </view>
    <view class="section">
      <view class="section-heading"><text class="section-title">偏好设置</text></view>
      <view class="settings card">
        <button class="setting-row" @click="toast('消息提醒为静态演示')"><view><text class="row-title">订单消息提醒</text><text class="row-copy">制作与取餐状态通知</text></view><text class="arrow">›</text></button>
        <button class="setting-row" @click="toast('隐私说明为静态演示')"><view><text class="row-title">隐私与权限</text><text class="row-copy">当前版本不采集真实位置与账号数据</text></view><text class="arrow">›</text></button>
        <button class="setting-row" @click="toast('当前已是最新演示版本')"><view><text class="row-title">关于本项目</text><text class="row-copy">交互原型 v2.1.0</text></view><text class="arrow">›</text></button>
      </view>
    </view>
    <view class="section"><button class="reset-button" @click="reset">重置全部演示数据</button><text class="reset-tip">遇到展示数据混乱时，可随时恢复初始状态</text></view>
  </view>
</template>

<style scoped lang="scss">
.setting-page{padding-bottom:60rpx}.setting-header{position:relative;padding:calc(92rpx + env(safe-area-inset-top)) 30rpx 56rpx;background:linear-gradient(145deg,#35231b,#684736);color:#fff}.top-back{position:absolute;left:26rpx;top:calc(22rpx + env(safe-area-inset-top));width:66rpx;height:66rpx;display:flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(255,255,255,.12);color:white;font-size:48rpx;padding-bottom:8rpx}.setting-header text{display:block}.setting-header>text:first-of-type{font-size:18rpx;letter-spacing:5rpx;color:var(--caramel-300)}.setting-header>text:nth-of-type(2){margin-top:14rpx;font-size:47rpx;font-weight:800}.setting-header>text:last-child{margin-top:9rpx;font-size:23rpx;color:rgba(255,255,255,.6)}.settings{padding:0 24rpx}.setting-row{display:flex;align-items:center;justify-content:space-between;width:100%;min-height:106rpx;border:0;border-bottom:1rpx solid var(--line);background:transparent;text-align:left;color:var(--ink)}.setting-row:last-child{border-bottom:0}.row-title,.row-copy{display:block}.row-title{font-size:26rpx;font-weight:700}.row-copy{margin-top:7rpx;color:var(--muted);font-size:20rpx}.tag{padding:7rpx 12rpx;border-radius:10rpx;background:var(--oat-100);color:var(--coffee-700);font-size:18rpx}.safe{color:var(--green);font-size:31rpx}.arrow{font-size:36rpx;color:var(--muted)}.reset-button{width:100%;height:90rpx;border:1rpx solid #d6aaa3;border-radius:45rpx;color:var(--danger);font-size:26rpx;font-weight:700}.reset-tip{display:block;margin-top:15rpx;text-align:center;color:var(--muted);font-size:19rpx}
</style>
