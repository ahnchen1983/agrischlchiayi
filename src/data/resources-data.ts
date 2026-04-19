/**
 * Agricultural Resources Database
 * 農業資源盤點 - Traditional Chinese (繁體中文) Only
 * Covering: Central Ministries, Local Agencies, Marketing Platforms, Financing, Water & Sustainability
 */

export interface ResourceSite {
  nameKey: string; // i18n key, e.g. 'resources.site.moa'
  url: string;
  domain: string;
  descKey?: string; // optional description i18n key (featured sites only)
  featured?: boolean; // Top 3 featured per chapter
}

export interface HeroCategory {
  id: string;
  labelKey: string;
  color: string;
  sites: ResourceSite[];
}

// ─── Hero Mindmap Data (5 Agricultural Categories) ───
export const heroCategories: HeroCategory[] = [
  {
    id: 'agri-governance',
    labelKey: 'resources.category.agri.governance.label',
    color: '#15803d', // Deeper green for agriculture
    sites: [
      {
        nameKey: 'resources.site.moa.main',
        url: 'https://www.moa.gov.tw/',
        domain: 'moa.gov.tw',
        featured: true,
        descKey: 'resources.featured.moa',
      },
      {
        nameKey: 'resources.site.cyhg',
        url: 'https://www.cyhg.gov.tw/',
        domain: 'cyhg.gov.tw',
        featured: true,
        descKey: 'resources.featured.cyhg',
      },
      {
        nameKey: 'resources.site.trit',
        url: 'https://www.trit.gov.tw/',
        domain: 'trit.gov.tw',
      },
      {
        nameKey: 'resources.site.swcb',
        url: 'https://www.swcb.gov.tw/',
        domain: 'swcb.gov.tw',
      },
      {
        nameKey: 'resources.site.fa',
        url: 'https://www.fa.gov.tw/',
        domain: 'fa.gov.tw',
        featured: true,
        descKey: 'resources.featured.fa',
      },
    ],
  },
  {
    id: 'agri-technology',
    labelKey: 'resources.category.agri.technology.label',
    color: '#059669', // Standard green
    sites: [
      {
        nameKey: 'resources.site.tais',
        url: 'https://www.tais.gov.tw/',
        domain: 'tais.gov.tw',
        featured: true,
        descKey: 'resources.featured.tais',
      },
      {
        nameKey: 'resources.site.afrec',
        url: 'https://www.afrec.gov.tw/',
        domain: 'afrec.gov.tw',
      },
      {
        nameKey: 'resources.site.ttsdcc',
        url: 'https://www.ttsdcc.org.tw/',
        domain: 'ttsdcc.org.tw',
      },
      {
        nameKey: 'resources.site.isia',
        url: 'https://www.isia.org.tw/',
        domain: 'isia.org.tw',
      },
      {
        nameKey: 'resources.site.tesd',
        url: 'https://tesd.survey.sinica.edu.tw/',
        domain: 'tesd.survey.sinica.edu.tw',
      },
    ],
  },
  {
    id: 'agri-marketing',
    labelKey: 'resources.category.agri.marketing.label',
    color: '#10b981', // Light green
    sites: [
      {
        nameKey: 'resources.site.coa.market',
        url: 'https://www.coa.gov.tw/ws.php?id=2449',
        domain: 'coa.gov.tw',
        featured: true,
        descKey: 'resources.featured.coa.market',
      },
      {
        nameKey: 'resources.site.shopee',
        url: 'https://shopee.tw/',
        domain: 'shopee.tw',
      },
      {
        nameKey: 'resources.site.pchome',
        url: 'https://www.pchome.com.tw/',
        domain: 'pchome.com.tw',
      },
      {
        nameKey: 'resources.site.momo',
        url: 'https://www.momoshop.com.tw/',
        domain: 'momoshop.com.tw',
      },
      {
        nameKey: 'resources.site.gomaji',
        url: 'https://www.gomaji.com/',
        domain: 'gomaji.com',
      },
    ],
  },
  {
    id: 'agri-finance',
    labelKey: 'resources.category.agri.finance.label',
    color: '#047857', // Dark green
    sites: [
      {
        nameKey: 'resources.site.acgf',
        url: 'https://www.acgf.org.tw/',
        domain: 'acgf.org.tw',
        featured: true,
        descKey: 'resources.featured.acgf',
      },
      {
        nameKey: 'resources.site.coa.subsidy',
        url: 'https://www.coa.gov.tw/theme_list.php?theme=subsidy',
        domain: 'coa.gov.tw',
      },
      {
        nameKey: 'resources.site.tai',
        url: 'https://www.taii.org.tw/',
        domain: 'taii.org.tw',
      },
      {
        nameKey: 'resources.site.fsc',
        url: 'https://www.fsc.gov.tw/',
        domain: 'fsc.gov.tw',
      },
      {
        nameKey: 'resources.site.moa.insurance',
        url: 'https://www.moa.gov.tw/theme_list.php?theme=insurance',
        domain: 'moa.gov.tw',
      },
    ],
  },
  {
    id: 'agri-sustainability',
    labelKey: 'resources.category.agri.sustainability.label',
    color: '#065f46', // Forest green
    sites: [
      {
        nameKey: 'resources.site.swcb.water',
        url: 'https://www.swcb.gov.tw/',
        domain: 'swcb.gov.tw',
        featured: true,
        descKey: 'resources.featured.swcb.water',
      },
      {
        nameKey: 'resources.site.coa.organic',
        url: 'https://www.coa.gov.tw/ws.php?id=2461',
        domain: 'coa.gov.tw',
      },
      {
        nameKey: 'resources.site.moenv',
        url: 'https://www.moenv.gov.tw/',
        domain: 'moenv.gov.tw',
      },
      {
        nameKey: 'resources.site.cwa',
        url: 'https://www.cwa.gov.tw/',
        domain: 'cwa.gov.tw',
      },
      {
        nameKey: 'resources.site.nstc',
        url: 'https://www.nstc.gov.tw/',
        domain: 'nstc.gov.tw',
      },
    ],
  },
];

