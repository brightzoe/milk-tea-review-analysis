import csv
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRANDS = ["蜜雪茶姬", "瑞巴克", "爷爷喜欢茶"]
PRODUCTS = ["珍珠奶茶", "柠檬茶", "奶盖茶", "杨枝甘露", "水果茶", "厚乳拿铁"]
CHANNELS = ["门店", "外卖"]

# 饮品/奶茶场景白名单：出现任一关键词即视为潜在可用评论
BEVERAGE_KEYWORDS = [
    # 奶茶及小料
    "奶茶", "奶盖", "珍珠", "波霸", "椰果", "布丁", "红豆", "燕麦", "仙草",
    "芋圆", "双皮奶", "烧仙草", "西米", "蒟蒻", "龟苓膏", "青稞", "爆珠",
    # 茶类/果茶
    "果茶", "水果茶", "柠檬茶", "乌龙茶", "红茶", "绿茶", "茉莉茶", "芝士茶",
    "奶霜", "奶绿", "抹茶", "四季春", "普洱茶", "铁观音", "花茶",
    # 咖啡
    "拿铁", "咖啡", "美式", "卡布奇诺", "摩卡", "星冰乐", "浓缩咖啡", "意式浓缩",
    # 通用饮品
    "饮品", "饮料", "奶茶三兄弟", "抹绿珍奶", "港式奶茶", "丝袜奶茶", "原味奶茶",
    "长岛奶茶", "香醇奶茶", "玉米牛奶", "红豆沙牛奶", "玫瑰汽泡水", "巴黎水",
    "苏打水", "汽泡水", "柠檬汁", "果汁", "百香", "芒果冰", "雪顶", "乐活冰",
    # 常见品牌（优先保留的真实品牌线索）
    "星巴克", "瑞幸", "喜茶", "奈雪", "一点点", "COCO", "古茗", "茶百道",
    "书亦", "沪上阿姨", "霸王茶姬", "茶颜悦色", "蜜雪冰城", "七分甜", "快乐柠檬",
    "KOI", "贡茶", "皇茶", "益禾堂", "CoCo", "coco",
    # 口感/场景词
    "甜度", "三分糖", "五分糖", "七分糖", "全糖", "无糖", "少冰", "去冰", "常温",
    "热饮", "冰量", "加冰", "标准糖", "半糖", "微糖",
]

# 非饮品/非奶茶场景黑名单：出现任一关键词即丢弃
NON_BEVERAGE_KEYWORDS = [
    # 正餐类型
    "烧烤", "烤肉", "火锅", "日料", "寿司", "拉面", "海鲜", "牛排", "披萨", "汉堡",
    "炸鸡", "烤鱼", "酸菜鱼", "自助餐", "泰国菜", "川菜", "湘菜", "粤菜", "西餐",
    "中餐", "意大利餐厅", "茶餐厅", "韩国料理", "日本料理", "烤鸭", "烤肉串",
    # 主食/菜品
    "粥", "粉", "面", "饭", "炒菜", "主食", "菜品", "鱼头", "肉蟹煲", "多嘴肉蟹煲",
    "蟹", "虾", "鱼", "牛肉", "猪肉", "羊肉", "鸡肉", "鸭肉", "鸡爪", "猪蹄", "排骨",
    "蛋糕", "面包", "甜品", "甜点", "冰淇淋", "雪糕", "巧克力蛋糕", "芝士蛋糕",
    "沙拉", "意面", "咖喱", "炒饭", "盖浇", "快餐", "小炒", "麻辣烫", "麻辣香锅",
    "麻辣拌", "铁板烧", "干锅", "烤鱼", "烤羊腿", "酥油茶", "油茶", "豆浆",
    # 其他餐饮场所词
    "饭店", "餐厅", "餐馆", "大酒店", "宾馆", "酒楼",
]


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", "", text.strip())
    text = text.replace("\ufeff", "")
    return text


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"[。！？!?\n\r]", text)
    return [part.strip("，,；; ") for part in parts if len(part.strip()) >= 8]


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(kw in text for kw in keywords)


def score_beverage_relevance(sentence: str) -> int:
    """根据饮品关键词命中数量打分，命中越多越相关。"""
    return sum(kw in sentence for kw in BEVERAGE_KEYWORDS)


