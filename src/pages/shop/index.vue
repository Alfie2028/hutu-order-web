<script setup>
import { computed, ref } from 'vue'
import { CAMPUS, STORES } from '@/data/catalog'
import { useAppStore } from '@/store/app'
import { formatDistance } from '@/utils/format'

const keyword = ref('')
const latitude = ref(CAMPUS.latitude)
const longitude = ref(CAMPUS.longitude)
const mapTarget = ref(CAMPUS)
const { state, currentStore, setStore } = useAppStore()

const osmMapUrl = computed(() => {
  const lat = Number(mapTarget.value.osmLatitude ?? mapTarget.value.latitude)
  const lng = Number(mapTarget.value.osmLongitude ?? mapTarget.value.longitude)
  const south = (lat - 0.008).toFixed(6)
  const west = (lng - 0.013).toFixed(6)
  const north = (lat + 0.008).toFixed(6)
  const east = (lng + 0.013).toFixed(6)
  const bbox = `${west},${south},${east},${north}`
  return `https://www.openstreetmap.org/export/embed.html?bbox=${encodeURIComponent(bbox)}&layer=mapnik&marker=${lat}%2C${lng}`
})

const filteredStores = computed(() => {
  const key = keyword.value.trim()
  return key ? STORES.filter((store) => `${store.name}${store.address}`.includes(key)) : STORES
})

const markers = computed(() => [
  {
    id: 0,
    latitude: CAMPUS.latitude,
    longitude: CAMPUS.longitude,
    title: CAMPUS.name,
    iconPath: '/static/icon/my-location.png',
    width: 32,
    height: 32,
    callout: { content: `${CAMPUS.name}\n${CAMPUS.campus}`, display: 'ALWAYS', padding: 8, borderRadius: 6, color: '#35231b', bgColor: '#ffffff' },
  },
  ...STORES.map((store, index) => ({
    id: index + 1,
    latitude: store.latitude,
    longitude: store.longitude,
    title: store.name,
    iconPath: store.id === state.currentStoreId ? '/static/icon/shop-location-selected.png' : '/static/icon/shop-location.png',
    width: store.id === state.currentStoreId ? 32 : 27,
    height: store.id === state.currentStoreId ? 32 : 27,
    callout: { content: store.name, display: store.id === state.currentStoreId ? 'ALWAYS' : 'BYCLICK', padding: 7, borderRadius: 5, color: '#35231b', bgColor: '#ffffff' },
  })),
])

function select(store) {
  const apply = () => {
    setStore(store.id)
    latitude.value = store.latitude
    longitude.value = store.longitude
    mapTarget.value = store
  }
  if (state.cart.length && state.currentStoreId !== store.id) {
    uni.showModal({ title: '切换餐厅', content: '切换餐厅将清空当前购物车，是否继续？', success: ({ confirm }) => confirm && apply() })
  } else apply()
}

function handleMarkerTap(event) {
  const markerId = Number(event.detail?.markerId ?? event.markerId)
  if (markerId === 0) return recenterCampus()
  const store = STORES[markerId - 1]
  if (store) select(store)
}

function recenterCampus() {
  latitude.value = CAMPUS.latitude
  longitude.value = CAMPUS.longitude
  mapTarget.value = CAMPUS
}

function goOrder() { uni.switchTab({ url: '/pages/order/index' }) }
</script>

<template>
  <view class="page-shell shop-page">
    <view class="map-wrap">
      <!-- #ifdef H5 -->
      <iframe
        class="map-box osm-frame"
        :src="osmMapUrl"
        title="河南农业大学软件学院周边地图"
        loading="eager"
        referrerpolicy="no-referrer-when-downgrade"
      ></iframe>
      <!-- #endif -->
      <!-- #ifndef H5 -->
      <map
        class="map-box"
        :latitude="latitude"
        :longitude="longitude"
        :markers="markers"
        :scale="15"
        show-location
        @markertap="handleMarkerTap"
      />
      <!-- #endif -->
      <view class="map-caption card">
        <text class="caption-label">当前位置</text>
        <text class="caption-title">{{ CAMPUS.name }}</text>
        <text class="caption-copy">{{ CAMPUS.campus }} · {{ CAMPUS.address }}</text>
      </view>
      <button class="recenter-button" aria-label="回到学院位置" @click="recenterCampus">
        <image src="/static/icon/local.png" mode="aspectFit" />
      </button>
    </view>

    <view class="shop-content">
      <view class="sheet-handle" />
      <view class="sheet-heading">
        <view><text class="sheet-kicker">DINING LOCATIONS</text><text class="sheet-title">选择就餐地点</text></view>
        <view class="service-status"><text class="status-dot"></text><text>营业中</text></view>
      </view>
      <view class="search-box"><text class="search-symbol">⌕</text><input v-model="keyword" placeholder="搜索餐厅名称或地址" confirm-type="search" /><text v-if="keyword" class="clear" @click="keyword = ''">×</text></view>
      <view class="result-title"><text>附近餐厅</text><text class="result-count">{{ filteredStores.length }} 家</text></view>
      <scroll-view scroll-y class="store-list">
        <view v-for="store in filteredStores" :key="store.id" class="store-item card" :class="{ selected: store.id === state.currentStoreId }" @click="select(store)">
          <image class="store-cover" :src="store.image" mode="aspectFill" />
          <view class="store-main">
            <view class="store-row"><text class="store-name">{{ store.name }}</text><text class="store-distance">{{ formatDistance(store.distance) }}</text></view>
            <text class="store-address">{{ store.address }}</text>
            <view class="store-meta"><text :class="store.status">{{ store.status === 'open' ? '营业中' : '客流较多' }}</text><text>约 {{ store.waitMinutes }} 分钟</text></view>
            <text class="store-hours">{{ store.hours }}</text>
            <view class="service-row"><text v-for="service in store.services" :key="service" class="chip">{{ service }}</text></view>
          </view>
          <text v-if="store.id === state.currentStoreId" class="selected-mark">已选择</text>
        </view>
      </scroll-view>
      <button class="primary-button confirm-button" @click="goOrder">进入 {{ currentStore.shortName }} 点餐</button>
    </view>
  </view>
