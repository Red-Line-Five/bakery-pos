// ════════════════════════════════════════════════════════════
//  data.js — فرن الأصلي
//  عدّل هذا الملف لتغيير الأصناف أو الإضافات
//  لا حاجة لتغيير bakery-pos.html
// ════════════════════════════════════════════════════════════

// ── الإضافات (تظهر كـ checkbox عند كل صنف) ──────────────────
var DEF_EXTRAS = [
  {id:'x1', name:'خضرة',          price:30000},
  {id:'x2', name:'7 حبوب',         price:30000},
  {id:'x3', name:'جريش',            price:30000},
  {id:'x4', name:'أسمر',            price:30000},
  {id:'x5', name:'عسكر',     price:-20000},
  {id:'x6', name:'محمصة',   price:0},

];

// ── تحديد الإضافات المسموح بها حسب نوع الصنف ─────────────────
//  - manousheh: '*' يعني كل الإضافات
//  - pizza: ضع هنا ids الإضافات المسموح بها للبيتزا
//    مثال: ['x1','x5'] ويمكن إضافة أي id جديد لاحقاً
var DEF_EXTRA_IDS_BY_TYPE = {
  manousheh: '*',
  pizza: ['x1', 'x5'],
 simple: [ 'x5']
};

// ── قائمة الأصناف ────────────────────────────────────────────
//  type: 'manousheh'  → priceA (عادي) + priceB (مشروحة)
//  type: 'pizza'      → priceS (صغير) + priceM (وسط) + priceL (كبير)
//  type: 'simple'     → price (سعر واحد)

