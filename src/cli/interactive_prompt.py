"""
Interactive Prompt System / 交互式提示系统

This module provides interactive user input collection with validation.
本模块提供带验证的交互式用户输入收集功能。
"""

from typing import List, Optional, Any
from datetime import datetime
import re


class InteractivePrompt:
    """
    Interactive prompt system for collecting user input.
    交互式提示系统，用于收集用户输入。
    
    Responsibilities / 职责:
    - Collect text input / 收集文本输入
    - Collect choice input / 收集选择输入
    - Validate number input / 验证数字输入
    - Validate date input / 验证日期输入
    - Provide confirmation prompts / 提供确认提示
    """
    
    def __init__(self):
        """Initialize the interactive prompt system / 初始化交互式提示系统"""
        pass
    
    def ask_text(
        self, 
        prompt: str, 
        default: Optional[str] = None,
        allow_empty: bool = False
    ) -> str:
        """
        Ask for text input from user.
        向用户询问文本输入。
        
        Args:
            prompt: The prompt message to display / 显示的提示消息
            default: Default value if user presses Enter / 用户按回车时的默认值
            allow_empty: Whether to allow empty input / 是否允许空输入
            
        Returns:
            User's text input / 用户的文本输入
            
        Validates: Requirements 12.2, 12.3
        """
        while True:
            # Display prompt with default value if provided
            # 如果提供了默认值，则在提示中显示
            if default:
                display_prompt = f"{prompt} [默认: {default}]: "
            else:
                display_prompt = f"{prompt}: "
            
            user_input = input(display_prompt).strip()
            
            # Use default if input is empty and default is provided
            # 如果输入为空且提供了默认值，则使用默认值
            if not user_input and default:
                return default
            
            # Check if empty input is allowed
            # 检查是否允许空输入
            if not user_input and not allow_empty:
                print("❌ 错误: 输入不能为空，请重新输入。")
                print("❌ Error: Input cannot be empty, please try again.")
                continue
            
            return user_input
    
    def ask_choice(
        self, 
        prompt: str, 
        choices: List[str],
        default: Optional[int] = None
    ) -> str:
        """
        Ask user to select from a list of choices.
        让用户从选项列表中选择。
        
        Args:
            prompt: The prompt message to display / 显示的提示消息
            choices: List of available choices / 可用选项列表
            default: Default choice index (1-based) / 默认选项索引（从1开始）
            
        Returns:
            Selected choice string / 选中的选项字符串
            
        Validates: Requirements 12.2, 12.3, 12.5
        """
        if not choices:
            raise ValueError("Choices list cannot be empty / 选项列表不能为空")
        
        while True:
            # Display prompt and choices
            # 显示提示和选项
            print(f"\n{prompt}")
            for i, choice in enumerate(choices, 1):
                if default and i == default:
                    print(f"  {i}. {choice} [默认]")
                else:
                    print(f"  {i}. {choice}")
            
            # Get user input
            # 获取用户输入
            if default:
                user_input = input(f"请选择 (1-{len(choices)}) [默认: {default}]: ").strip()
            else:
                user_input = input(f"请选择 (1-{len(choices)}): ").strip()
            
            # Use default if input is empty and default is provided
            # 如果输入为空且提供了默认值，则使用默认值
            if not user_input and default:
                return choices[default - 1]
            
            # Validate input is a number
            # 验证输入是否为数字
            try:
                choice_num = int(user_input)
            except ValueError:
                print("❌ 错误: 请输入有效的数字。")
                print("❌ Error: Please enter a valid number.")
                continue
            
            # Validate choice is in range
            # 验证选择是否在范围内
            if choice_num < 1 or choice_num > len(choices):
                print(f"❌ 错误: 请输入 1 到 {len(choices)} 之间的数字。")
                print(f"❌ Error: Please enter a number between 1 and {len(choices)}.")
                continue
            
            return choices[choice_num - 1]
    
    def ask_number(
        self, 
        prompt: str, 
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        default: Optional[float] = None,
        number_type: str = "float"
    ) -> float:
        """
        Ask for numeric input with validation.
        询问数字输入并进行验证。
        
        Args:
            prompt: The prompt message to display / 显示的提示消息
            min_val: Minimum allowed value / 最小允许值
            max_val: Maximum allowed value / 最大允许值
            default: Default value / 默认值
            number_type: Type of number ("int" or "float") / 数字类型（"int"或"float"）
            
        Returns:
            User's numeric input / 用户的数字输入
            
        Validates: Requirements 12.2, 12.3, 12.5
        """
        while True:
            # Build prompt with constraints
            # 构建带约束的提示
            constraints = []
            if min_val is not None:
                constraints.append(f"最小: {min_val}")
            if max_val is not None:
                constraints.append(f"最大: {max_val}")
            
            display_prompt = prompt
            if constraints:
                display_prompt += f" ({', '.join(constraints)})"
            if default is not None:
                display_prompt += f" [默认: {default}]"
            display_prompt += ": "
            
            user_input = input(display_prompt).strip()
            
            # Use default if input is empty and default is provided
            # 如果输入为空且提供了默认值，则使用默认值
            if not user_input and default is not None:
                return default
            
            # Validate input is a number
            # 验证输入是否为数字
            try:
                if number_type == "int":
                    value = int(user_input)
                else:
                    value = float(user_input)
            except ValueError:
                print(f"❌ 错误: 请输入有效的{'整数' if number_type == 'int' else '数字'}。")
                print(f"❌ Error: Please enter a valid {'integer' if number_type == 'int' else 'number'}.")
                continue
            
            # Validate range
            # 验证范围
            if min_val is not None and value < min_val:
                print(f"❌ 错误: 输入值不能小于 {min_val}。")
                print(f"❌ Error: Input value cannot be less than {min_val}.")
                continue
            
            if max_val is not None and value > max_val:
                print(f"❌ 错误: 输入值不能大于 {max_val}。")
                print(f"❌ Error: Input value cannot be greater than {max_val}.")
                continue
            
            return value
    
    def ask_date(
        self, 
        prompt: str, 
        default: Optional[str] = None,
        date_format: str = "%Y-%m-%d"
    ) -> str:
        """
        Ask for date input with validation.
        询问日期输入并进行验证。
        
        Args:
            prompt: The prompt message to display / 显示的提示消息
            default: Default date string / 默认日期字符串
            date_format: Expected date format / 期望的日期格式
            
        Returns:
            User's date input in specified format / 用户的日期输入（指定格式）
            
        Validates: Requirements 12.2, 12.3, 12.5
        """
        while True:
            # Display prompt with format hint
            # 显示带格式提示的提示
            display_prompt = f"{prompt} (格式: {date_format})"
            if default:
                display_prompt += f" [默认: {default}]"
            display_prompt += ": "
            
            user_input = input(display_prompt).strip()
            
            # Use default if input is empty and default is provided
            # 如果输入为空且提供了默认值，则使用默认值
            if not user_input and default:
                return default
            
            # Validate date format
            # 验证日期格式
            try:
                datetime.strptime(user_input, date_format)
                return user_input
            except ValueError:
                print(f"❌ 错误: 日期格式不正确，请使用 {date_format} 格式。")
                print(f"❌ Error: Invalid date format, please use {date_format} format.")
                print(f"   示例 / Example: {datetime.now().strftime(date_format)}")
                continue
    
    def confirm(
        self, 
        prompt: str, 
        default: bool = True
    ) -> bool:
        """
        Ask for yes/no confirmation.
        询问是/否确认。
        
        Args:
            prompt: The confirmation message / 确认消息
            default: Default value (True for yes, False for no) / 默认值（True表示是，False表示否）
            
        Returns:
            True if user confirms, False otherwise / 如果用户确认则返回True，否则返回False
            
        Validates: Requirements 12.2, 12.3
        """
        # Build prompt with default hint
        # 构建带默认提示的提示
        if default:
            display_prompt = f"{prompt} (是/否) [默认: 是]: "
            default_str = "y"
        else:
            display_prompt = f"{prompt} (是/否) [默认: 否]: "
            default_str = "n"
        
        while True:
            user_input = input(display_prompt).strip().lower()
            
            # Use default if input is empty
            # 如果输入为空则使用默认值
            if not user_input:
                user_input = default_str
            
            # Check for yes/no variations
            # 检查是/否的各种变体
            if user_input in ['y', 'yes', '是', 'shi', 's']:
                return True
            elif user_input in ['n', 'no', '否', 'fou', 'f']:
                return False
            else:
                print("❌ 错误: 请输入 '是' 或 '否'。")
                print("❌ Error: Please enter 'yes' or 'no'.")
                continue
    
    def ask_integer(
        self,
        prompt: str,
        min_val: Optional[int] = None,
        max_val: Optional[int] = None,
        default: Optional[int] = None
    ) -> int:
        """
        Ask for integer input with validation.
        询问整数输入并进行验证。
        
        Args:
            prompt: The prompt message to display / 显示的提示消息
            min_val: Minimum allowed value / 最小允许值
            max_val: Maximum allowed value / 最大允许值
            default: Default value / 默认值
            
        Returns:
            User's integer input / 用户的整数输入
            
        Validates: Requirements 12.2, 12.3, 12.5
        """
        return int(self.ask_number(
            prompt=prompt,
            min_val=min_val,
            max_val=max_val,
            default=default,
            number_type="int"
        ))
    
    def display_message(self, message: str, message_type: str = "info") -> None:
        """
        Display a formatted message to the user.
        向用户显示格式化的消息。
        
        Args:
            message: The message to display / 要显示的消息
            message_type: Type of message ("info", "success", "warning", "error") / 消息类型
        """
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        icon = icons.get(message_type, "ℹ️")
        print(f"\n{icon} {message}\n")
    
    def display_progress(self, current: int, total: int, message: str = "") -> None:
        """
        Display a simple progress indicator.
        显示简单的进度指示器。
        
        Args:
            current: Current progress value / 当前进度值
            total: Total progress value / 总进度值
            message: Optional message to display / 可选的显示消息
        """
        percentage = int((current / total) * 100)
        bar_length = 40
        filled_length = int(bar_length * current / total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f"\r进度 / Progress: [{bar}] {percentage}% {message}", end='', flush=True)
        
        if current >= total:
            print()  # New line when complete
