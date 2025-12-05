"""
Unit tests for InteractivePrompt / InteractivePrompt单元测试

Tests the interactive prompt system functionality.
测试交互式提示系统功能。
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.cli.interactive_prompt import InteractivePrompt


class TestInteractivePrompt:
    """Test suite for InteractivePrompt class / InteractivePrompt类测试套件"""
    
    def setup_method(self):
        """Set up test fixtures / 设置测试夹具"""
        self.prompt = InteractivePrompt()
    
    # Test ask_text method
    
    def test_ask_text_with_input(self):
        """Test text input with user input / 测试带用户输入的文本输入"""
        with patch('builtins.input', return_value='test input'):
            result = self.prompt.ask_text("Enter text")
            assert result == 'test input'
    
    def test_ask_text_with_default(self):
        """Test text input with default value / 测试带默认值的文本输入"""
        with patch('builtins.input', return_value=''):
            result = self.prompt.ask_text("Enter text", default="default value")
            assert result == 'default value'
    
    def test_ask_text_empty_not_allowed(self):
        """Test text input rejects empty when not allowed / 测试不允许空输入时拒绝空值"""
        with patch('builtins.input', side_effect=['', 'valid input']):
            with patch('builtins.print'):  # Suppress error messages
                result = self.prompt.ask_text("Enter text", allow_empty=False)
                assert result == 'valid input'
    
    def test_ask_text_empty_allowed(self):
        """Test text input accepts empty when allowed / 测试允许空输入时接受空值"""
        with patch('builtins.input', return_value=''):
            result = self.prompt.ask_text("Enter text", allow_empty=True)
            assert result == ''
    
    # Test ask_choice method
    
    def test_ask_choice_valid_selection(self):
        """Test choice selection with valid input / 测试有效输入的选择"""
        choices = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value='2'):
            with patch('builtins.print'):  # Suppress menu display
                result = self.prompt.ask_choice("Select option", choices)
                assert result == "Option 2"
    
    def test_ask_choice_with_default(self):
        """Test choice selection with default / 测试带默认值的选择"""
        choices = ["Option 1", "Option 2", "Option 3"]
        with patch('builtins.input', return_value=''):
            with patch('builtins.print'):
                result = self.prompt.ask_choice("Select option", choices, default=1)
                assert result == "Option 1"
    
    def test_ask_choice_invalid_then_valid(self):
        """Test choice selection with invalid then valid input / 测试无效后有效输入的选择"""
        choices = ["Option 1", "Option 2"]
        with patch('builtins.input', side_effect=['invalid', '5', '1']):
            with patch('builtins.print'):
                result = self.prompt.ask_choice("Select option", choices)
                assert result == "Option 1"
    
    def test_ask_choice_empty_list_raises_error(self):
        """Test choice selection with empty list raises error / 测试空列表选择引发错误"""
        with pytest.raises(ValueError):
            self.prompt.ask_choice("Select option", [])
    
    # Test ask_number method
    
    def test_ask_number_valid_float(self):
        """Test number input with valid float / 测试有效浮点数输入"""
        with patch('builtins.input', return_value='3.14'):
            result = self.prompt.ask_number("Enter number")
            assert result == 3.14
    
    def test_ask_number_valid_int(self):
        """Test number input with valid integer / 测试有效整数输入"""
        with patch('builtins.input', return_value='42'):
            result = self.prompt.ask_number("Enter number", number_type="int")
            assert result == 42
            assert isinstance(result, int)
    
    def test_ask_number_with_default(self):
        """Test number input with default / 测试带默认值的数字输入"""
        with patch('builtins.input', return_value=''):
            result = self.prompt.ask_number("Enter number", default=10.5)
            assert result == 10.5
    
    def test_ask_number_min_max_validation(self):
        """Test number input validates min/max / 测试数字输入验证最小/最大值"""
        with patch('builtins.input', side_effect=['-5', '150', '50']):
            with patch('builtins.print'):
                result = self.prompt.ask_number("Enter number", min_val=0, max_val=100)
                assert result == 50
    
    def test_ask_number_invalid_then_valid(self):
        """Test number input with invalid then valid / 测试无效后有效的数字输入"""
        with patch('builtins.input', side_effect=['abc', '42']):
            with patch('builtins.print'):
                result = self.prompt.ask_number("Enter number")
                assert result == 42
    
    # Test ask_integer method
    
    def test_ask_integer(self):
        """Test integer input / 测试整数输入"""
        with patch('builtins.input', return_value='42'):
            result = self.prompt.ask_integer("Enter integer")
            assert result == 42
            assert isinstance(result, int)
    
    def test_ask_integer_with_constraints(self):
        """Test integer input with constraints / 测试带约束的整数输入"""
        with patch('builtins.input', side_effect=['-5', '150', '50']):
            with patch('builtins.print'):
                result = self.prompt.ask_integer("Enter integer", min_val=0, max_val=100)
                assert result == 50
    
    # Test ask_date method
    
    def test_ask_date_valid_format(self):
        """Test date input with valid format / 测试有效格式的日期输入"""
        with patch('builtins.input', return_value='2024-01-15'):
            result = self.prompt.ask_date("Enter date")
            assert result == '2024-01-15'
    
    def test_ask_date_with_default(self):
        """Test date input with default / 测试带默认值的日期输入"""
        with patch('builtins.input', return_value=''):
            result = self.prompt.ask_date("Enter date", default='2024-01-01')
            assert result == '2024-01-01'
    
    def test_ask_date_invalid_then_valid(self):
        """Test date input with invalid then valid format / 测试无效后有效格式的日期输入"""
        with patch('builtins.input', side_effect=['invalid-date', '2024-13-45', '2024-01-15']):
            with patch('builtins.print'):
                result = self.prompt.ask_date("Enter date")
                assert result == '2024-01-15'
    
    def test_ask_date_custom_format(self):
        """Test date input with custom format / 测试自定义格式的日期输入"""
        with patch('builtins.input', return_value='15/01/2024'):
            result = self.prompt.ask_date("Enter date", date_format='%d/%m/%Y')
            assert result == '15/01/2024'
    
    # Test confirm method
    
    def test_confirm_yes_variations(self):
        """Test confirmation with various yes inputs / 测试各种是的输入确认"""
        yes_inputs = ['y', 'yes', '是', 'Y', 'YES']
        for yes_input in yes_inputs:
            with patch('builtins.input', return_value=yes_input):
                result = self.prompt.confirm("Confirm?")
                assert result is True
    
    def test_confirm_no_variations(self):
        """Test confirmation with various no inputs / 测试各种否的输入确认"""
        no_inputs = ['n', 'no', '否', 'N', 'NO']
        for no_input in no_inputs:
            with patch('builtins.input', return_value=no_input):
                result = self.prompt.confirm("Confirm?")
                assert result is False
    
    def test_confirm_default_yes(self):
        """Test confirmation with default yes / 测试默认是的确认"""
        with patch('builtins.input', return_value=''):
            result = self.prompt.confirm("Confirm?", default=True)
            assert result is True
    
    def test_confirm_default_no(self):
        """Test confirmation with default no / 测试默认否的确认"""
        with patch('builtins.input', return_value=''):
            result = self.prompt.confirm("Confirm?", default=False)
            assert result is False
    
    def test_confirm_invalid_then_valid(self):
        """Test confirmation with invalid then valid input / 测试无效后有效输入的确认"""
        with patch('builtins.input', side_effect=['maybe', 'yes']):
            with patch('builtins.print'):
                result = self.prompt.confirm("Confirm?")
                assert result is True
    
    # Test display methods
    
    def test_display_message(self):
        """Test message display / 测试消息显示"""
        with patch('builtins.print') as mock_print:
            self.prompt.display_message("Test message", "info")
            mock_print.assert_called()
    
    def test_display_message_types(self):
        """Test different message types / 测试不同消息类型"""
        message_types = ["info", "success", "warning", "error"]
        for msg_type in message_types:
            with patch('builtins.print') as mock_print:
                self.prompt.display_message("Test", msg_type)
                mock_print.assert_called()
    
    def test_display_progress(self):
        """Test progress display / 测试进度显示"""
        with patch('builtins.print') as mock_print:
            self.prompt.display_progress(5, 10, "Processing")
            mock_print.assert_called()
    
    def test_display_progress_complete(self):
        """Test progress display at completion / 测试完成时的进度显示"""
        with patch('builtins.print') as mock_print:
            self.prompt.display_progress(10, 10, "Done")
            # Should print newline when complete
            assert mock_print.call_count >= 1


class TestInteractivePromptIntegration:
    """Integration tests for InteractivePrompt / InteractivePrompt集成测试"""
    
    def test_complete_workflow_simulation(self):
        """Test a complete workflow simulation / 测试完整工作流程模拟"""
        prompt = InteractivePrompt()
        
        # Simulate a complete user interaction workflow
        inputs = [
            '1',           # Market selection
            '1',           # Asset type selection
            '20',          # Target return
            '30',          # Simulation days
            '2024-01-01',  # Start date
            'yes'          # Confirmation
        ]
        
        with patch('builtins.input', side_effect=inputs):
            with patch('builtins.print'):
                # Market selection
                markets = ["中国市场", "美国市场", "香港市场"]
                market = prompt.ask_choice("Select market", markets)
                assert market == "中国市场"
                
                # Asset type selection
                asset_types = ["股票", "基金", "ETF"]
                asset_type = prompt.ask_choice("Select asset type", asset_types)
                assert asset_type == "股票"
                
                # Target return
                target_return = prompt.ask_number("Enter target return", min_val=0, max_val=100)
                assert target_return == 20
                
                # Simulation days
                simulation_days = prompt.ask_integer("Enter simulation days", min_val=1, max_val=365)
                assert simulation_days == 30
                
                # Start date
                start_date = prompt.ask_date("Enter start date")
                assert start_date == '2024-01-01'
                
                # Confirmation
                confirmed = prompt.confirm("Confirm?")
                assert confirmed is True


# Property-based tests would go here if using Hypothesis
# 基于属性的测试如果使用Hypothesis会放在这里