def pick_beverage_snippet(text: str, max_len: int = 70) -> str | None:
    """
    从评论中筛选出属于奶茶/饮品消费场景的句子。
    只保留命中白名单且未命中黑名单的句子。
    """
    sentences = split_sentences(text)
    candidates = []
    for sentence in sentences:
        if not contains_any(sentence, BEVERAGE_KEYWORDS):
            continue
        if contains_any(sentence, NON_BEVERAGE_KEYWORDS):
            # 若同时命中黑名单，说明是混合场景（如餐厅里顺带喝了奶茶），为避免歧义丢弃
            continue
        if len(sentence) < 12:
            continue
        candidates.append(sentence)

    if not candidates:
        return None

    # 优先选饮品关键词命中多、长度适中的句子
    scored = sorted(
        candidates,
        key=lambda sentence: (
            -score_beverage_relevance(sentence),
            abs(len(sentence) - 40),
        ),
    )
    snippet = scored[0]
    if len(snippet) > max_len:
        snippet = snippet[:max_len].rstrip("，,；; ")
    return snippet


def label_from_star(star: str) -> str:
    value = float(star)
    if value >= 4:
        return "正面"
    if value <= 2:
        return "负面"
    return "中性"


def rating_from_label(label: str) -> int:
    return {"正面": 5, "中性": 3, "负面": 2}[label]


def load_asap_beverage_rows() -> list[dict[str, str]]:
    """从 ASAP sample 中严格筛选奶茶/饮品相关评论。"""
    rows: list[dict[str, str]] = []
    paths = [
        ROOT / "data" / "external" / "asap_train_sample.csv",
        ROOT / "data" / "external" / "asap_dev_sample.csv",
        ROOT / "data" / "external" / "asap_test_sample.csv",
    ]
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                text = normalize_text(row.get("reviewbody", ""))
                if len(text) < 20:
                    continue
                snippet = pick_beverage_snippet(text)
                if snippet is None:
                    continue
                label = label_from_star(row.get("star", "3"))
                rows.append(
                    {
                        "content": snippet,
                        "rating": str(rating_from_label(label)),
                        "label": label,
                    }
                )
    random.Random(7).shuffle(rows)
    return rows