</template>

<style scoped lang="scss">
.shop-page{height:100vh;overflow:hidden;padding:0;background:var(--oat-50)}
.map-wrap{position:relative;height:45vh;min-height:430rpx;overflow:hidden;background:#e6ebf6}.map-box{width:100%;height:100%}.osm-frame{display:block;border:0;background:#edf1f7}
.map-caption{position:absolute;z-index:2;left:24rpx;top:24rpx;max-width:430rpx;padding:17rpx 21rpx;border-color:rgba(255,255,255,.8);border-radius:20rpx;background:rgba(255,255,255,.92);box-shadow:0 8rpx 28rpx rgba(16,38,111,.12);backdrop-filter:blur(10rpx)}.map-caption text{display:block}.caption-label{color:var(--brand);font-size:17rpx;font-weight:750;letter-spacing:2rpx}.caption-title{margin-top:5rpx;font-size:24rpx;font-weight:750}.caption-copy{margin-top:5rpx;color:var(--muted);font-size:18rpx}
.recenter-button{position:absolute;z-index:3;right:24rpx;bottom:32rpx;width:68rpx;height:68rpx;padding:0;display:flex;align-items:center;justify-content:center;border:1rpx solid rgba(6,55,201,.1);border-radius:50%;background:#fff;box-shadow:0 8rpx 24rpx rgba(16,38,111,.17)}.recenter-button image{width:32rpx;height:32rpx}
.shop-content{position:relative;z-index:4;height:calc(55vh + 26rpx);margin-top:-26rpx;padding:12rpx 28rpx 170rpx;border-radius:32rpx 32rpx 0 0;background:var(--oat-50);box-shadow:0 -10rpx 35rpx rgba(34,48,42,.08)}.sheet-handle{width:68rpx;height:7rpx;margin:0 auto 16rpx;border-radius:5rpx;background:#d6d2ca}.sheet-heading{display:flex;align-items:center;justify-content:space-between;margin:0 2rpx 19rpx}.sheet-heading text{display:block}.sheet-kicker{color:var(--brand);font-size:16rpx;font-weight:750;letter-spacing:3rpx}.sheet-title{margin-top:3rpx;font-size:31rpx;font-weight:780}.service-status{display:flex;align-items:center;gap:8rpx;padding:10rpx 15rpx;border-radius:24rpx;color:var(--brand);background:var(--brand-soft);font-size:19rpx;font-weight:650}.status-dot{width:10rpx;height:10rpx;border-radius:50%;background:var(--brand)}
.search-box{display:flex;align-items:center;gap:14rpx;height:76rpx;padding:0 23rpx;border:1rpx solid var(--line);border-radius:22rpx;background:#fff;box-shadow:0 6rpx 20rpx rgba(16,38,111,.04)}.search-box input{flex:1;font-size:23rpx}.search-symbol{font-size:24rpx;color:var(--brand)}.clear{font-size:34rpx;color:var(--muted)}
.result-title{display:flex;justify-content:space-between;margin:24rpx 2rpx 14rpx;font-size:27rpx;font-weight:750}.result-count{color:var(--muted);font-size:20rpx;font-weight:400}.store-list{height:calc(55vh - 320rpx)}
.store-item{position:relative;display:flex;gap:18rpx;margin-bottom:14rpx;padding:18rpx;border-radius:22rpx;box-shadow:0 7rpx 22rpx rgba(16,38,111,.045)}.store-item.selected{border:1rpx solid rgba(6,55,201,.28);background:linear-gradient(135deg,#fff 60%,#edf2ff)}.store-cover{width:138rpx;height:166rpx;flex:0 0 138rpx;border-radius:17rpx;background:#e6e9f1}.store-main{min-width:0;flex:1}.store-row{display:flex;justify-content:space-between;gap:12rpx}.store-name{min-width:0;flex:1;font-size:24rpx;font-weight:760;line-height:1.3}.store-distance{flex:none;color:var(--brand);font-size:19rpx;font-weight:650}.store-address{display:block;margin-top:7rpx;color:var(--muted);font-size:18rpx;line-height:1.35}.store-meta{display:flex;gap:13rpx;margin-top:9rpx;color:var(--muted);font-size:17rpx}.store-meta .open{color:var(--brand);font-weight:700}.store-meta .busy{color:var(--danger);font-weight:700}.store-hours{display:block;margin-top:5rpx;color:#858891;font-size:16rpx}.service-row{display:flex;gap:7rpx;margin-top:10rpx}.service-row .chip{min-height:32rpx;padding:0 9rpx;color:#40527d;background:#f0f3fa;font-size:15rpx}.selected-mark{position:absolute;left:29rpx;bottom:27rpx;padding:5rpx 9rpx;border-radius:12rpx;color:#fff;background:rgba(6,55,201,.94);font-size:15rpx;font-weight:750}
.confirm-button{position:fixed;z-index:10;left:28rpx;right:28rpx;bottom:calc(116rpx + env(safe-area-inset-bottom))}
@media screen and (min-width:760px){.confirm-button{left:50%;right:auto;width:694px;transform:translateX(-50%)}}
</style>
