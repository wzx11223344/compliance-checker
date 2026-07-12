#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业合规工具 - compliance-checker
提供10个合规相关工具：合同分析、法规检索、风险评估、合规清单、隐私审计、
敏感信息脱敏、法律术语解释、条款生成、义务追踪、报告生成。

无外部依赖，仅使用Python标准库。
"""

import re
import json
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# 1. 合同条款分析
# ---------------------------------------------------------------------------
def contract_analyzer(contract_text, check_items=None):
    """
    合同条款分析：检查合同文本中的关键条款和潜在风险。

    参数:
        contract_text (str): 合同全文文本。
        check_items (list[str]): 需要检查的条款类型列表，如
            ["付款条件", "违约责任", "保密条款", "终止条款"]，为None时使用默认项。

    返回:
        dict: 分析报告，包含发现的条款、风险点和建议。
    """
    if check_items is None:
        check_items = ["付款条件", "违约责任", "保密条款", "终止条款", "适用法律", "争议解决"]

    # 关键条款模式
    clause_patterns = {
        "付款条件": [r'付款\s*方式[:：]?(.+)', r'支付\s*期限[:：]?(.+)', r'金额[:：]?(.+?)元'],
        "违约责任": [r'违约.{0,20}责任.{0,200}', r'赔偿.{0,100}', r'罚款.{0,100}'],
        "保密条款": [r'保密.{0,200}', r'机密信息.{0,200}'],
        "终止条款": [r'终止.{0,200}', r'解除.{0,200}', r'到期.{0,100}'],
        "适用法律": [r'适用.{0,10}法律[:：]?(.+)', r'管辖.{0,10}法律[:：]?(.+)'],
        "争议解决": [r'争议.{0,10}解决.{0,200}', r'仲裁.{0,200}', r'诉讼.{0,200}']
    }

    # 风险关键词
    risk_keywords = ["自动续约", "无限期", "无限制", "单方面", "不可撤销", "无条件",
                     "全部责任", "无限赔偿", "放弃权利", "不得异议"]

    results = {
        "contract_length": len(contract_text),
        "check_items": [],
        "risk_points": [],
        "missing_items": [],
        "suggestions": []
    }

    for item in check_items:
        patterns = clause_patterns.get(item, [])
        found = False
        for pattern in patterns:
            matches = re.findall(pattern, contract_text, re.IGNORECASE)
            if matches:
                results["check_items"].append({
                    "item": item,
                    "status": "已找到",
                    "content_preview": matches[0][:100] if matches else ""
                })
                found = True
                break
        if not found:
            results["missing_items"].append(item)
            results["check_items"].append({
                "item": item,
                "status": "未找到",
                "content_preview": ""
            })

    # 检查风险关键词
    for keyword in risk_keywords:
        if keyword in contract_text:
            results["risk_points"].append({
                "keyword": keyword,
                "severity": "高" if keyword in ["无限期", "不可撤销", "全部责任", "无限赔偿"] else "中",
                "suggestion": f"注意合同中包含「{keyword}」相关表述，建议仔细审查相关条款。"
            })

    # 生成建议
    if results["missing_items"]:
        results["suggestions"].append(f"合同缺少以下重要条款：{', '.join(results['missing_items'])}，建议补充。")
    if results["risk_points"]:
        results["suggestions"].append(f"发现{len(results['risk_points'])}个风险点，建议法律顾问审查。")
    if not results["risk_points"] and not results["missing_items"]:
        results["suggestions"].append("合同条款基本完备，无明显风险关键词。")

    results["risk_count"] = len(results["risk_points"])
    results["overall_status"] = "高风险" if results["risk_count"] > 3 else ("中风险" if results["risk_count"] > 0 else "低风险")

    return results


# ---------------------------------------------------------------------------
# 2. 法规检索
# ---------------------------------------------------------------------------
def regulation_searcher(keyword, industry="通用", jurisdiction="中国"):
    """
    法规检索：根据关键词、行业和司法管辖区检索相关法规。

    参数:
        keyword (str): 检索关键词。
        industry (str): 行业领域，默认"通用"。
        jurisdiction (str): 司法管辖区，默认"中国"。

    返回:
        dict: 检索结果，含匹配法规列表。
    """
    # 法规知识库（示例数据）
    regulation_db = {
        "中国": {
            "通用": [
                {"name": "中华人民共和国民法典", "code": "民法典", "effective_date": "2021-01-01",
                 "keywords": ["合同", "侵权", "物权", "人格权", "婚姻", "继承"]},
                {"name": "中华人民共和国公司法", "code": "公司法", "effective_date": "2024-07-01",
                 "keywords": ["公司", "股东", "董事", "监事", "注册资本"]},
                {"name": "中华人民共和国劳动法", "code": "劳动法", "effective_date": "1995-01-01",
                 "keywords": ["劳动", "工资", "社保", "工伤", "辞退"]}
            ],
            "金融": [
                {"name": "中华人民共和国商业银行法", "code": "商业银行法", "effective_date": "2015-10-01",
                 "keywords": ["银行", "存款", "贷款", "金融"]},
                {"name": "中华人民共和国证券法", "code": "证券法", "effective_date": "2020-03-01",
                 "keywords": ["证券", "股票", "债券", "上市", "信息披露"]}
            ],
            "互联网": [
                {"name": "中华人民共和国网络安全法", "code": "网络安全法", "effective_date": "2017-06-01",
                 "keywords": ["网络安全", "数据", "个人信息", "网络运营"]},
                {"name": "中华人民共和国数据安全法", "code": "数据安全法", "effective_date": "2021-09-01",
                 "keywords": ["数据", "数据安全", "数据处理", "数据分类"]}
            ],
            "医疗": [
                {"name": "中华人民共和国基本医疗卫生与健康促进法", "code": "医疗卫生法", "effective_date": "2020-06-01",
                 "keywords": ["医疗", "卫生", "健康", "药品"]},
                {"name": "中华人民共和国药品管理法", "code": "药品管理法", "effective_date": "2019-12-01",
                 "keywords": ["药品", "药品管理", "药品注册", "药品生产"]}
            ]
        },
        "美国": {
            "通用": [
                {"name": "Uniform Commercial Code (UCC)", "code": "UCC", "effective_date": "1952-01-01",
                 "keywords": ["commercial", "contract", "sale", "negotiable"]}
            ]
        }
    }

    jurisdiction_laws = regulation_db.get(jurisdiction, {})
    industry_laws = jurisdiction_laws.get(industry, jurisdiction_laws.get("通用", []))

    matched = []
    for law in industry_laws:
        relevance = 0
        if keyword in law["name"]:
            relevance += 50
        for kw in law.get("keywords", []):
            if keyword in kw or kw in keyword:
                relevance += 20
        if relevance > 0:
            matched.append({
                **law,
                "relevance_score": relevance,
                "match_type": "名称匹配" if keyword in law["name"] else "关键词匹配"
            })

    matched.sort(key=lambda x: x["relevance_score"], reverse=True)

    return {
        "keyword": keyword,
        "industry": industry,
        "jurisdiction": jurisdiction,
        "total_found": len(matched),
        "results": matched,
        "suggestion": "建议查阅完整法规文本以确认具体条款。" if matched else "未找到匹配法规，请调整关键词。"
    }


# ---------------------------------------------------------------------------
# 3. 风险评估
# ---------------------------------------------------------------------------
def risk_assessor(business_info, risk_factors):
    """
    风险评估：根据业务信息和风险因素评估整体风险等级。

    参数:
        business_info (dict): 业务信息，含 company_name、industry、size、region 等。
        risk_factors (list[dict]): 风险因素列表，每项含 factor、likelihood(1-5)、impact(1-5)。

    返回:
        dict: 风险评估报告，含总体风险等级和各风险详情。
    """
    risk_levels = {1: "极低", 2: "低", 3: "中", 4: "高", 5: "极高"}
    assessed_risks = []

    total_score = 0
    for rf in risk_factors:
        likelihood = rf.get("likelihood", 3)
        impact = rf.get("impact", 3)
        score = likelihood * impact  # 1-25
        total_score += score

        level = "低" if score <= 5 else ("中" if score <= 12 else ("高" if score <= 20 else "极高"))

        assessed_risks.append({
            "factor": rf.get("factor", "未知风险"),
            "likelihood": likelihood,
            "likelihood_label": risk_levels.get(likelihood, "中"),
            "impact": impact,
            "impact_label": risk_levels.get(impact, "中"),
            "risk_score": score,
            "risk_level": level,
            "recommendation": _get_risk_recommendation(level, rf.get("factor", ""))
        })

    avg_score = total_score / len(risk_factors) if risk_factors else 0
    overall_level = "低" if avg_score <= 5 else ("中" if avg_score <= 12 else ("高" if avg_score <= 20 else "极高"))

    return {
        "company": business_info.get("company_name", "未知企业"),
        "industry": business_info.get("industry", "未知"),
        "total_risks": len(risk_factors),
        "overall_risk_score": round(avg_score, 1),
        "overall_risk_level": overall_level,
        "risk_breakdown": {
            "低": len([r for r in assessed_risks if r["risk_level"] == "低"]),
            "中": len([r for r in assessed_risks if r["risk_level"] == "中"]),
            "高": len([r for r in assessed_risks if r["risk_level"] == "高"]),
            "极高": len([r for r in assessed_risks if r["risk_level"] == "极高"])
        },
        "assessed_risks": sorted(assessed_risks, key=lambda x: x["risk_score"], reverse=True),
        "priority_actions": [r["recommendation"] for r in assessed_risks if r["risk_level"] in ("高", "极高")]
    }


def _get_risk_recommendation(level, factor):
    """根据风险等级和因素生成建议。"""
    recommendations = {
        "低": f"「{factor}」风险较低，建议常规监控。",
        "中": f"「{factor}」风险中等，建议制定缓解措施并定期评估。",
        "高": f"「{factor}」风险较高，建议立即采取控制措施并加强监控。",
        "极高": f"「{factor}」风险极高，建议优先处理并制定应急预案。"
    }
    return recommendations.get(level, "建议进一步评估。")


# ---------------------------------------------------------------------------
# 4. 合规检查清单
# ---------------------------------------------------------------------------
def compliance_checklist(industry, checklist_type="general"):
    """
    合规检查清单：根据行业和清单类型生成合规检查项。

    参数:
        industry (str): 行业类型，如 "金融"、"互联网"、"医疗"、"制造"。
        checklist_type (str): 清单类型，如 "general"（通用）、"data_privacy"（数据隐私）、
            "financial"（财务合规），默认 "general"。

    返回:
        dict: 合规检查清单，含检查项列表。
    """
    checklist_db = {
        "金融": {
            "general": [
                "持有有效的金融业务许可证",
                "建立了反洗钱(AML)内部控制制度",
                "客户身份识别(KYC)程序完整",
                "定期进行合规审计",
                "设立合规管理部门",
                "员工合规培训完成率达标",
                "大额交易报告机制健全",
                "风险管理制度已落实"
            ],
            "financial": [
                "财务报表按期编制并审计",
                "资本充足率符合监管要求",
                "关联交易披露完整",
                "内控报告已提交",
                "呆账准备金计提合规",
                "信息披露符合要求"
            ],
            "data_privacy": [
                "客户数据分类分级制度建立",
                "数据加密传输和存储",
                "数据访问权限控制到位",
                "客户隐私政策已公示",
                "数据泄露应急预案就绪",
                "数据保留期限符合规定"
            ]
        },
        "互联网": {
            "general": [
                "ICP备案完成",
                "网络安全等级保护测评通过",
                "用户协议和隐私政策已公示",
                "内容审核机制建立",
                "未成年人保护措施到位",
                "数据安全管理制度建立"
            ],
            "data_privacy": [
                "个人信息收集最小化原则落实",
                "用户同意机制完善",
                "个人信息影响评估已完成",
                "数据出境安全评估完成",
                "个人信息保护负责人已指定",
                "数据主体权利保障机制建立"
            ]
        },
        "医疗": {
            "general": [
                "医疗机构执业许可证有效",
                "医护人员资质证书齐全",
                "药品采购渠道合规",
                "医疗废物处理符合规范",
                "病历管理制度健全",
                "医疗质量控制体系建立"
            ],
            "data_privacy": [
                "患者隐私保护制度建立",
                "病历数据加密存储",
                "医疗数据访问权限控制",
                "患者知情同意书签署",
                "医疗数据共享合规审查",
                "健康数据跨境传输评估"
            ]
        }
    }

    industry_checklists = checklist_db.get(industry, {})
    items = industry_checklists.get(checklist_type, industry_checklists.get("general", [
        "营业执照有效",
        "税务登记完成",
        "社保缴纳合规",
        "劳动用工合规",
        "安全生产制度建立",
        "环境保护措施到位"
    ]))

    checklist = []
    for i, item in enumerate(items):
        checklist.append({
            "id": i + 1,
            "item": item,
            "status": "待检查",
            "priority": "高" if i < len(items) // 3 else ("中" if i < len(items) * 2 // 3 else "低"),
            "category": checklist_type
        })

    return {
        "industry": industry,
        "checklist_type": checklist_type,
        "total_items": len(checklist),
        "items": checklist,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ---------------------------------------------------------------------------
# 5. 数据隐私审计
# ---------------------------------------------------------------------------
def data_privacy_auditor(data_flow, processing_activities):
    """
    数据隐私审计：审计数据流向和处理活动的合规性。

    参数:
        data_flow (list[dict]): 数据流列表，每项含 source、destination、data_type、purpose。
        processing_activities (list[dict]): 处理活动列表，每项含 activity、legal_basis、
            data_category、retention_period。

    返回:
        dict: 审计报告，含合规状态和问题清单。
    """
    valid_legal_bases = ["同意", "合同履行", "法定义务", "合法权益", "公共利益", "重大利益"]

    audit_result = {
        "total_data_flows": len(data_flow),
        "total_activities": len(processing_activities),
        "compliant_flows": 0,
        "non_compliant_flows": 0,
        "compliant_activities": 0,
        "non_compliant_activities": 0,
        "issues": [],
        "recommendations": [],
        "data_flow_audit": [],
        "activity_audit": []
    }

    # 审计数据流
    for i, flow in enumerate(data_flow):
        issues = []
        if not flow.get("purpose"):
            issues.append("缺少数据处理目的说明")
        if not flow.get("data_type"):
            issues.append("未标明数据类型")
        if flow.get("destination") and "境外" in str(flow.get("destination", "")):
            issues.append("数据涉及跨境传输，需进行安全评估")

        status = "合规" if not issues else "不合规"
        if status == "合规":
            audit_result["compliant_flows"] += 1
        else:
            audit_result["non_compliant_flows"] += 1

        audit_result["data_flow_audit"].append({
            "flow_id": i + 1,
            "source": flow.get("source", "未知"),
            "destination": flow.get("destination", "未知"),
            "data_type": flow.get("data_type", "未标明"),
            "purpose": flow.get("purpose", "未说明"),
            "status": status,
            "issues": issues
        })
        audit_result["issues"].extend([f"数据流{i + 1}: {iss}" for iss in issues])

    # 审计处理活动
    for i, activity in enumerate(processing_activities):
        issues = []
        legal_basis = activity.get("legal_basis", "")
        if legal_basis not in valid_legal_bases:
            issues.append(f"法律依据「{legal_basis}」不在有效范围内")
        if not activity.get("retention_period"):
            issues.append("未设定数据保留期限")

        status = "合规" if not issues else "不合规"
        if status == "合规":
            audit_result["compliant_activities"] += 1
        else:
            audit_result["non_compliant_activities"] += 1

        audit_result["activity_audit"].append({
            "activity_id": i + 1,
            "activity": activity.get("activity", "未知"),
            "legal_basis": legal_basis,
            "data_category": activity.get("data_category", "未标明"),
            "retention_period": activity.get("retention_period", "未设定"),
            "status": status,
            "issues": issues
        })
        audit_result["issues"].extend([f"处理活动{i + 1}: {iss}" for iss in issues])

    # 生成建议
    if audit_result["non_compliant_flows"] > 0:
        audit_result["recommendations"].append("存在不合规数据流，建议补充目的说明和数据类型标注。")
    if audit_result["non_compliant_activities"] > 0:
        audit_result["recommendations"].append("部分处理活动法律依据不明确，建议补充合法依据。")
    if not audit_result["issues"]:
        audit_result["recommendations"].append("数据隐私合规状态良好，建议保持定期审计。")

    audit_result["overall_compliance"] = "合格" if audit_result["non_compliant_flows"] == 0 and audit_result["non_compliant_activities"] == 0 else "不合格"

    return audit_result


# ---------------------------------------------------------------------------
# 6. 敏感信息脱敏
# ---------------------------------------------------------------------------
def document_redactor(text, sensitive_patterns=None):
    """
    敏感信息脱敏：识别并脱敏文本中的敏感信息。

    参数:
        text (str): 原始文本。
        sensitive_patterns (dict): 自定义敏感模式，键为类型，值为正则表达式。
            为None时使用默认模式。

    返回:
        dict: 脱敏结果，含脱敏后文本和替换统计。
    """
    if sensitive_patterns is None:
        sensitive_patterns = {
            "身份证号": r'\d{17}[\dXx]',
            "手机号": r'1[3-9]\d{9}',
            "银行卡号": r'\d{16,19}',
            "邮箱": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "IP地址": r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
            "微信号": r'[Ww]echat[:：]?\s*\w+'
        }

    redacted_text = text
    stats = {}

    for pattern_name, pattern in sensitive_patterns.items():
        matches = re.findall(pattern, redacted_text)
        count = len(matches)
        if count > 0:
            redacted_text = re.sub(pattern, f'【{pattern_name}已脱敏】', redacted_text)
            stats[pattern_name] = {
                "count": count,
                "examples": matches[:3]  # 保留前3个示例
            }

    return {
        "original_length": len(text),
        "redacted_length": len(redacted_text),
        "redacted_text": redacted_text,
        "redaction_stats": stats,
        "total_redactions": sum(s["count"] for s in stats.values()),
        "patterns_used": list(sensitive_patterns.keys())
    }


# ---------------------------------------------------------------------------
# 7. 法律术语解释
# ---------------------------------------------------------------------------
def legal_term_explainer(term, context=""):
    """
    法律术语解释：解释法律术语的含义。

    参数:
        term (str): 需要解释的法律术语。
        context (str): 术语出现的上下文，帮助精确解释，默认空。

    返回:
        dict: 术语解释，含定义、相关概念和注意事项。
    """
    term_db = {
        "违约责任": {
            "definition": "当事人一方不履行合同义务或者履行合同义务不符合约定时，应当承担的民事责任。",
            "legal_basis": "《民法典》第五百七十七条",
            "types": ["继续履行", "采取补救措施", "赔偿损失", "支付违约金", "解除合同"],
            "notes": "违约责任的承担不以过错为前提，但不可抗力可部分或全部免责。"
        },
        "不可抗力": {
            "definition": "不能预见、不能避免且不能克服的客观情况，如自然灾害、战争等。",
            "legal_basis": "《民法典》第一百八十条",
            "types": ["自然灾害", "社会异常事件", "政府行为"],
            "notes": "发生不可抗力时，应及时通知对方并采取措施减损，否则不能全部免责。"
        },
        "缔约过失责任": {
            "definition": "在合同订立过程中，一方因违背诚信原则导致对方损失时应承担的赔偿责任。",
            "legal_basis": "《民法典》第五百条",
            "types": ["假借订立合同恶意磋商", "故意隐瞒重要事实", "提供虚假情况"],
            "notes": "缔约过失责任发生在合同成立之前，区别于违约责任。"
        },
        "诉讼时效": {
            "definition": "权利人请求人民法院保护其民事权利的法定期间。",
            "legal_basis": "《民法典》第一百八十八条",
            "types": ["一般诉讼时效（3年）", "短期诉讼时效", "最长诉讼时效（20年）"],
            "notes": "诉讼时效届满后，实体权利不消灭，但义务人可提出抗辩拒绝履行。"
        },
        "连带责任": {
            "definition": "两个或两个以上的债务人对同一债务负有全部清偿责任的制度。",
            "legal_basis": "《民法典》第五百一十八条",
            "types": ["法定连带责任", "约定连带责任"],
            "notes": "债权人可向任一连带债务人请求全部给付，债务人内部可追偿。"
        },
        "知识产权": {
            "definition": "权利人对其智力成果和经营活动中的标记、信誉依法享有的专有权利。",
            "legal_basis": "《民法典》第一百二十三条",
            "types": ["著作权", "专利权", "商标权", "商业秘密", "集成电路布图设计"],
            "notes": "知识产权具有地域性、时间性和专有性特征。"
        },
        "个人信息": {
            "definition": "以电子或者其他方式记录的与已识别或者可识别的自然人有关的各种信息。",
            "legal_basis": "《个人信息保护法》第四条",
            "types": ["一般个人信息", "敏感个人信息"],
            "notes": "处理个人信息应遵循合法、正当、必要和诚信原则，取得个人同意。"
        }
    }

    # 查找术语
    explanation = term_db.get(term)
    if not explanation:
        # 模糊匹配
        for key in term_db:
            if term in key or key in term:
                explanation = term_db[key]
                explanation["matched_term"] = key
                break

    if not explanation:
        return {
            "term": term,
            "found": False,
            "message": f"未在数据库中找到「{term}」的解释，建议查阅法律条文或咨询专业律师。"
        }

    explanation["term"] = term
    explanation["context"] = context
    explanation["found"] = True

    if context:
        explanation["context_note"] = f"结合上下文「{context[:50]}」，该术语在此场景中应注意其具体适用条件。"

    return explanation


# ---------------------------------------------------------------------------
# 8. 条款生成器
# ---------------------------------------------------------------------------
def clause_generator(contract_type, clause_type, parameters=None):
    """
    条款生成器：根据合同类型和条款类型生成标准条款文本。

    参数:
        contract_type (str): 合同类型，如 "买卖合同"、"租赁合同"、"服务合同"。
        clause_type (str): 条款类型，如 "保密条款"、"违约条款"、"争议解决"。
        parameters (dict): 条款参数，如 {party_a: "甲方", party_b: "乙方", amount: "10000"}。

    返回:
        dict: 生成的条款文本和说明。
    """
    if parameters is None:
        parameters = {"party_a": "甲方", "party_b": "乙方"}

    clause_templates = {
        "保密条款": {
            "content": """第X条 保密条款