def handcrafted_rows(target_count: int = 450) -> list[dict[str, str]]:
    """人工扩写的奶茶消费场景评论模板，覆盖多维度和多情感。"""
    positive = [
        "{brand}的{product}好喝，甜度合适，价格也实惠",
        "今天买的{product}很清爽，店员服务好，出餐速度也快",
        "{product}口感好，料足，包装好，没有洒",
        "这杯{product}茶味很香，喝起来新鲜，整体满意",
        "{brand}这次的{product}挺划算，排队也不久",
        "外卖送来的{product}包装好，冰量合适，味道喜欢",
        "门店店员服务好，{product}做得很快，口味稳定",
        "{product}清爽不腻，珍珠口感好，下次还会买",
        "三分糖刚好，{product}不齁，喝完也不腻",
        "奶盖很细腻，{product}整体搭配不错",
        "{product}的芝士奶盖咸香适中，茶底也很清新",
        "{brand}家的{product}一如既往的稳定，喝了三年没变",
        "今天点了杯{product}，小料给得很足，性价比超高",
        "{product}半糖刚刚好，茶香和奶香融合得很好",
        "外卖送到时{product}还是冰的，杯盖也没漏",
        "{brand}的{product}用料很实在，珍珠软糯有嚼劲",
        "这杯{product}果肉很多，喝起来很满足",
        "{product}包装颜值很高，拍照好看味道也不错",
        "{brand}门店环境干净，等餐时还有座位可以坐",
        "{product}甜度可以自选，对控糖的人很友好",
        "今天用了优惠券，{product}到手才几块钱，太值了",
        "{product}的茶味很浓，不是那种廉价的香精味",
        "{brand}的{product}配送很快，二十分钟就送到了",
        "这杯{product}冷热都好喝，冬天夏天都适合",
        "{product}奶盖和茶分层明显，颜值和口感都在线",
        "店员推荐的新品{product}没有踩雷，挺好喝的",
        "{brand}的{product}分量足，一杯能喝一下午",
        "{product}的椰果很Q弹，搭配奶茶刚刚好",
        "今天试了{brand}的{product}，口感顺滑不涩口",
        "{product}少冰刚刚好，不会因为冰块多而变淡",
        "{brand}服务很贴心，备注少糖真的按要求做了",
        "{product}的芋圆煮得很软糯，比别家好吃",
        "这杯{product}奶香浓郁，喝完嘴里还有回甘",
        "{brand}的{product}性价比在同类里算很高的",
        "外卖包装用了保温袋，{product}送到还是凉的",
        "{product}五分糖甜度正好，不会太甜也不会淡",
        "{brand}门店出餐很快，排队五分钟就拿到了",
        "{product}的布丁很嫩滑，和奶茶搭配很和谐",
        "今天买的{product}很解渴，夏天喝特别爽",
        "{brand}的{product}没有香精味，喝着很放心",
        "{product}加了一份珍珠，口感层次更丰富了",
        "店员态度很好，{product}做错了马上重做了一杯",
        "{brand}的{product}杯子设计很好看，很有辨识度",
        "{product}的果味很自然，不是糖浆兑出来的",
        "今天带朋友来喝{brand}的{product}，她也说好喝",
        "{product}热饮版本也很香，冬天暖胃刚好",
        "{brand}的{product}经常搞活动，学生党很友好",
        "这杯{product}入口丝滑，没有颗粒感",
        "{product}的奶油顶很绵密，配茶底不腻",
        "{brand}离公司很近，午休来一杯{product}很方便",
        "{product}的包装很严实，插管都不会洒",
        "今天点了{brand}的招牌{product}，确实好喝",
    ]

    neutral = [
        "{product}味道还可以，但是没有特别惊喜",
        "{brand}的{product}甜度正常，价格也一般",
        "这次{product}包装没问题，口味中规中矩",
        "{product}喝着还行，出餐速度一般",
        "今天的{product}有点甜，但还能接受",
        "{brand}门店人比较多，整体体验一般",
        "{product}料不算多，不过味道还可以",
        "外卖{product}送到时还行，没有明显问题",
        "不算难喝，但也没有想象中好喝",
        "价格有点贵，不过用券后还能接受",
        "{product}口感一般，就是普通奶茶水平",
        "{brand}的{product}中规中矩，不会回购也不踩雷",
        "这次{product}的冰有点多，不过味道还行",
        "{product}奶盖一般般，没有特别出彩",
        "{brand}的服务还行，{product}也没什么问题",
        "{product}的珍珠偏硬，但奶茶本身还可以",
        "今天喝的{product}茶味有点淡，凑合能喝",
        "{brand}的{product}价格和品质匹配，没什么亮点",
        "外卖{product}晚了十分钟，但还能接受",
        "{product}包装普通，味道也普通",
        "{brand}门店环境一般，{product}也就那样",
        "这杯{product}甜度适中，但少了点香气",
        "{product}料不算少，但也不算多",
        "{brand}的{product}喝起来不腻，但也没记忆点",
        "今天{product}等了一会，不过味道还可以",
        "{product}果味不够浓，像是加水了",
        "{brand}的{product}用了券价格还行，原价不值",
        "这杯{product}冷热适中，就是常规水平",
        "{product}的奶盖有点稀，不过整体能接受",
        "{brand}服务没有特别好，但也没差到哪里去",
        "{product}喝了不会惊艳，也不会讨厌",
        "今天{product}的分量一般，刚够喝",
        "{brand}的{product}包装换了，感觉不如以前",
        "{product}少糖还是有点甜，不过能忍",
        "外卖{product}的封口贴有点歪，但没漏",
        "{brand}的{product}新品试了一下，无功无过",
        "这杯{product}茶香不够突出，比较平庸",
        "{product}的小料种类不多，选择有限",
        "{brand}排队五分钟，{product}口感也就那样",
        "{product}喝完没有回味，普通饮品",
    ]

    negative = [
        "{product}太甜了，喝到后面有点腻",
        "{brand}的{product}价格贵，感觉不划算",
        "中午排队等很久，{product}出餐慢",
        "店员态度差，问甜度时很不耐烦",
        "外卖包装漏了，杯盖不紧，袋子湿了",
        "配送慢，送到时{product}已经不新鲜",
        "{product}珍珠硬，冰太多，料少",
        "这杯{product}太淡了，还有点苦，不好喝",
        "点的{product}送错了，处理也不及时",
        "{brand}最近涨价明显，性价比低",
        "三分糖还是偏甜，喝到最后有点齁",
        "奶盖太腻，杯盖也没压紧",
        "{product}喝完舌头很涩，像加了香精",
        "{brand}的{product}小料里有异物，很恶心",
        "外卖{product}洒了一半，商家还不处理",
        "{product}说好了少冰，结果半杯都是冰",
        "店员把{product}做错了，还说是我点的问题",
        "{brand}的{product}排队二十分钟，出品却一般",
        "这杯{product}奶盖分层严重，搅拌不开",
        "{product}的珍珠夹生，咬起来很硬",
        "{brand}客服态度冷淡，投诉也没用",
        "{product}果茶里的水果不新鲜，有异味",
        "配送员找不到地方，{product}送了一个小时",
        "{brand}的{product}杯盖没盖紧，漏了一袋子",
        "这杯{product}喝着有股怪味，像是变质了",
        "{product}价格涨了，但品质没跟上",
        "{brand}门店卫生一般，桌面上还有污渍",
        "{product}的甜度选项形同虚设，全糖太甜无糖没味",
        "外卖{product}没给吸管，联系商家也不回",
        "{brand}的{product}料越来越少，不会再买了",
        "这杯{product}冰化了之后淡得像水",
        "店员推荐{product}说招牌，结果很难喝",
        "{product}包装破损，杯子都瘪了",
        "{brand}的{product}喝了之后肚子不舒服",
        "{product}的奶盖有腥味，完全喝不下去",
        "等{product}等了四十分钟，前面没几个人",
        "{brand}优惠活动套路多，{product}实付不便宜",
        "这杯{product}闻着香，喝着苦，反差很大",
        "{product}的椰果发酸，明显不新鲜",
        "{brand}的{product}广告图和实物差距太大",
        "外卖{product}送到时冰块全化了，温温的",
        "{product}杯子漏底，还没喝就洒了",
        "店员对{product}的配方不熟悉，答非所问",
        "{brand}的{product}越来越水，没以前好喝",
        "这杯{product}甜得发苦，不知道放了什么",
        "{product}标注大杯，实际容量偏小",
        "{brand}的{product}二次加热后味道很怪",
        "外卖{product}送错了地址，重新送又等很久",
        "{product}的封口膜没封好，一碰就洒",
        "{brand}新品{product}纯纯智商税，不好喝",
        "这杯{product}喝到最后有沉淀物，不敢喝了",
        "{product}的小料硬邦邦的，像是隔夜泡的",
        "{brand}门店空调坏了，喝{product}出一身汗",
        "{product}说是鲜奶做的，喝着像奶粉冲的",
        "外卖{product}的包装袋破了，杯身全是灰",
        "{brand}的{product}优惠券不能用，体验很差",
        "这杯{product}茶味和奶味完全分离，很难喝",
        "{product}点了去冰还是给了很多冰",
        "{brand}的{product}服务员态度恶劣，不想再去",
        "{product}喝完嘴里发酸，品质有问题",
        "配送{product}超时半小时，商家也不赔偿",
        "{brand}的{product}价格虚高，味道普通",
        "这杯{product}底部有未溶解的粉末，很恶心",
        "{product}的杯套都烂了，拿在手上很脏",
        "{brand}的{product}改了配方，变得很难喝",
        "外卖{product}没加我单点的小料，钱白花了",
        "{product}喝着有塑料味，怀疑杯子质量差",
    ]

    # 按正面 40%、中性 25%、负面 35% 分配
    positive_count = int(target_count * 0.40)
    neutral_count = int(target_count * 0.25)
    negative_count = target_count - positive_count - neutral_count

    plan = [
        ("正面", positive, positive_count),
        ("中性", neutral, neutral_count),
        ("负面", negative, negative_count),
    ]
    rows: list[dict[str, str]] = []
    rng = random.Random(21)
    for label, templates, count in plan:
        for i in range(count):
            brand = BRANDS[(i + len(rows)) % len(BRANDS)]
            product = PRODUCTS[(i + len(label)) % len(PRODUCTS)]
            channel = CHANNELS[(i + len(rows)) % len(CHANNELS)]
            content = rng.choice(templates).format(brand=brand, product=product)
            rows.append(
                {
                    "brand": brand,
                    "product": product,
                    "channel": channel,
                    "content": content,
                    "rating": str(rating_from_label(label)),
                    "label": label,
                }
            )
    rng.shuffle(rows)
    return rows


def build_dataset(min_total: int = 500) -> list[list[str]]:
    rng = random.Random(42)
    asap = load_asap_beverage_rows()
    handcrafted_target = max(min_total - len(asap), 0)
    handcrafted = handcrafted_rows(handcrafted_target)
    rows: list[dict[str, str]] = []

    for i, row in enumerate(asap):
        row = dict(row)
        row["brand"] = BRANDS[i % len(BRANDS)]
        row["product"] = PRODUCTS[(i * 2) % len(PRODUCTS)]
        row["channel"] = "门店"
        rows.append(row)

    rows.extend(handcrafted)
    rng.shuffle(rows)

    output: list[list[str]] = []
    for index, row in enumerate(rows, start=1):
        output.append(
            [
                str(index),
                f"2026-06-{(index % 28) + 1:02d}",
                row["brand"],
                row["product"],
                row["channel"],
                row["content"],
                row["rating"],
                row["label"],
            ]
        )
    return output


def main() -> None:
    output_path = ROOT / "data" / "reviews.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_dataset()
    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["review_id", "date", "brand", "product", "channel", "content", "rating", "label"])
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
