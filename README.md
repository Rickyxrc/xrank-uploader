# xrank-uploader

## 这是什么？

这是配合另一款开源软件[xrank](https://github.com/rickyxrc/xrank)使用的,可以快速上传后缀为`.csv`的文件添加排名。

csv 文件的格式如下：

```
<首列名称>,<列名称>,<列名称>,......
<索引值>,<值>,<值>,......
......
```

如果有不需要的列，可以在`./main.py`的`__ignore_rows`中设置。
后端网址在`__instant_baseurl`设置。
`API_KEY`在`__SECRET_API_KEY`中设置，为启动docker的镜像中的`API_KEY`环境变量。