// ─── Chapter 1: 農業行政與管理 (Agricultural Administration & Management) ───

// Subcategory 1.1: 中央農業部會 (Central Agricultural Ministries)
export const agriGovernanceCentral: ResourceSite[] = [
  {
    nameKey: 'resources.site.moa.main',
    url: 'https://www.moa.gov.tw/',
    domain: 'moa.gov.tw',
    featured: true,
    descKey: 'resources.featured.moa',
  },
  {
    nameKey: 'resources.site.moa.crops',
    url: 'https://www.moa.gov.tw/ws.php?id=24649',
    domain: 'moa.gov.tw',
  },
  {
    nameKey: 'resources.site.moa.livestock',
    url: 'https://www.moa.gov.tw/ws.php?id=24650',
    domain: 'moa.gov.tw',
  },
  {
    nameKey: 'resources.site.moa.fisheries',
    url: 'https://www.moa.gov.tw/ws.php?id=24651',
    domain: 'moa.gov.tw',
  },
  {
    nameKey: 'resources.site.trit',
    url: 'https://www.trit.gov.tw/',
    domain: 'trit.gov.tw',
  },
  {
    nameKey: 'resources.site.trit.crops',
    url: 'https://www.trit.gov.tw/ws.php?id=1142',
    domain: 'trit.gov.tw',
  },
  {
    nameKey: 'resources.site.trit.livestock',
    url: 'https://www.trit.gov.tw/ws.php?id=1143',
    domain: 'trit.gov.tw',
  },
  {
    nameKey: 'resources.site.trit.fisheries',
    url: 'https://www.trit.gov.tw/ws.php?id=1144',
    domain: 'trit.gov.tw',
  },
  {
    nameKey: 'resources.site.trit.forestry',
    url: 'https://www.trit.gov.tw/ws.php?id=1145',
    domain: 'trit.gov.tw',
  },
  {
    nameKey: 'resources.site.fa',
    url: 'https://www.fa.gov.tw/',
    domain: 'fa.gov.tw',
    featured: true,
    descKey: 'resources.featured.fa',
  },
  {
    nameKey: 'resources.site.swcb',
    url: 'https://www.swcb.gov.tw/',
    domain: 'swcb.gov.tw',
  },
  {
    nameKey: 'resources.site.afpa',
    url: 'https://www.afpa.gov.tw/',
    domain: 'afpa.gov.tw',
  },
  {
    nameKey: 'resources.site.nlsc',
    url: 'https://www.nlsc.gov.tw/',
    domain: 'nlsc.gov.tw',
  },
  {
    nameKey: 'resources.site.forestbureau',
    url: 'https://www.forest.gov.tw/',
    domain: 'forest.gov.tw',
  },
];

