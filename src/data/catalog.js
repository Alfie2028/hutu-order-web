export const CAMPUS = {
  name: '河南农业大学软件学院', campus: '许昌校区',
  address: '许昌市建安区劳动北路', latitude: 34.13765, longitude: 113.80378,
}

export const STORES = [
  { id: 'henau-campus', name: '农大校园店', shortName: '农大校园店', address: '许昌校区生活广场 1 层', distance: 180, openTime: '07:30', closeTime: '22:00', status: 'open', waitMinutes: 8, services: ['堂食', '外带', '校园送'], latitude: 34.13652, longitude: 113.80791 },
  { id: 'nongda-road', name: '农大路店', shortName: '农大路店', address: '农大路与劳动北路交叉口东 120 米', distance: 760, openTime: '08:00', closeTime: '21:30', status: 'open', waitMinutes: 12, services: ['堂食', '外带'], latitude: 34.14031, longitude: 113.80483 },
  { id: 'jianan-center', name: '建安中心店', shortName: '建安中心店', address: '建安区新元大道青年汇 1 层', distance: 2300, openTime: '09:00', closeTime: '22:30', status: 'busy', waitMinutes: 18, services: ['堂食', '外带', '停车'], latitude: 34.12582, longitude: 113.82512 },
]

export const CATEGORIES = [
  { id: 'popular', name: '人气必喝' }, { id: 'coffee', name: '精选咖啡' },
  { id: 'latte', name: '拿铁特调' }, { id: 'tea', name: '轻茶果饮' }, { id: 'bakery', name: '现烤烘焙' },
]

const coffeeOptions = [
  { id: 'size', name: '杯型', required: true, multiple: false, options: [{ id: 'regular', name: '中杯', extraCents: 0 }, { id: 'large', name: '大杯', extraCents: 300 }] },
  { id: 'temperature', name: '温度', required: true, multiple: false, options: [{ id: 'iced', name: '冰', extraCents: 0 }, { id: 'hot', name: '热', extraCents: 0 }] },
  { id: 'sweetness', name: '甜度', required: true, multiple: false, options: [{ id: 'none', name: '不另加糖', extraCents: 0 }, { id: 'half', name: '半糖', extraCents: 0 }, { id: 'full', name: '标准糖', extraCents: 0 }] },
  { id: 'extras', name: '加料', required: false, multiple: true, options: [{ id: 'shot', name: '加一份浓缩', extraCents: 300 }, { id: 'oat', name: '换燕麦奶', extraCents: 400 }, { id: 'cream', name: '海盐奶盖', extraCents: 300 }] },
]

export const PRODUCTS = [
  { id: 'coconut-latte', categoryId: 'popular', name: '生椰拿铁', subtitle: '生椰乳与浓缩咖啡的清爽碰撞', priceCents: 1800, originalPriceCents: 2200, badge: '校园热卖', sales: 1268, image: '/static/image/menu-coffee.jpg', fallback: '饮品', options: coffeeOptions },
  { id: 'dirty', categoryId: 'popular', name: '黑金 Dirty', subtitle: '冰博鲜奶托起热浓缩', priceCents: 2000, badge: '店长推荐', sales: 986, image: '/static/image/menu-coffee.jpg', fallback: '咖啡', options: coffeeOptions },
  { id: 'americano', categoryId: 'coffee', name: '经典美式', subtitle: '干净明亮，带有坚果与黑巧风味', priceCents: 1200, badge: '轻负担', sales: 845, image: '/static/image/menu-coffee.jpg', fallback: '咖啡', options: coffeeOptions },
  { id: 'orange-americano', categoryId: 'coffee', name: '橙 C 美式', subtitle: '鲜橙果香融合清爽咖啡', priceCents: 1600, badge: '活力上新', sales: 532, image: '/static/image/menu-coffee.jpg', fallback: '咖啡', options: coffeeOptions },
  { id: 'caramel-latte', categoryId: 'latte', name: '焦糖燕麦拿铁', subtitle: '焦糖香气、燕麦奶与咖啡层次丰富', priceCents: 2100, badge: '秋日限定', sales: 621, image: '/static/image/menu-coffee.jpg', fallback: '饮品', options: coffeeOptions },
  { id: 'matcha-latte', categoryId: 'latte', name: '青岚抹茶拿铁', subtitle: '宇治抹茶与醇厚牛奶', priceCents: 1900, badge: '不含咖啡', sales: 488, image: '/static/image/menu-tea.jpg', fallback: '饮品', options: coffeeOptions.filter((group) => group.id !== 'extras') },
  { id: 'grape-tea', categoryId: 'tea', name: '青提茉莉冰茶', subtitle: '阳光青提、茉莉茶与清凉碎冰', priceCents: 1600, badge: '清爽推荐', sales: 772, image: '/static/image/menu-tea.jpg', fallback: '茶饮', options: coffeeOptions.filter((group) => ['size', 'sweetness'].includes(group.id)) },
  { id: 'lemon-tea', categoryId: 'tea', name: '鸭屎香柠檬茶', subtitle: '现捣黄柠檬，茶香鲜明', priceCents: 1400, badge: '真果汁', sales: 692, image: '/static/image/menu-tea.jpg', fallback: '茶饮', options: coffeeOptions.filter((group) => ['size', 'sweetness'].includes(group.id)) },
  { id: 'croissant', categoryId: 'bakery', name: '法式黄油可颂', subtitle: '层层酥脆，每日门店现烤', priceCents: 1200, badge: '现烤', sales: 410, image: '/static/image/menu-bakery.jpg', fallback: '烘焙', options: [] },
  { id: 'bagel', categoryId: 'bakery', name: '烟熏鸡肉贝果', subtitle: '高蛋白轻食，课间也能吃饱', priceCents: 1800, badge: '轻食', sales: 352, image: '/static/image/menu-bakery.jpg', fallback: '轻食', options: [] },
]

export const COUPONS = [
  { id: 'new-user', name: '新人立减券', thresholdCents: 2000, discountCents: 500, expires: '2026-12-31' },
  { id: 'campus', name: '农大校园券', thresholdCents: 3000, discountCents: 600, expires: '2026-12-31' },
]

export const DEMO_USER = { id: 'demo-student', name: '同学', title: '校园会员', avatar: '/static/image/avatar/default.jpg', points: 860, level: 3, nextLevelPoints: 1200 }
