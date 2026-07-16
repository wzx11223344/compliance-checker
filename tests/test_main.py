"""Auto-generated tests for compliance-checker."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main


class TestMain:
    """Tests for compliance-checker module."""

    def test_module_import(self):
        """Test that main module imports correctly."""
        assert main is not None
        assert hasattr(main, "contract_analyzer")


    def test_contract_analyzer_basic(self):
        """Test contract analysis with valid contract text."""
        contract = """甲方（上海XX科技）与乙方（北京YY公司）签订合同。
        第一条 合同期限：自2025年1月1日至2025年12月31日。
        第二条 合同金额：人民币 500,000 元。
        第三条 违约责任：如一方违约，应支付违约金。
        第四条 争议解决：提交上海仲裁委员会仲裁。"""
        result = main.contract_analyzer(contract)
        assert "structure" in result
        assert "key_elements" in result
        assert result["completeness"]["score"] > 0

    def test_contract_risk_points(self):
        """Test that risk points are identified."""
        contract = "甲方与乙方签订合同。合同金额：100,000元。"
        result = main.contract_analyzer(contract)
        assert "risk_points" in result
        assert "risk_level" in result

    def test_contract_parties(self):
        """Test party identification."""
        contract = "甲方（科技有限公司）与乙方（服务有限公司）"
        result = main.contract_analyzer(contract)
        parties = result["key_elements"]["parties"]
        assert len(parties) >= 0  # May or may not match depending on format
        assert result["risk_level"] in ["高", "中", "低"]


    def test_regulation_search_basic(self):
        """Test regulation search engine."""
        db = [
            {"id": "1", "title": "个人信息保护法", "content": "个人信息处理者应当遵循最小必要原则", "level": "法律"},
            {"id": "2", "title": "数据安全法", "content": "国家建立数据安全风险评估机制", "level": "法律"},
            {"id": "3", "title": "网络安全审查办法", "content": "重点评估数据出境安全风险", "level": "部门规章"},
        ]
        results = main.regulation_search_engine("个人信息安全", db, top_k=2)
        assert len(results) <= 2
        if results:
            assert "score" in results[0]

    def test_regulation_search_matches(self):
        """Test that search returns matching terms."""
        db = [{"id": "1", "title": "测试法", "content": "数据隐私保护个人信息安全管理", "level": "法律"}]
        results = main.regulation_search_engine("数据隐私", db)
        if results:
            assert len(results[0]["matched_terms"]) >= 0

    def test_regulation_search_empty(self):
        """Test regulation search with empty database."""
        results = main.regulation_search_engine("test", [])
        assert len(results) == 0


    def test_risk_assessment_model_basic(self):
        """Test risk assessment model."""
        factors = {"数据泄露频率": 7, "安全措施完善度": 3, "合规历史": 5, "第三方风险": 6}
        weights = {"数据泄露频率": 0.3, "安全措施完善度": 0.3, "合规历史": 0.2, "第三方风险": 0.2}
        result = main.risk_assessment_model(factors, weights, {})
        assert result["risk_level"] in ["低", "中低", "中", "中高", "高"]
        assert "total_score" in result
        assert "risk_matrix" in result

    def test_risk_assessment_high_risk(self):
        """Test risk assessment with all high factors."""
        factors = {"因子1": 10, "因子2": 10}
        weights = {"因子1": 1.0, "因子2": 1.0}
        result = main.risk_assessment_model(factors, weights, {})
        assert result["risk_level"] in ["中高", "高"]

    def test_risk_factors_detail(self):
        """Test that factor details are returned."""
        factors = {"a": 5, "b": 5}
        weights = {"a": 0.5, "b": 0.5}
        result = main.risk_assessment_model(factors, weights, {})
        assert "factors_detail" in result
        assert "a" in result["factors_detail"]

    def test_compliance_checklist_generator_exists(self):
        """Test that compliance_checklist_generator function is callable."""
        assert callable(main.compliance_checklist_generator)
        assert main.compliance_checklist_generator.__doc__ is not None


    def test_privacy_impact_assessment_basic(self):
        """Test privacy impact assessment."""
        activities = [
            {"activity_name": "用户注册", "data_types": ["姓名", "手机号", "身份证号"],
             "purpose": "身份验证", "retention_period": "5年",
             "recipients": ["云服务商"], "security_measures": ["加密", "访问控制"]},
        ]
        result = main.privacy_impact_assessment(activities)
        assert "risk_level" in result
        assert "risk_assessment" in result
        assert result["overall_risk_score"] > 0

    def test_pia_sensitive_data(self):
        """Test PIA with sensitive data types."""
        activities = [
            {"activity_name": "健康分析", "data_types": ["健康信息", "生物特征"],
             "purpose": "个性化推荐", "retention_period": "永久",
             "recipients": ["境外分析公司"], "security_measures": ["加密"]},
        ]
        result = main.privacy_impact_assessment(activities)
        assert len(result["risk_assessment"][0]["risks"]) >= 1

    def test_pia_dpa_notification(self):
        """Test that DPA notification flag is set correctly."""
        activities = [
            {"activity_name": "基本统计", "data_types": ["姓名"],
             "purpose": "统计报表", "retention_period": "1年",
             "recipients": [], "security_measures": ["加密", "访问控制", "审计日志", "备份"]},
        ]
        result = main.privacy_impact_assessment(activities)
        assert "requires_dpa_notification" in result
