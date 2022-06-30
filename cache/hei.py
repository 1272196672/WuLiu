from pyecharts import options as opts
from pyecharts.charts import BMap, Geo
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Geo
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

data = [
    ['东方明珠塔', '你的位置']
]

c = (

    BMap(init_opts=opts.InitOpts(width="1400px", height="800px"))
        # 百度地图开发应用 appkey，使用到百度地图的开发者自行到百度地图开发者中
        .add_schema(
        baidu_ak="wyysZdPfv503WDTI2nnuMyMsk6BGdrG9",
        center=[115.9865786272891, 39.992593559164156],  # 当前视角的中心点，用经纬度表示
        zoom=12,  # 当前视角的缩放比例
        is_roam=True,  # 是否开启鼠标缩放和平移漫游
    )

        .add(
        type_="effectScatter",  # 涟漪效果
        series_name="",  # 不使用的话会在地图上方有个小点
        data_pair=data,
        # data_pair = [list(z) for z in zip(['石家庄‘,'合肥','北京','上海','新疆'], [120,100,77,53,12])],
        # data_pair=[list(z) for z in zip(Faker.provinces, Faker.values())],  #生成虚假数据，方便调试
        symbol_size=5,
        effect_opts=opts.EffectOpts(),
        label_opts=opts.LabelOpts(
            position="top",  # 标签位置
            is_show=True,  # is_show是否显示标签,点上面的内容
            formatter=JsCode(  # formatter为标签内容格式器{a}：系列名;{b}：数据名;{c}：数值数组也可以是回调函数
                """function(params) {
                if ('value' in params.data) {
                    return params.data.value[2];
                }
            }"""
            ),
            # 显示数据，可以去掉经纬度只显示数值return params.data.value[2] + ': ' + params.data.value[0]+': ' + params.data.value[1];
        ),
        itemstyle_opts=opts.ItemStyleOpts(),
        is_selected=True,  # 选中图例
    )

        .set_global_opts(
        title_opts=opts.TitleOpts(
            title="物流",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(color="#0C0C0C"),  # 文字样式配置
        ),
        tooltip_opts=opts.TooltipOpts(  # 标签配置，选中某一个点显示的框
            trigger="item",  # 触发类型，item主要用于散点图
            formatter=JsCode(  # 显示提示框formatter为标签内容格式器{a}：系列名;{b}：数据名;{c}：数值数组也可以是回调函数
                """function(params) {
                if ('value' in params.data) {
                    return params.data.name + '<br>' + params.data.value[2];
                }
            }"""
            ),
            # 显示数据，可以去掉经纬度，只显示数值return params.data.value[2] + ': ' + params.data.value[0]+': ' + params.data.value[1];
        ),

    )
        .render(path="templates/myapp/map.html")
)
