from .models import AnalysisSummary, BrandReport


class SuggestionGenerator:
    TEMPLATES = {
        "口味问题": "建议复核甜度、冰量和茶底比例，稳定不同门店的出品口感。",
        "价格问题": "建议增加小杯或套餐选择，并在菜单中突出性价比产品。",
        "出餐问题": "建议在高峰期提前备料，优化点单、制作和取餐流程。",
        "服务问题": "建议加强门店服务话术和高峰期沟通培训。",
        "包装问题": "建议检查杯盖密封性，并加强外卖订单二次封装。",
        "配送问题": "建议优化外卖出餐交接，减少送错和配送超时。",
        "产品问题": "建议检查小料新鲜度和添加标准，减少缺料、料少等情况。",
    }

    def enrich_summary(self, summary: AnalysisSummary) -> AnalysisSummary:
        for report in summary.brand_reports:
            report.suggestions = self.generate_for_brand(report)
        return summary

    def generate(self, problem_statistics: dict[str, int]) -> list[str]:
        top_categories = [category for category, _ in sorted(problem_statistics.items(), key=lambda item: item[1], reverse=True)[:3]]
        if not top_categories:
            return ["当前负面问题较少，建议继续保持产品稳定性和服务响应速度。"]
        return [self.TEMPLATES.get(category, "建议持续跟踪该类问题并复盘门店执行情况。") for category in top_categories]

    def generate_for_brand(self, brand_report: BrandReport) -> list[str]:
        if not brand_report.top_problems:
            return ["当前负面问题较少，建议继续保持产品稳定性和服务响应速度。"]
        return [self.TEMPLATES.get(category, "建议持续跟踪该类问题并复盘门店执行情况。") for category, _ in brand_report.top_problems]
