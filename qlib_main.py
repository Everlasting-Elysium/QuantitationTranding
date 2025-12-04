import qlib
from qlib.constant import REG_CN
from qlib.data import D

provider_uri = "~/data/cn_data"  # target_dir

# init
qlib.init(provider_uri=provider_uri, region=REG_CN,exp_manager= {
    "class": "MLflowExpManager",
    "module_path": "qlib.workflow.expm",
    "kwargs": {
        "uri": "examples/mlruns",
        "default_exp_name": "Experiment",
    }
})

# 加载数据
D.calendar(start_time='20240-01-01', end_time='2024-12-31', freq='day')[:2]
D.instruments(market='all')