// Subcategory 1.2: 地方農業單位 (Local Agricultural Units) - Focused on Chiayi
export const agriGovernanceLocal: ResourceSite[] = [
  {
    nameKey: 'resources.site.cyhg',
    url: 'https://www.cyhg.gov.tw/',
    domain: 'cyhg.gov.tw',
    featured: true,
    descKey: 'resources.featured.cyhg',
  },
  {
    nameKey: 'resources.site.cyhg.agri',
    url: 'https://www.cyhg.gov.tw/cp.aspx?n=5566',
    domain: 'cyhg.gov.tw',
  },
  {
    nameKey: 'resources.site.chiayicity',
    url: 'https://www.chiayi.gov.tw/',
    domain: 'chiayi.gov.tw',
  },
  {
    nameKey: 'resources.site.chiayicity.agri',
    url: 'https://www.chiayi.gov.tw/cp.aspx?n=4932',
    domain: 'chiayi.gov.tw',
  },
  {
    nameKey: 'resources.site.ttsdcc',
    url: 'https://www.ttsdcc.org.tw/',
    domain: 'ttsdcc.org.tw',
  },
  {
    nameKey: 'resources.site.ttsdcc.chiayi',
    url: 'https://chiayi.ttsdcc.org.tw/',
    domain: 'ttsdcc.org.tw',
  },
  {
    nameKey: 'resources.site.tainan.agri',
    url: 'https://www.tainan.gov.tw/cp.aspx?n=4932',
    domain: 'tainan.gov.tw',
  },
  {
    nameKey: 'resources.site.yunlin.agri',
    url: 'https://www.yunlin.gov.tw/cp.aspx?n=4932',
    domain: 'yunlin.gov.tw',
  },
  {
    nameKey: 'resources.site.kaohsiung.agri',
    url: 'https://www.kcg.gov.tw/cp.aspx?n=4932',
    domain: 'kcg.gov.tw',
  },
  {
    nameKey: 'resources.site.pingtung.agri',
    url: 'https://www.pthg.gov.tw/cp.aspx?n=4932',
    domain: 'pthg.gov.tw',
  },
  {
    nameKey: 'resources.site.taichung.agri',
    url: 'https://www.taichung.gov.tw/cp.aspx?n=4932',
    domain: 'taichung.gov.tw',
  },
  {
    nameKey: 'resources.site.nantou.agri',
    url: 'https://www.nantou.gov.tw/cp.aspx?n=4932',
    domain: 'nantou.gov.tw',
  },
];

// Subcategory 1.3: 農業法規與政策 (Agricultural Regulations & Policies)
export const agriGovernancePolicy: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.law',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=law',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.lawdb.agri',
    url: 'https://law.moj.gov.tw/News/NewsList.aspx?pcode=M0020001',
    domain: 'law.moj.gov.tw',
  },
  {
    nameKey: 'resources.site.moj.agri',
    url: 'https://www.moj.gov.tw/',
    domain: 'moj.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.land',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=land',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.nladb',
    url: 'https://nladb.nla.gov.tw/',
    domain: 'nladb.nla.gov.tw',
  },
];

