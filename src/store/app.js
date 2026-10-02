import { computed, reactive } from 'vue'
import { COUPONS, PRODUCTS, STALLS, STORES, USER_PROFILE } from '@/data/catalog'
import { createOrderNo } from '@/utils/format'

const STORAGE_KEY = 'CAMPUS_ORDERING_V11'
const seedOrderItem = (productId, quantity = 1, selectedOptions = []) => {
  const product = PRODUCTS.find((item) => item.id === productId)
  const extras = selectedOptions.reduce((sum, option) => sum + Number(option.extraCents || 0), 0)
  return { key: `${productId}:seed`, productId, name: product.name, stallName: product.stallName, image: product.image, fallback: product.fallback, selectedOptions, unitPriceCents: product.priceCents + extras, quantity }
}
const createInitialOrders = () => {
  const activeItems = [seedOrderItem('black-pepper-chicken-rice', 1, [{ id: 'regular', name: '标准份', groupName: '份量', extraCents: 0 }])]
  const historyItems = [seedOrderItem('henan-huimian'), seedOrderItem('beef-pan-fried-buns')]
  return [
    { id: 'XC-20261002-0928', storeId: STORES[0].id, storeName: STORES[0].name, mode: 'pickup', status: 'making', statusText: '制作中', pickupCode: '218', createdAt: Date.now() - 6 * 60 * 1000, pickupTime: '尽快取餐', remark: '', items: activeItems, subtotalCents: 1880, discountCents: 0, totalCents: 1880, couponName: '' },
    { id: 'XC-20261001-0927', storeId: STORES[0].id, storeName: STORES[0].name, mode: 'dineIn', status: 'completed', statusText: '已完成', pickupCode: '506', createdAt: Date.now() - 26 * 60 * 60 * 1000, pickupTime: '15 分钟后', remark: '微辣', items: historyItems, subtotalCents: 3160, discountCents: 0, totalCents: 3160, couponName: '' },
  ]
}
const initialState = () => ({ initialized: false, currentStoreId: STORES[0].id, selectedStallId: STALLS[0].id, orderMode: 'pickup', cart: [], orders: createInitialOrders(), favoriteIds: ['black-pepper-chicken-rice', 'henan-huimian'], couponIds: COUPONS.map((coupon) => coupon.id), user: { ...USER_PROFILE } })
const state = reactive(initialState())

function persist() {
  if (!state.initialized) return
  uni.setStorageSync(STORAGE_KEY, { currentStoreId: state.currentStoreId, selectedStallId: state.selectedStallId, orderMode: state.orderMode, cart: state.cart, orders: state.orders, favoriteIds: state.favoriteIds, couponIds: state.couponIds, user: state.user })
}

export function initializeStore() {
  if (state.initialized) return
  const saved = uni.getStorageSync(STORAGE_KEY)
  if (saved && typeof saved === 'object') Object.assign(state, initialState(), saved)
  state.initialized = true
}

const cartKey = (productId, options) => `${productId}:${options.map((option) => option.id).sort().join('-')}`

export function useAppStore() {
  initializeStore()
  const currentStore = computed(() => STORES.find((store) => store.id === state.currentStoreId) || STORES[0])
  const cartCount = computed(() => state.cart.reduce((sum, item) => sum + item.quantity, 0))
  const cartSubtotal = computed(() => state.cart.reduce((sum, item) => sum + item.unitPriceCents * item.quantity, 0))

  function setStore(storeId) {
    if (!STORES.some((store) => store.id === storeId)) return
    if (state.currentStoreId !== storeId && state.cart.length) state.cart = []
    state.currentStoreId = storeId
    persist()
  }
  function setOrderMode(mode) { state.orderMode = mode === 'dineIn' ? 'dineIn' : 'pickup'; persist() }
  function setStall(stallId) { if (STALLS.some((stall) => stall.id === stallId)) { state.selectedStallId = stallId; persist() } }
  function addToCart(productId, selectedOptions = [], quantity = 1) {
    const product = PRODUCTS.find((item) => item.id === productId)
    if (!product) return
    const options = selectedOptions.map((option) => ({ id: option.id, name: option.name, groupName: option.groupName, extraCents: Number(option.extraCents || 0) }))
    const key = cartKey(productId, options)
    const existing = state.cart.find((item) => item.key === key)
    if (existing) existing.quantity += quantity
    else state.cart.push({ key, productId, name: product.name, stallName: product.stallName, image: product.image, fallback: product.fallback, selectedOptions: options, unitPriceCents: product.priceCents + options.reduce((sum, option) => sum + option.extraCents, 0), quantity })
    persist()
  }
  function updateCartQuantity(key, quantity) {
    const item = state.cart.find((entry) => entry.key === key)
    if (!item) return
    if (quantity <= 0) state.cart = state.cart.filter((entry) => entry.key !== key)
    else item.quantity = quantity
    persist()
  }
  function clearCart() { state.cart = []; persist() }
  function toggleFavorite(productId) { state.favoriteIds = state.favoriteIds.includes(productId) ? state.favoriteIds.filter((id) => id !== productId) : [...state.favoriteIds, productId]; persist() }
  function createOrder({ couponId = '', remark = '', pickupTime = '尽快取餐' } = {}) {
    if (!state.cart.length) return null
    const coupon = COUPONS.find((item) => item.id === couponId)
    const subtotalCents = cartSubtotal.value
    const discountCents = coupon && subtotalCents >= coupon.thresholdCents ? coupon.discountCents : 0
    const order = { id: createOrderNo(), storeId: currentStore.value.id, storeName: currentStore.value.name, mode: state.orderMode, status: 'making', statusText: '制作中', pickupCode: String(Math.floor(100 + Math.random() * 900)), createdAt: Date.now(), pickupTime, remark, items: JSON.parse(JSON.stringify(state.cart)), subtotalCents, discountCents, totalCents: Math.max(0, subtotalCents - discountCents), couponName: discountCents ? coupon.name : '' }
    state.orders.unshift(order)
    if (discountCents) state.couponIds = state.couponIds.filter((id) => id !== couponId)
    state.user.points += Math.floor(order.totalCents / 100)
    state.cart = []
    persist()
    return order
  }
  const findOrder = (orderId) => state.orders.find((order) => order.id === orderId)
  function advanceOrder(orderId) {
    const order = findOrder(orderId)
    if (!order) return
    const sequence = [['making', '制作中'], ['ready', '待取餐'], ['completed', '已完成']]
    const index = sequence.findIndex(([status]) => status === order.status)
    const next = sequence[Math.min(index + 1, sequence.length - 1)]
    order.status = next[0]; order.statusText = next[1]; persist()
  }
  function reorder(orderId) { const order = findOrder(orderId); if (!order) return; state.currentStoreId = order.storeId; state.orderMode = order.mode; state.cart = JSON.parse(JSON.stringify(order.items)); const firstProduct = PRODUCTS.find((product) => product.id === order.items[0]?.productId); if (firstProduct) state.selectedStallId = firstProduct.stallId; persist() }
  function resetStore() { Object.assign(state, initialState(), { initialized: true }); persist() }

  return { state, currentStore, cartCount, cartSubtotal, setStore, setOrderMode, setStall, addToCart, updateCartQuantity, clearCart, toggleFavorite, createOrder, findOrder, advanceOrder, reorder, resetStore }
}
