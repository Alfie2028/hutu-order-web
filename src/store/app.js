import { computed, reactive } from 'vue'
import { COUPONS, DEMO_USER, PRODUCTS, STORES } from '@/data/catalog'
import { createOrderNo } from '@/utils/format'

const STORAGE_KEY = 'CAMPUS_COFFEE_DEMO_V4'
const demoOrderItem = (productId, quantity = 1, selectedOptions = []) => {
  const product = PRODUCTS.find((item) => item.id === productId)
  const extras = selectedOptions.reduce((sum, option) => sum + Number(option.extraCents || 0), 0)
  return { key: `${productId}:demo`, productId, name: product.name, image: product.image, fallback: product.fallback, selectedOptions, unitPriceCents: product.priceCents + extras, quantity }
}
const createDemoOrders = () => {
  const activeItems = [demoOrderItem('coconut-latte', 1, [{ id: 'large', name: '大杯', groupName: '杯型', extraCents: 300 }, { id: 'iced', name: '冰', groupName: '温度', extraCents: 0 }, { id: 'half', name: '半糖', groupName: '甜度', extraCents: 0 }])]
  const historyItems = [demoOrderItem('grape-tea'), demoOrderItem('croissant')]
  return [
    { id: 'HT-DEMO-0928', storeId: STORES[0].id, storeName: STORES[0].name, mode: 'pickup', status: 'making', statusText: '制作中', pickupCode: '218', createdAt: Date.now() - 6 * 60 * 1000, pickupTime: '尽快取餐', remark: '', items: activeItems, subtotalCents: 2100, discountCents: 0, totalCents: 2100, couponName: '' },
    { id: 'HT-DEMO-0927', storeId: STORES[0].id, storeName: STORES[0].name, mode: 'dineIn', status: 'completed', statusText: '已完成', pickupCode: '506', createdAt: Date.now() - 26 * 60 * 60 * 1000, pickupTime: '15 分钟后', remark: '少冰', items: historyItems, subtotalCents: 2800, discountCents: 0, totalCents: 2800, couponName: '' },
  ]
}
const initialState = () => ({ initialized: false, currentStoreId: STORES[0].id, orderMode: 'pickup', cart: [], orders: createDemoOrders(), favoriteIds: ['coconut-latte', 'grape-tea'], couponIds: COUPONS.map((coupon) => coupon.id), user: { ...DEMO_USER } })
const state = reactive(initialState())

function persist() {
  if (!state.initialized) return
  uni.setStorageSync(STORAGE_KEY, { currentStoreId: state.currentStoreId, orderMode: state.orderMode, cart: state.cart, orders: state.orders, favoriteIds: state.favoriteIds, couponIds: state.couponIds, user: state.user })
}

export function initializeDemoStore() {
  if (state.initialized) return
  const saved = uni.getStorageSync(STORAGE_KEY)
  if (saved && typeof saved === 'object') Object.assign(state, initialState(), saved)
  state.initialized = true
}

const cartKey = (productId, options) => `${productId}:${options.map((option) => option.id).sort().join('-')}`

export function useAppStore() {
  initializeDemoStore()
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
  function addToCart(productId, selectedOptions = [], quantity = 1) {
    const product = PRODUCTS.find((item) => item.id === productId)
    if (!product) return
    const options = selectedOptions.map((option) => ({ id: option.id, name: option.name, groupName: option.groupName, extraCents: Number(option.extraCents || 0) }))
    const key = cartKey(productId, options)
    const existing = state.cart.find((item) => item.key === key)
    if (existing) existing.quantity += quantity
    else state.cart.push({ key, productId, name: product.name, image: product.image, fallback: product.fallback, selectedOptions: options, unitPriceCents: product.priceCents + options.reduce((sum, option) => sum + option.extraCents, 0), quantity })
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
  function reorder(orderId) { const order = findOrder(orderId); if (!order) return; state.currentStoreId = order.storeId; state.orderMode = order.mode; state.cart = JSON.parse(JSON.stringify(order.items)); persist() }
  function resetDemo() { Object.assign(state, initialState(), { initialized: true }); persist() }

  return { state, currentStore, cartCount, cartSubtotal, setStore, setOrderMode, addToCart, updateCartQuantity, clearCart, toggleFavorite, createOrder, findOrder, advanceOrder, reorder, resetDemo }
}