{party_a}与{party_b}（以下简称"双方"）在履行本合同过程中知悉的对方商业秘密、技术秘密及其他保密信息，未经对方书面同意，不得向任何第三方披露、使用或允许他人使用。

保密义务在本合同终止后【{retention_years}】年内继续有效。违反本条约定的一方应赔偿对方因此遭受的全部损失，并支付违约金人民币{penalty_amount}元。""",
            "variables": ["party_a", "party_b", "retention_years", "penalty_amount"]
        },
        "违约条款": {
            "content": """第X条 违约责任

任何一方违反本合同约定的，应承担违约责任。违约方应向守约方支付违约金人民币{penalty_amount}元，并赔偿守约方因此遭受的直接损失。

如违约金不足以弥补守约方损失的，违约方应补足差额。守约方有权选择要求违约方继续履行合同或解除合同。""",
            "variables": ["penalty_amount"]
        },
        "争议解决": {
            "content": """第X条 争议解决

因本合同引起的或与本合同有关的任何争议，双方应首先通过友好协商解决；协商不成的，任何一方均有权向{court_jurisdiction}人民法院提起诉讼。

在争议解决期间，对争议部分以外的合同条款，双方仍应继续履行。""",
            "variables": ["court_jurisdiction"]
        },
        "不可抗力": {
            "content": """第X条 不可抗力

