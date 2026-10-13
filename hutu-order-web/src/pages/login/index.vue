<script setup>
import { ref } from 'vue'
import { useAppStore } from '@/store/app'

const store = useAppStore()
const mode = ref('login')
const username = ref('')
const password = ref('')
const submitting = ref(false)

async function submit() {
  if (submitting.value) return
  const name = username.value.trim()
  const pwd = password.value
  if (!name || !pwd) { uni.showToast({ title: '请输入账号和密码', icon: 'none' }); return }
  if (pwd.length < 6) { uni.showToast({ title: '密码至少 6 位', icon: 'none' }); return }
  submitting.value = true
  uni.showLoading({ title: mode.value === 'login' ? '登录中' : '注册中' })
  try {
    if (mode.value === 'login') await store.login(name, pwd)
    else await store.register(name, pwd)
    uni.hideLoading()
    uni.showToast({ title: mode.value === 'login' ? '登录成功' : '注册成功', icon: 'success' })
    setTimeout(() => {
      if (store.state.user && store.state.user.role === 'merchant') {
        uni.redirectTo({ url: '/pages/merchant/index' })
      } else {
        const pages = getCurrentPages()
        if (pages.length > 1) uni.navigateBack()
        else uni.switchTab({ url: '/pages/my/index' })
      }
    }, 400)
  } catch (e) {
    uni.hideLoading()
  } finally {
    submitting.value = false
  }
}

function switchMode(next) {
  if (next === mode.value) return
  mode.value = next
  password.value = ''
}
</script>

<template>
  <view class="page-shell login-page">
    <view class="login-header">
      <button class="top-back" @click="uni.navigateBack()">‹</button>
      <text class="eyebrow">MEMBER ACCESS</text>
      <text class="title">{{ mode === 'login' ? '登录' : '注册' }}</text>
      <text class="subtitle">{{ mode === 'login' ? '登录后同步订单、收藏与购物车' : '创建账户，开启校园点餐' }}</text>
    </view>

    <view class="form-card card">
      <view class="mode-tabs">
        <button :class="{ active: mode === 'login' }" @click="switchMode('login')">登录</button>
        <button :class="{ active: mode === 'register' }" @click="switchMode('register')">注册</button>
      </view>
      <view class="field">
        <text>账号</text>
        <input v-model="username" placeholder="请输入用户名" maxlength="30" />
      </view>
      <view class="field">
        <text>密码</text>
        <input v-model="password" password placeholder="请输入密码（至少 6 位）" maxlength="30" @confirm="submit" />
      </view>
      <button class="submit-button" :class="{ disabled: submitting }" @click="submit">{{ mode === 'login' ? '登录' : '注册并登录' }}</button>
    </view>

    <view class="tips">
      <text class="tip-title">演示账号</text>
      <text class="tip-line">用户端：test / 123456</text>
      <text class="tip-line">商家端：merchant / 123456</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
.login-page { padding-bottom: 60rpx; }
.login-header { position: relative; padding: calc(92rpx + env(safe-area-inset-top)) 30rpx 70rpx; background: linear-gradient(145deg, #0637c9, #071a62); color: #fff; }
.top-back { position: absolute; left: 26rpx; top: calc(22rpx + env(safe-area-inset-top)); width: 66rpx; height: 66rpx; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: rgba(255,255,255,.12); color: #fff; font-size: 48rpx; padding-bottom: 8rpx; }
.eyebrow, .title, .subtitle { display: block; }
.eyebrow { font-size: 18rpx; letter-spacing: 5rpx; color: #edcf91; }
.title { margin-top: 14rpx; font-size: 47rpx; font-weight: 800; }
.subtitle { margin-top: 9rpx; font-size: 22rpx; color: rgba(255,255,255,.65); }
.form-card { margin: -40rpx 28rpx 0; position: relative; padding: 30rpx 28rpx; }
.mode-tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 12rpx; padding: 8rpx; border-radius: 20rpx; background: var(--oat-50); }
.mode-tabs button { height: 74rpx; border-radius: 16rpx; color: var(--muted); font-size: 26rpx; }
.mode-tabs button.active { background: var(--brand-800); color: #fff; font-weight: 700; }
.field { display: flex; align-items: center; gap: 16rpx; min-height: 100rpx; border-bottom: 1rpx solid var(--line); }
.field > text { width: 96rpx; font-weight: 650; font-size: 25rpx; }
.field input { flex: 1; font-size: 25rpx; }
.submit-button { width: 100%; height: 88rpx; margin-top: 30rpx; border-radius: 20rpx; background: var(--brand); color: #fff; font-size: 28rpx; font-weight: 750; }
.submit-button.disabled { opacity: .5; }
.tips { margin: 34rpx 28rpx 0; padding: 26rpx; border: 1rpx dashed #d8cec2; border-radius: 18rpx; }
.tips text { display: block; }
.tip-title { font-size: 23rpx; font-weight: 700; color: var(--ink); }
.tip-line { margin-top: 10rpx; font-size: 21rpx; color: var(--muted); }
</style>