// ─── Chapter 2: 技術研發與推廣 (Technical R&D & Promotion) ───

// Subcategory 2.1: 農業試驗研究機構 (Agricultural Research Institutions)
export const agriTechResearch: ResourceSite[] = [
  {
    nameKey: 'resources.site.tais',
    url: 'https://www.tais.gov.tw/',
    domain: 'tais.gov.tw',
    featured: true,
    descKey: 'resources.featured.tais',
  },
  {
    nameKey: 'resources.site.tais.crops',
    url: 'https://www.tais.gov.tw/ws.php?id=1',
    domain: 'tais.gov.tw',
  },
  {
    nameKey: 'resources.site.tais.livestock',
    url: 'https://www.tais.gov.tw/ws.php?id=2',
    domain: 'tais.gov.tw',
  },
  {
    nameKey: 'resources.site.tais.fisheries',
    url: 'https://www.tais.gov.tw/ws.php?id=3',
    domain: 'tais.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec',
    url: 'https://www.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.tainan',
    url: 'https://tainan.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.chiayi',
    url: 'https://chiayi.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.taichung',
    url: 'https://taichung.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.afrec.kaohsiung',
    url: 'https://kaohsiung.afrec.gov.tw/',
    domain: 'afrec.gov.tw',
  },
  {
    nameKey: 'resources.site.tfri',
    url: 'https://www.tfri.gov.tw/',
    domain: 'tfri.gov.tw',
  },
  {
    nameKey: 'resources.site.fric',
    url: 'https://www.fric.gov.tw/',
    domain: 'fric.gov.tw',
  },
  {
    nameKey: 'resources.site.kktrdc',
    url: 'https://www.kktrdc.org.tw/',
    domain: 'kktrdc.org.tw',
  },
  {
    nameKey: 'resources.site.niaes',
    url: 'https://www.niaes.org.tw/',
    domain: 'niaes.org.tw',
  },
  {
    nameKey: 'resources.site.aspc',
    url: 'https://www.aspc.org.tw/',
    domain: 'aspc.org.tw',
  },
];

// Subcategory 2.2: 農業科技與創新 (Agricultural Technology & Innovation)
export const agriTechInnovation: ResourceSite[] = [
  {
    nameKey: 'resources.site.aait',
    url: 'https://www.aait.org.tw/',
    domain: 'aait.org.tw',
  },
  {
    nameKey: 'resources.site.isia',
    url: 'https://www.isia.org.tw/',
    domain: 'isia.org.tw',
  },
  {
    nameKey: 'resources.site.tesd',
    url: 'https://tesd.survey.sinica.edu.tw/',
    domain: 'tesd.survey.sinica.edu.tw',
  },
  {
    nameKey: 'resources.site.coa.smartagri',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=smartfarm',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.nstc',
    url: 'https://www.nstc.gov.tw/',
    domain: 'nstc.gov.tw',
  },
  {
    nameKey: 'resources.site.itri',
    url: 'https://www.itri.org.tw/',
    domain: 'itri.org.tw',
  },
  {
    nameKey: 'resources.site.nia',
    url: 'https://www.nia.org.tw/',
    domain: 'nia.org.tw',
  },
];

// Subcategory 2.3: 農業推廣與教育 (Agricultural Extension & Education)
export const agriTechExtension: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.extension',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=extension',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.ttsdcc.chiayi.ext',
    url: 'https://chiayi.ttsdcc.org.tw/education',
    domain: 'ttsdcc.org.tw',
  },
  {
    nameKey: 'resources.site.coa.nagu',
    url: 'https://www.nagu.org.tw/',
    domain: 'nagu.org.tw',
  },
  {
    nameKey: 'resources.site.tca',
    url: 'https://www.tca.org.tw/',
    domain: 'tca.org.tw',
  },
  {
    nameKey: 'resources.site.wda',
    url: 'https://www.wda.org.tw/',
    domain: 'wda.org.tw',
  },
  {
    nameKey: 'resources.site.tua',
    url: 'https://www.tua.org.tw/',
    domain: 'tua.org.tw',
  },
];

