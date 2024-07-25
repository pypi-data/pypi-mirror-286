# utils-hj3415

utils-hj3415 is the collection of utility functions.

두가지 모듈이 존재한다. - noti, utils

## Installation

```bash
pip install utils-hj3415
```

## Usage

### utils module
```python
from utils_hj3415 import utils

def to_float(s) -> float:

def to_int(s) -> int:
    
def deco_num(s) -> str:
    
def to_억(v) -> str:

def to_만(v) -> str:
    
def get_kor_amount(amount: int, omit: str = '', str_suffix: str = '원') -> str:
    
def str_to_date(d: str) -> datetime.datetime:

def date_to_str(d: datetime.datetime, sep: str = '-') -> str:

def isYmd(date: str) -> bool:

def isY_slash_m(date: str) -> bool:

def scrape_simple_data(url: str, css_selector: str) -> str:

def get_price_now(code: str) -> tuple:
    
def get_ip_addr() -> str:
    
def get_pc_info() -> dict:
    
def get_driver_edge() -> WebDriver | None:
    
def get_driver_safari() -> WebDriver | None:

def get_driver(temp_dir: str = '', headless=True, geolocation=False) -> WebDriver | None:

def nan_to_zero(v: float) -> float:

def code_divider_by_cpu_core(entire_codes: list) -> Tuple[int, List[list]]:
```

### noti module
```python
from utils_hj3415 import noti

def mail_to(title: str, text: str, mail_addr='hj3415@hanmail.net') -> bool:

def telegram_to(botname: str, text: str, parse_html: bool = False) -> bool:
    # botname - ['manager', 'dart', 'eval', 'cybos', 'servers']
```