因不可抗力导致一方不能履行或不能完全履行本合同义务的，应根据不可抗力的影响程度，部分或全部免除责任。

遭遇不可抗力的一方应在事件发生后【{notice_days}】日内书面通知对方，并提供相关证明文件。双方应协商采取补救措施，减少不可抗力造成的损失。""",
            "variables": ["notice_days"]
        },
        "终止条款": {
            "content": """第X条 合同终止

出现下列情形之一的，本合同终止：
（一）双方协商一致解除；
（二）一方严重违约，经催告后仍未改正的，守约方有权解除；
（三）因不可抗力致使合同目的不能实现；
（四）法律法规规定的其他情形。

合同终止后，双方应按约定进行结算和交接。""",
            "variables": []
        }
    }

    template = clause_templates.get(clause_type)
    if not template:
        return {
            "contract_type": contract_type,
            "clause_type": clause_type,
            "found": False,
            "available_types": list(clause_templates.keys()),
            "message": f"未找到「{clause_type}」的模板，请使用可用类型之一。"
        }

    # 填充参数
    defaults = {
        "retention_years": "3",
        "penalty_amount": "10000",
        "court_jurisdiction": "合同签订地",
        "notice_days": "15",
        "party_a": "甲方",
        "party_b": "乙方"
    }
    # 合并参数和默认值
    full_params = {**defaults, **parameters}

    content = template["content"]
    for var in template["variables"]:
        placeholder = "{" + var + "}"
        content = content.replace(placeholder, str(full_params.get(var, defaults.get(var, ""))))

    return {
        "contract_type": contract_type,
        "clause_type": clause_type,
        "found": True,
        "clause_content": content,
        "variables_used": template["variables"],
        "parameters_applied": {v: full_params.get(v) for v in template["variables"]},
        "note": f"生成的条款适用于{contract_type}，请根据实际情况调整具体参数。"
    }


# ---------------------------------------------------------------------------
# 9. 义务追踪器
# ---------------------------------------------------------------------------
def obligation_tracker(obligations, deadlines):
    """
    义务追踪器：追踪合同或法规义务的履行状态和截止日期。

    参数:
        obligations (list[dict]): 义务列表，每项含 id、description、responsible_party、status。
        deadlines (dict): 截止日期映射，键为义务id，值为日期字符串 "YYYY-MM-DD"。

    返回:
        dict: 义务追踪报告，含状态统计和即将到期项。
    """
    today = datetime.now()
    tracked = []
    overdue = []
    upcoming = []
    completed = []

    for obligation in obligations:
        obl_id = obligation.get("id")
        description = obligation.get("description", "")
        responsible = obligation.get("responsible_party", "未指定")
        status = obligation.get("status", "pending")

        deadline_str = deadlines.get(obl_id, "")
        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            days_remaining = (deadline - today).days
        else:
            deadline = None
            days_remaining = None

        item = {
            "id": obl_id,
            "description": description,
            "responsible_party": responsible,
            "status": status,
            "deadline": deadline_str,
            "days_remaining": days_remaining,
            "priority": "紧急" if (days_remaining is not None and days_remaining <= 7 and status != "completed") else "常规"
        }

        if status == "completed":
            item["urgency"] = "已完成"
            completed.append(item)
        elif days_remaining is not None:
            if days_remaining < 0:
                item["urgency"] = "已逾期"
                overdue.append(item)
            elif days_remaining <= 7:
                item["urgency"] = "即将到期"
                upcoming.append(item)
            else:
                item["urgency"] = "正常"
        else:
            item["urgency"] = "未设定期限"

        tracked.append(item)

    return {
        "total_obligations": len(obligations),
        "status_summary": {
            "completed": len(completed),
            "overdue": len(overdue),
            "upcoming": len(upcoming),
            "pending": len(obligations) - len(completed) - len(overdue) - len(upcoming)
        },
        "overdue_items": overdue,
        "upcoming_items": upcoming,
        "completed_items": completed,
        "all_tracked": sorted(tracked, key=lambda x: (x.get("days_remaining") or 9999)),
        "generated_at": today.strftime("%Y-%m-%d %H:%M"),
        "action_required": len(overdue) > 0 or len(upcoming) > 0
    }


# ---------------------------------------------------------------------------
# 10. 合规报告生成
# ---------------------------------------------------------------------------
def compliance_report_generator(audit_data, output_format="text"):
    """
    合规报告生成：将审计数据整理为结构化报告。

    参数:
        audit_data (dict): 审计数据，含 report_title、auditor、date、findings、
            recommendations、overall_status 等。
        output_format (str): 输出格式，可选 "text"（纯文本）、"json"（JSON格式）、
            "markdown"（Markdown格式），默认 "text"。

    返回:
        str: 格式化的合规报告。
    """
    report_title = audit_data.get("report_title", "合规审计报告")
    auditor = audit_data.get("auditor", "未知")
    audit_date = audit_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    findings = audit_data.get("findings", [])
    recommendations = audit_data.get("recommendations", [])
    overall_status = audit_data.get("overall_status", "待评估")
    scope = audit_data.get("scope", "全量审计")

    # 统计发现项
    critical = [f for f in findings if f.get("severity") == "critical"]
    high = [f for f in findings if f.get("severity") == "high"]
    medium = [f for f in findings if f.get("severity") == "medium"]
    low = [f for f in findings if f.get("severity") == "low"]

    stats = {
        "total_findings": len(findings),
        "critical": len(critical),
        "high": len(high),
        "medium": len(medium),
        "low": len(low),
        "recommendations_count": len(recommendations)
    }

    if output_format == "json":
        report = {
            "report_title": report_title,
            "auditor": auditor,
            "audit_date": audit_date,
            "scope": scope,
            "overall_status": overall_status,
            "statistics": stats,
            "findings": findings,
            "recommendations": recommendations
        }
        return json.dumps(report, ensure_ascii=False, indent=2)

    elif output_format == "markdown":
        lines = [
            f"# {report_title}",
            "",
            f"**审计人员**: {auditor}  ",
            f"**审计日期**: {audit_date}  ",
            f"**审计范围**: {scope}  ",
            f"**总体状态**: {overall_status}",
            "",
            "## 统计概要",
            "",
            f"| 严重程度 | 数量 |",
            f"|----------|------|",
            f"| 严重 | {stats['critical']} |",
            f"| 高 | {stats['high']} |",
            f"| 中 | {stats['medium']} |",
            f"| 低 | {stats['low']} |",
            f"| **合计** | **{stats['total_findings']}** |",
            ""
        ]

        if findings:
            lines.append("## 审计发现")
            lines.append("")
            for i, f in enumerate(findings, 1):
                lines.append(f"### 发现 {i}")
                lines.append(f"- **描述**: {f.get('description', '')}")
                lines.append(f"- **严重程度**: {f.get('severity', '未知')}")
                lines.append(f"- **状态**: {f.get('status', '未处理')}")
                if f.get('recommendation'):
                    lines.append(f"- **建议**: {f.get('recommendation')}")
                lines.append("")

        if recommendations:
            lines.append("## 改进建议")
            lines.append("")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")

        lines.append("---")
        lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    else:  # text format
        lines = [
            "=" * 60,
            f"  {report_title}",
            "=" * 60,
            "",
            f"  审计人员: {auditor}",
            f"  审计日期: {audit_date}",
            f"  审计范围: {scope}",
            f"  总体状态: {overall_status}",
            "",
            "-" * 60,
            "  统计概要",
            "-" * 60,
            f"  严重问题: {stats['critical']}",
            f"  高级问题: {stats['high']}",
            f"  中级问题: {stats['medium']}",
            f"  低级问题: {stats['low']}",
            f"  问题总数: {stats['total_findings']}",
            f"  建议数量: {stats['recommendations_count']}",
            "",
        ]

        if findings:
            lines.append("-" * 60)
            lines.append("  审计发现")
            lines.append("-" * 60)
            for i, f in enumerate(findings, 1):
                lines.append(f"  [{i}] {f.get('description', '')}")
                lines.append(f"      严重程度: {f.get('severity', '未知')}")
                lines.append(f"      状态: {f.get('status', '未处理')}")
                if f.get('recommendation'):
                    lines.append(f"      建议: {f.get('recommendation')}")
                lines.append("")

        if recommendations:
            lines.append("-" * 60)
            lines.append("  改进建议")
            lines.append("-" * 60)
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"  {i}. {rec}")
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"  报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 60)

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主程序入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("行业合规工具 - compliance-checker")
    print("=" * 60)

    # 演示：合同分析
    print("\n[1] 合同条款分析示例:")
    sample_contract = "本合同金额为50000元，付款方式为银行转账。如一方违约，需赔偿对方全部损失。本合同适用中国法律。"
    result = contract_analyzer(sample_contract)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 演示：法规检索
    print("\n[2] 法规检索示例:")
    regs = regulation_searcher("数据", "互联网", "中国")
    print(json.dumps(regs, ensure_ascii=False, indent=2))

    # 演示：法律术语
    print("\n[3] 法律术语解释示例:")
    term = legal_term_explainer("不可抗力", "合同履行")
    print(json.dumps(term, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print("所有工具已就绪，可通过导入 main 模块使用。")
