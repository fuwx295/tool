# 大模型对话

## 数据获取

使用PostMan 工具，发送POST请求，获取数据
接口文档参考 [alert接口文档](https://kgwnvb.yuque.com/grmkz0/lymk39/wkin5i91vrtisbfh#LyPLc)

或者使用 data.py 脚本获取数据

```shell
python data.py
```

数据保存在alert_input.json和topology_input.json中

### 查询拓扑图接口

GET 192.168.1.20:31406/api/service/relation

### 查询告警事件数据

POST 192.168.1.20:31406/api/alerts/descendant/anormal/delta

## 对话流程

### 1.提示拓扑图+提供拓扑图数据

这里有一个微服务拓扑图，每层有服务名和调用接口，上层服务调用下层服务构成上游和下游调用关系，请根据数据内容记住上下游服务关系的拓扑结构。

注意：最上面的为入口服务。不要创造不存在的上下游调用关系，拓扑结构中不要出现环，不要联想到其他东西，只需要记住给出微服务拓扑图，也不需要解释内容。拓扑图数据如下

### 2.提示告警事件+告警数据

下面有一些告警事件，告警事件为JSON格式数据。

第一层的KEY为服务名

第二层的KEY为告警事件的异常类型

第三层的KEY含义如下

- add新增告警事件数
- duplicate重复告警事件数
- resolve已经解决告警事件数
- keep 目前还存留告警事件数
- firstTime该类型告警事件第一次发生时间
- lastTime该类型告警事件最后一次发生时间

记住这些告警事件，不用打印和解释这些数据。告警事件数据如下  

### 3.定义规则和根因判断流程，要求给出根因节点的结论

请根据上文提供的微服务拓扑图和每个节点的告警事件,根据规则寻找出根因节点。

规则如下，请牢记清楚

规则1:告警异常类型中值含义 1为应用异常,2为容器异常,3为基础设施异常,4为网络程序异常,5为JAVA堆栈抛出异常。没有告警事件的节点可以排除。

规则2:在拓扑中，下游节点发生告警，上游节点然后发生同类型的告警，那么认为告警从下游向上游传递。甚至还可以向更上游传递。因此根因节点需要满足最先发生告警且向上传递的条件 (传递可以参考告警事件第一次发生的时间)

规则3:在拓扑中，一个上游可能有多个下游节点，多个下游视为同级节点。如果同级节点中的服务都有和上游节点相同类型异常，那么这些下游节点都可认为是根因，且排除上游节点，不要遗漏节点。同时记得排除入口节点。

规则4:根因节点需要满足该节点下游未传递异常，或者为叶子节点（没有下游节点），同时告警事件是持续发生的，而不是偶发的（可以根据告警是否存留和告警发生时间判断）。如果节点的异常告警是偶发，那么它不应该被认定为根因节点

规则5:如果某个节点发生异常，但是上游节点未发生任何类型异常告警事件，可以将这个节点排除

规则6:如果两个节点都发送异常，且异常告警类型相同，这时判断这两个节点是否为上下游节点，如果是可以排除上游节点

根因寻找流程:

1. 根据告警事件中异常类型和发生次数，记录异常事件从下游往上游传递的顺序
2. 拓扑图中寻找异常类型对应的节点,主要关注应用异常和JAVA异常,同时查看上下游关系里面是否出现同样异常，相同则继续向下游继续排查

回答直接给出根因节点即可，不需要回答寻找根因流程等额外信息

### 4.引导大模型验证自己的结论，详细讲述推理流程

根据提供的拓扑图和告警事件数据并详细说明验证结论流程，验证流程应该带上数据。

如因为该节点发生xx异常,上下游发生了xx异常,根据规则xx,同时查看其他节点情况,因此可以判断xx。

## 存在的问题

### 1.数据采裁剪

告警事件为 200以下基本都能达到效果，但是告警事件超过500时，效果较差
需要提前对告警事件进行统计分析

数据处理工具

topology.py 用于生成拓扑图 处理拓扑图数据

alter.py 用于统计告警事件

告警事件统计流程
针对节点汇总，每个节点有如下信息
服务名用于标识节点
数字为告警事件异常类型

- add为新增告警事件数
- duplicate 重复告警事件数
- resolve: 已经解决告警事件数
- keep 存留告警事件数
- firstTime 该类型告警事件第一次发生时间
- lastTime 该类型告警事件最后一次发生时间

JSON数据中
第一层的KEY为服务名
第二层的KEY异常告警类型 （1为应用异常，2为容器异常，3为基础设施异常，4为网络异常，5为JAVA堆栈异常）
第三层数据中

```json
ts-xxx-service : {
 "1": {
  add: 0,
  duplicate: 0,
  resolve: 0,
  keep: 0,
  firstTime: 0,
  lastTime:0,
 }
}

```

### 2.提问尽可能丰富完善,每一步都去引导

模版中尽可能多添加信息，完善调整好，但是回答信息要钱尽可能简洁

1. 初始 设置gpt 角色
2. 告诉拓扑的描述+拓扑数据
3. 告诉规则+告警事件数据

### 数据补充

对于应用异常告警，耗时升高，有可能是偶发现象，因此需要查看1小时内的延时曲线，如果延时曲线未发送明显突破，可以认为该节点发生的异常是偶现，可以忽略。