// ─── Chapter 3: 農產品行銷與銷售 (Agricultural Marketing & Sales) ───

// Subcategory 3.1: 線上銷售平台 (Online Sales Platforms)
export const agriMarketingOnline: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.market',
    url: 'https://www.coa.gov.tw/ws.php?id=2449',
    domain: 'coa.gov.tw',
    featured: true,
    descKey: 'resources.featured.coa.market',
  },
  {
    nameKey: 'resources.site.coa.trade',
    url: 'https://trade.coa.gov.tw/',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.shopee',
    url: 'https://shopee.tw/',
    domain: 'shopee.tw',
  },
  {
    nameKey: 'resources.site.shopee.farm',
    url: 'https://shopee.tw/cat.8010146',
    domain: 'shopee.tw',
  },
  {
    nameKey: 'resources.site.pchome',
    url: 'https://www.pchome.com.tw/',
    domain: 'pchome.com.tw',
  },
  {
    nameKey: 'resources.site.momo',
    url: 'https://www.momoshop.com.tw/',
    domain: 'momoshop.com.tw',
  },
  {
    nameKey: 'resources.site.momo.farm',
    url: 'https://www.momoshop.com.tw/category/DgrpGrp/7003010001.html',
    domain: 'momoshop.com.tw',
  },
  {
    nameKey: 'resources.site.77fresh',
    url: 'https://www.77fresh.com/',
    domain: '77fresh.com',
  },
  {
    nameKey: 'resources.site.gomaji',
    url: 'https://www.gomaji.com/',
    domain: 'gomaji.com',
  },
  {
    nameKey: 'resources.site.ezfresh',
    url: 'https://www.ezfresh.com.tw/',
    domain: 'ezfresh.com.tw',
  },
  {
    nameKey: 'resources.site.ibon',
    url: 'https://www.ibon.tw/',
    domain: 'ibon.tw',
  },
  {
    nameKey: 'resources.site.foodbank',
    url: 'https://food.tw.aeon.com/',
    domain: 'aeon.com',
  },
];

// Subcategory 3.2: 直銷與市集 (Direct Sales & Markets)
export const agriMarketingDirect: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.market.direct',
    url: 'https://www.coa.gov.tw/ws.php?id=2453',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.ttsdcc.market',
    url: 'https://www.ttsdcc.org.tw/web/Services.aspx?id=52',
    domain: 'ttsdcc.org.tw',
  },
  {
    nameKey: 'resources.site.coa.farmers.market',
    url: 'https://market.coa.gov.tw/',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.huashan.market',
    url: 'https://www.huashancreative.tw/',
    domain: 'huashancreative.tw',
  },
  {
    nameKey: 'resources.site.taipei.agri.market',
    url: 'https://www.ccw.org.tw/agriculture_market',
    domain: 'ccw.org.tw',
  },
  {
    nameKey: 'resources.site.coa.organic.market',
    url: 'https://www.coa.gov.tw/ws.php?id=2465',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.csf',
    url: 'https://www.csf.org.tw/',
    domain: 'csf.org.tw',
  },
];

// Subcategory 3.3: 認證與品牌建立 (Certification & Branding)
export const agriMarketingCertification: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.organic',
    url: 'https://www.coa.gov.tw/ws.php?id=2461',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.gis',
    url: 'https://www.coa.gov.tw/ws.php?id=2462',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.traceability',
    url: 'https://www.coa.gov.tw/ws.php?id=2466',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.fsq',
    url: 'https://www.coa.gov.tw/ws.php?id=2467',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.good.agricultural',
    url: 'https://www.coa.gov.tw/ws.php?id=2468',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.ttasia',
    url: 'https://www.ttasia.org.tw/',
    domain: 'ttasia.org.tw',
  },
  {
    nameKey: 'resources.site.tactcc',
    url: 'https://www.tactcc.org.tw/',
    domain: 'tactcc.org.tw',
  },
  {
    nameKey: 'resources.site.sgs',
    url: 'https://www.sgsgroup.com.tw/',
    domain: 'sgsgroup.com.tw',
  },
];

