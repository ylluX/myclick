# myclick

Imitate the [click](https://click.palletsprojects.com/en/8.0.x/) package

模仿`click`包，写一个超简易自定义包`myclick`，主要为了了解`click`的原理。


## 安装

```bash
pip install -e .
```


## 实例

以学生成绩录入系统(`enter_score.py`)为例：

```python
# coding:utf-8

import myclick

@myclick.command()
@myclick.option('-n', '--name', 'username', default='Alice', help='input your name')
@myclick.option('-s', '--sex', default='M')
@myclick.option('--age', default='10')
@myclick.option('--verbose', is_flag=True)
@myclick.argument('chinese')
@myclick.argument('math')
@myclick.argument('englist')
def cli(username, sex, age, verbose, chinese, math, englist):
    """
    input student score.
    """
    print(f'name: {username}, sex: {sex}, age: {age}')
    if verbose:
        print(f'  Chinese: {chinese}')
        print(f'  Math: {math}')
        print(f'  Englist: {englist}')

cli()

```

**1.查看help信息**

```bash
python enter_score.py --help
```
结果：

```bash
age: enter_score.py [OPTIONS] ENGLIST MATH CHINESE

Options:
  -n, --name          input your name
  -s, --sex
  --age
  --verbose
  --help              Show this message and exit.``

```
**2.录入成绩**

```bash
python enter_score.py -n xiaowang -s M --age 8 --verbose 100 90 80
```
结果：

```bash
name: xiaowang, sex: M, age: 8
  Chinese: 80
  Math: 90
  Englist: 100
```