// ─────────────────────────────────────────────────────────────
var DEF = [

  // ── مناقيش ──────────────────────────────────────────────
  {cat:'مناقيش', name:'جبنة عكاوي',               desc:'', type:'manousheh', priceA:160000, priceB:200000},
  {cat:'مناقيش', name:'جبنة + ريحان + فطر + حرة', desc:'', type:'manousheh', priceA:200000, priceB:230000},
  {cat:'مناقيش', name:'4 شيز',                     desc:'', type:'manousheh', priceA:200000, priceB:230000},
  {cat:'مناقيش', name:'حلوم',                      desc:'', type:'manousheh', priceA:200000, priceB:230000},
  {cat:'مناقيش', name:'قشقوان',                    desc:'', type:'manousheh', priceA:200000, priceB:250000},
  {cat:'مناقيش', name:'كوكتيل',                    desc:'', type:'manousheh', priceA:150000, priceB:180000},
  {cat:'مناقيش', name:'زعتر',                      desc:'', type:'manousheh', priceA:50000,  priceB:70000},
  {cat:'مناقيش', name:'زعتر مع حر',                desc:'', type:'manousheh', priceA:70000,  priceB:100000},
  {cat:'مناقيش', name:'زعتر مع قشقوان',            desc:'', type:'manousheh', priceA:170000, priceB:200000},
  {cat:'مناقيش', name:'زعتر مع بصل وبندورة',       desc:'', type:'manousheh', priceA:120000, priceB:150000},
  {cat:'مناقيش', name:'كشك',                       desc:'', type:'manousheh', priceA:150000, priceB:180000},
  {cat:'مناقيش', name:'كشك وجبنة',                 desc:'', type:'manousheh', priceA:170000, priceB:200000},
  {cat:'مناقيش', name:'بصل وبندورة',               desc:'', type:'manousheh', priceA:150000, priceB:180000},
  {cat:'مناقيش', name:'بصل وبندورة مع جبنة',       desc:'', type:'manousheh', priceA:170000, priceB:200000},
  {cat:'مناقيش', name:'محمرة',                     desc:'', type:'manousheh', priceA:100000, priceB:120000},
  {cat:'مناقيش', name:'محمرة مع جبنة',             desc:'', type:'manousheh', priceA:140000, priceB:170000},
  {cat:'مناقيش', name:'لبنة',                      desc:'', type:'manousheh', priceA:150000, priceB:180000},
  {cat:'مناقيش', name:'مرتديلا وجبنة',             desc:'', type:'manousheh', priceA:220000, priceB:250000},
  {cat:'مناقيش', name:'جبش مدخن وجبنة',            desc:'', type:'manousheh', priceA:230000, priceB:280000},
  {cat:'مناقيش', name:'لحمة',                      desc:'', type:'manousheh', priceA:230000, priceB:280000},
  {cat:'مناقيش', name:'لحمة وجبنة',                desc:'', type:'manousheh', priceA:250000, priceB:300000},
  {cat:'مناقيش', name:'سجق',                       desc:'', type:'manousheh', priceA:230000, priceB:280000},
  {cat:'مناقيش', name:'سجق وجبنة',                 desc:'', type:'manousheh', priceA:250000, priceB:300000},
  {cat:'مناقيش', name:'كفتة',                      desc:'', type:'manousheh', priceA:250000, priceB:280000},
  {cat:'مناقيش', name:'كفتة وجبنة',                desc:'', type:'manousheh', priceA:250000, priceB:300000},
  {cat:'مناقيش', name:'بيروني مع جبنة',            desc:'', type:'manousheh', priceA:250000, priceB:300000},
  {cat:'مناقيش', name:'طاووق',                     desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'فاهيتا',                    desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'باربيكيو شيكن',             desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'تيرياكي شيكن',              desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'سويت شيكن',                 desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'ديناميت شيكن',              desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'شيلي شيكن',                 desc:'', type:'manousheh', priceA:280000, priceB:350000},
  {cat:'مناقيش', name:'دوبليكس',                   desc:'', type:'simple',    price:200000},
  {cat:'مناقيش', name:'سباناخ',                    desc:'مع خضرة', type:'simple', price:100000},
  {cat:'مناقيش', name:'شوكولا',                    desc:'', type:'simple',    price:180000},

  // ── بيتزا ────────────────────────────────────────────────
  {cat:'بيتزا', name:'Pepperoni',        desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Vegetarian',       desc:'', type:'pizza', priceS:400000, priceM:600000,  priceL:1000000},
  {cat:'بيتزا', name:'Margherita',       desc:'', type:'pizza', priceS:350000, priceM:550000,  priceL:850000},
  {cat:'بيتزا', name:'4 Cheese',         desc:'', type:'pizza', priceS:450000, priceM:650000,  priceL:1100000},
  {cat:'بيتزا', name:'Crazy Franc',      desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Sujuk',            desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Lebanese',         desc:'', type:'pizza', priceS:450000, priceM:650000,  priceL:1100000},
  {cat:'بيتزا', name:'Fajita',           desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Sweet and Sour',   desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Barbecue Chicken', desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Teriyaki',         desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Dynamite Chicken', desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Sweet Chili',      desc:'', type:'pizza', priceS:500000, priceM:700000,  priceL:1150000},
  {cat:'بيتزا', name:'Sweet Shrimps',    desc:'', type:'pizza', priceS:600000, priceM:1000000, priceL:1600000},
  {cat:'بيتزا', name:'Dynamite Shrimps', desc:'', type:'pizza', priceS:600000, priceM:1000000, priceL:1600000},
  {cat:'بيتزا', name:'Teriyaki Shrimps', desc:'', type:'pizza', priceS:600000, priceM:1000000, priceL:1600000},
  {cat:'بيتزا', name:'Sweet Chili Shrimps', desc:'', type:'pizza', priceS:600000, priceM:1000000, priceL:1600000},

  // ── معجنات────────────────────────────────────────────────
  {cat:'معجنات', name:'دزينة معجنات',                    desc:'', type:'simple',    price:300000},
  {cat:'معجنات', name:'دزينة معجنات دجاج',                    desc:'', type:'simple',    price:350000},
  {cat:'معجنات', name:'دزينة سباناخ',                    desc:'', type:'simple',    price:300000},
  {cat:'معجنات', name:'دزينة صفيحة بعلبكية',                    desc:'', type:'simple',    price:350000},

  // ── المشروبات────────────────────────────────────────────────
  {cat:'مشروبات', name:'PEPSI',                    desc:'', type:'simple',    price:80000},
  {cat:'مشروبات', name:'DIET PEPSI',                    desc:'', type:'simple',    price:80000},
  {cat:'مشروبات', name:'7 UP',                    desc:'', type:'',    price:80000},
  {cat:'مشروبات', name:'DIET 7 UP',                    desc:'', type:'simple',    price:80000},
  {cat:'مشروبات', name:'لبن عيران',                    desc:'', type:'simple',    price:60000},
  {cat:'مشروبات', name:'TOP juice',                    desc:'', type:'simple',    price:25000},
  {cat:'مشروبات', name:'WATER',                    desc:'', type:'simple',    price:25000},

];