// ─── Chapter 4: 融資與補助資源 (Financing & Subsidy Resources) ───

// Subcategory 4.1: 農業融資管道 (Agricultural Financing Channels)
export const agriFinanceChannels: ResourceSite[] = [
  {
    nameKey: 'resources.site.acgf',
    url: 'https://www.acgf.org.tw/',
    domain: 'acgf.org.tw',
    featured: true,
    descKey: 'resources.featured.acgf',
  },
  {
    nameKey: 'resources.site.coa.finance',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=finance',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.boafroc',
    url: 'https://www.boafroc.org.tw/',
    domain: 'boafroc.org.tw',
  },
  {
    nameKey: 'resources.site.coa.farmland',
    url: 'https://www.coa.gov.tw/ws.php?id=2471',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.fsc',
    url: 'https://www.fsc.gov.tw/',
    domain: 'fsc.gov.tw',
  },
  {
    nameKey: 'resources.site.ttua',
    url: 'https://www.ttua.org.tw/',
    domain: 'ttua.org.tw',
  },
  {
    nameKey: 'resources.site.cyhga.bank',
    url: 'https://www.cyhg.org.tw/',
    domain: 'cyhg.org.tw',
  },
  {
    nameKey: 'resources.site.chiayi.bank',
    url: 'https://www.cyhbank.com.tw/',
    domain: 'cyhbank.com.tw',
  },
];

// Subcategory 4.2: 政府補助計畫 (Government Subsidy Programs)
export const agriFinanceSubsidy: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.subsidy',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=subsidy',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.subsidy.direct',
    url: 'https://subsidy.coa.gov.tw/',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.cyhg.subsidy',
    url: 'https://www.cyhg.gov.tw/cp.aspx?n=7889',
    domain: 'cyhg.gov.tw',
  },
  {
    nameKey: 'resources.site.chiayicity.subsidy',
    url: 'https://www.chiayi.gov.tw/cp.aspx?n=7889',
    domain: 'chiayi.gov.tw',
  },
  {
    nameKey: 'resources.site.ttsdcc.subsidy',
    url: 'https://www.ttsdcc.org.tw/Services.aspx?id=14',
    domain: 'ttsdcc.org.tw',
  },
  {
    nameKey: 'resources.site.smeportal',
    url: 'https://smeportal.moeaboe.gov.tw/',
    domain: 'moeaboe.gov.tw',
  },
  {
    nameKey: 'resources.site.moea.subsidy',
    url: 'https://www.moea.gov.tw/',
    domain: 'moea.gov.tw',
  },
];

// Subcategory 4.3: 農業保險 (Agricultural Insurance)
export const agriFinanceInsurance: ResourceSite[] = [
  {
    nameKey: 'resources.site.moa.insurance',
    url: 'https://www.moa.gov.tw/theme_list.php?theme=insurance',
    domain: 'moa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.insurance',
    url: 'https://www.coa.gov.tw/ws.php?id=2474',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.tai',
    url: 'https://www.taii.org.tw/',
    domain: 'taii.org.tw',
  },
  {
    nameKey: 'resources.site.tmn',
    url: 'https://www.tmn.com.tw/',
    domain: 'tmn.com.tw',
  },
  {
    nameKey: 'resources.site.chinalife',
    url: 'https://www.chinalife.com.tw/',
    domain: 'chinalife.com.tw',
  },
  {
    nameKey: 'resources.site.cathay',
    url: 'https://www.cathayins.com.tw/',
    domain: 'cathayins.com.tw',
  },
];

// ─── Chapter 5: 水資源與環境永續 (Water Resources & Environmental Sustainability) ───

// Subcategory 5.1: 水資源管理 (Water Resource Management)
export const agriSustainabilityWater: ResourceSite[] = [
  {
    nameKey: 'resources.site.swcb.water',
    url: 'https://www.swcb.gov.tw/',
    domain: 'swcb.gov.tw',
    featured: true,
    descKey: 'resources.featured.swcb.water',
  },
  {
    nameKey: 'resources.site.swcb.chiayi',
    url: 'https://chiayi.swcb.gov.tw/',
    domain: 'swcb.gov.tw',
  },
  {
    nameKey: 'resources.site.wra',
    url: 'https://www.wra.gov.tw/',
    domain: 'wra.gov.tw',
  },
  {
    nameKey: 'resources.site.wra.chiayi',
    url: 'https://chiayi.wra.gov.tw/',
    domain: 'wra.gov.tw',
  },
  {
    nameKey: 'resources.site.itri.water',
    url: 'https://www.itri.org.tw/chi/Services/Service01/Service0103.aspx',
    domain: 'itri.org.tw',
  },
  {
    nameKey: 'resources.site.coa.water',
    url: 'https://www.coa.gov.tw/ws.php?id=2476',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.moenv.water',
    url: 'https://www.moenv.gov.tw/Page/8081DE39812DD5A7/8e0ff38b-eade-4c0a-87c8-5fb1c2c0e84e',
    domain: 'moenv.gov.tw',
  },
];

// Subcategory 5.2: 友善農業與認證 (Sustainable Farming & Certification)
export const agriSustainabilityOrganic: ResourceSite[] = [
  {
    nameKey: 'resources.site.coa.organic',
    url: 'https://www.coa.gov.tw/ws.php?id=2461',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.ecofarm',
    url: 'https://www.coa.gov.tw/ws.php?id=2477',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.moenv.ecolabel',
    url: 'https://www.moenv.gov.tw/Page/BB32E3DE2F09B2FA/18f48f2c-c82a-439f-919e-8c8cd8a6cb62',
    domain: 'moenv.gov.tw',
  },
  {
    nameKey: 'resources.site.tactcc.organic',
    url: 'https://www.tactcc.org.tw/w/xmdoc/ct_id-18.html',
    domain: 'tactcc.org.tw',
  },
  {
    nameKey: 'resources.site.toaff',
    url: 'https://www.toaff.org.tw/',
    domain: 'toaff.org.tw',
  },
  {
    nameKey: 'resources.site.ttasn',
    url: 'https://www.ttasn.org.tw/',
    domain: 'ttasn.org.tw',
  },
];

// Subcategory 5.3: 氣候調適資源 (Climate Adaptation Resources)
export const agriSustainabilityClimate: ResourceSite[] = [
  {
    nameKey: 'resources.site.cwa',
    url: 'https://www.cwa.gov.tw/',
    domain: 'cwa.gov.tw',
  },
  {
    nameKey: 'resources.site.cwa.agri',
    url: 'https://www.cwa.gov.tw/V8/C/K/agriculture.html',
    domain: 'cwa.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.climate',
    url: 'https://www.coa.gov.tw/ws.php?id=2478',
    domain: 'coa.gov.tw',
  },
  {
    nameKey: 'resources.site.moenv.climate',
    url: 'https://www.moenv.gov.tw/Page/207AFCE84AAFF4FD',
    domain: 'moenv.gov.tw',
  },
  {
    nameKey: 'resources.site.nstc.climate',
    url: 'https://www.nstc.gov.tw/',
    domain: 'nstc.gov.tw',
  },
  {
    nameKey: 'resources.site.tais.pest',
    url: 'https://www.tais.gov.tw/ws.php?id=1151',
    domain: 'tais.gov.tw',
  },
  {
    nameKey: 'resources.site.coa.disaster',
    url: 'https://www.coa.gov.tw/theme_list.php?theme=disaster',
    domain: 'coa.gov.tw',
  },
];
