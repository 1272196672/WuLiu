layui.use(['dropdown', 'util', 'layer', 'table'], function () {
    var dropdown = layui.dropdown
        , util = layui.util
        , layer = layui.layer
        , table = layui.table
        , $ = layui.jquery;

    //初演示
    dropdown.render({
        elem: '.demo1'
        , data: [{
            title: '温度'
            , id: 100
        }, {
            title: '湿度'
            , id: 101
        }]
        , click: function (obj) {
            layer.tips('点击了：' + obj.title, this.elem, {tips: [1, '#5FB878']})
        }
    });

    //初演示 - 绑定输入框
    dropdown.render({
        elem: '#demo2'
        , data: [{
            title: 'menu item 1'
            , id: 101
        }, {
            title: 'menu item 2'
            , id: 102
        }, {
            title: 'menu item 3'
            , id: 103
        }, {
            title: 'menu item 4'
            , id: 104
        }, {
            title: 'menu item 5'
            , id: 105
        }, {
            title: 'menu item 6'
            , id: 106
        }]
        , click: function (obj) {
            this.elem.val(obj.title);
        }
        , style: 'width: 235px;'
    });

    //初演示 - 绑定文字
    dropdown.render({
        elem: '#demo3'
        , data: [{
            title: 'menu item 1'
            , id: 100
        }, {
            title: 'menu item 2'
            , id: 101
            , child: [{  //横向子菜单
                title: 'menu item 2-1'
                , id: 1011
            }, {
                title: 'menu item 2-2'
                , id: 1012
            }]
        }, {
            title: 'menu item 3'
            , id: 102
        }, {
            type: '-' //分割线
        }, {
            title: 'menu group'
            , id: 103
            , type: 'group' //纵向菜单组
            , child: [{
                title: 'menu item 4-1'
                , id: 1031
            }, {
                title: 'menu item 4-2'
                , id: 1032
            }]
        }, {
            type: '-' //分割线
        }, {
            title: 'menu item 5'
            , id: 104
        }, {
            title: 'menu item 5'
            , id: 104
        }]
        , click: function (obj) {
            this.elem.val(obj.title);
        }
    });

    //高级演示 - 各种组合
    dropdown.render({
        elem: '#demo100'
        , data: [{
            title: 'menu item 1'
            ,
            templet: '<i class="layui-icon layui-icon-picture"></i> {{d.title}} <span class="layui-badge-dot"></span>'
            ,
            id: 100
            ,
            href: '#'
        }, {
            title: 'menu item 2'
            , templet: '<img src="https://cdn.layui.com/avatar/168.jpg?t=123" style="width: 16px;"> {{d.title}}'
            , id: 101
            , href: '/'
            , target: '_blank'
        }
            , {type: '-'} //分割线
            , {
                title: 'menu item 3'
                , id: 102
                , type: 'group'
                , child: [{
                    title: 'menu item 3-1'
                    , id: 103
                }, {
                    title: 'menu item 3-2'
                    , id: 104
                    , child: [{
                        title: 'menu item 3-2-1'
                        , id: 105
                    }, {
                        title: 'menu item 3-2-2'
                        , id: 11
                        , type: 'group'
                        , child: [{
                            title: 'menu item 3-2-2-1'
                            , id: 111
                        }, {
                            title: 'menu item 3-2-2-2'
                            , id: 1111
                        }]
                    }, {
                        title: 'menu item 3-2-3'
                        , id: 11111
                    }]
                }, {
                    title: 'menu item 3-3'
                    , id: 111111
                    , type: 'group'
                    , child: [{
                        title: 'menu item 3-3-1'
                        , id: 22
                    }, {
                        title: 'menu item 3-3-2'
                        , id: 222
                        , child: [{
                            title: 'menu item 3-3-2-1'
                            , id: 2222
                        }, {
                            title: 'menu item 3-3-2-2'
                            , id: 22222
                        }, {
                            title: 'menu item 3-3-2-3'
                            , id: 2222222
                        }]
                    }, {
                        title: 'menu item 3-3-3'
                        , id: 333
                    }]
                }]
            }
            , {type: '-'}
            , {
                title: 'menu item 4'
                , id: 4
            }, {
                title: 'menu item 5'
                , id: 5
                , child: [{
                    title: 'menu item 5-1'
                    , id: 55
                    , child: [{
                        title: 'menu item 5-1-1'
                        , id: 5555
                    }, {
                        title: 'menu item 5-1-2'
                        , id: 55555
                    }, {
                        title: 'menu item 5-1-3'
                        , id: 555555
                    }]
                }, {
                    title: 'menu item 5-2'
                    , id: 52
                }, {
                    title: 'menu item 5-3'
                    , id: 53
                }]
            }, {type: '-'}, {
                title: 'menu item 6'
                , id: 66
                , type: 'group'
                , isSpreadItem: false
                , child: [{
                    title: 'menu item 6-1'
                    , id: 666
                }, {
                    title: 'menu item 6-2'
                    , id: 6666
                }, {
                    title: 'menu item 6-3'
                    , id: 66666
                }]
            }]
        , click: function (item) {
            layer.msg(util.escape(JSON.stringify(item)));
        }
    });

    // dropdown 在表格中的应用
    table.render({
        elem: '#test-dropdown-table'
        , url: 'https://www.layui.com/test/table/demo5.json'
        , title: '用户数据表'
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'id', title: 'ID', width: 80, fixed: 'left', unresize: true, sort: true}
            , {field: 'username', title: '用户名', width: 120, edit: 'text'}
            , {field: 'email', title: '邮箱', minWidth: 150}
            , {fixed: 'right', title: '操作', toolbar: '#test-dropdown-toolbar-barDemo', width: 150}
        ]]
        , limits: [3]
        , page: true
    });
    //行工具事件
    table.on('tool(test-dropdown-table)', function (obj) {
        var that = this
            , data = obj.data;

        if (obj.event === 'edit') {
            layer.prompt({
                formType: 2
                , value: data.email
            }, function (value, index) {
                obj.update({
                    email: value
                });
                layer.close(index);
            });
        } else if (obj.event === 'more') {
            //更多下拉菜单
            dropdown.render({
                elem: that
                , show: true //外部事件触发即显示
                , data: [{
                    title: 'item 1'
                    , id: 'aaa'
                }, {
                    title: 'item 2'
                    , id: 'bbb'
                }, {
                    title: '删除'
                    , id: 'del'
                }]
                , click: function (data, othis) {
                    //根据 id 做出不同操作
                    if (data.id === 'del') {
                        layer.confirm('真的删除行么', function (index) {
                            obj.del();
                            layer.close(index);
                        });
                    } else {
                        layer.msg('得到表格下拉菜单 id：' + data.id);
                    }
                }
                , align: 'right' //右对齐弹出（v2.6.8 新增）
                , style: 'box-shadow: 1px 1px 10px rgb(0 0 0 / 12%);' //设置额外样式
            });
        }
    });

    //自定义事件 - hover
    dropdown.render({
        elem: '#demo4'
        , trigger: 'hover'
        , data: [{
            title: 'menu item 1'
            , id: 100
        }, {
            title: 'menu item 2'
            , id: 101
        }, {
            title: 'menu item 3'
            , id: 102
        }]
    });

    //自定义事件 - mousedown
    dropdown.render({
        elem: '#demo5'
        , trigger: 'mousedown'
        , data: [{
            title: 'menu item 1'
            , id: 100
        }, {
            title: 'menu item 2'
            , id: 101
        }, {
            title: 'menu item 3'
            , id: 102
        }]
    });

    //自定义事件 - dblclick
    dropdown.render({
        elem: '#demo6'
        , trigger: 'dblclick'
        , data: [{
            title: 'menu item 1'
            , id: 100
        }, {
            title: 'menu item 2'
            , id: 101
        }, {
            title: 'menu item 3'
            , id: 102
        }]
    });

    //右键菜单
    var inst = dropdown.render({
        elem: '#demo7' //也可绑定到 document，从而重置整个右键
        , trigger: 'contextmenu' //contextmenu
        , isAllowSpread: false //禁止菜单组展开收缩
        , style: 'width: 200px' //定义宽度，默认自适应
        , id: 'test777' //定义唯一索引
        , data: [{
            title: 'menu item 1'
            , id: 'test'
        }, {
            title: 'Printing'
            , id: 'print'
        }, {
            title: 'Reload'
            , id: 'reload'
        }, {type: '-'}, {
            title: 'menu item 3'
            , id: '#3'
            , child: [{
                title: 'menu item 3-1'
                , id: '#1'
            }, {
                title: 'menu item 3-2'
                , id: '#2'
            }, {
                title: 'menu item 3-3'
                , id: '#3'
            }]
        }, {type: '-'}, {
            title: 'menu item 4'
            , id: ''
        }, {
            title: 'menu item 5'
            , id: '#1'
        }, {
            title: 'menu item 6'
            , id: '#1'
        }]
        , click: function (obj, othis) {
            if (obj.id === 'test') {
                layer.msg('click');
            } else if (obj.id === 'print') {
                window.print();
            } else if (obj.id === 'reload') {
                location.reload();
            }
        }
    });

    //对齐方式
    dropdown.render({
        elem: '#demo200'
        , data: [{
            title: 'menu item test 111'
            , id: 100
        }, {
            title: 'menu item test 222'
            , id: 101
        }, {
            title: 'menu item test 333'
            , id: 102
        }]
    });
    dropdown.render({
        elem: '#demo201'
        , align: 'center' //居中对齐（2.6.8 新增）
        , data: [{
            title: 'menu item test 111'
            , id: 100
        }, {
            title: 'menu item test 222'
            , id: 101
        }, {
            title: 'menu item test 333'
            , id: 102
        }]
    });
    dropdown.render({
        elem: '#demo202'
        , align: 'right' //右对齐（2.6.8 新增）
        , data: [{
            title: 'menu item test 111'
            , id: 100
        }, {
            title: 'menu item test 222'
            , id: 101
        }, {
            title: 'menu item test 333'
            , id: 102
        }]
    });


    //重定义样式
    dropdown.render({
        elem: '#demo8'
        , data: [{
            title: 'menu item 1'
            , id: 100
        }, {
            title: 'menu item 2'
            , id: 101
        }, {
            title: 'menu item 3'
            , id: 103
        }, {
            title: 'menu item 4'
            , id: 104
        }, {
            title: 'menu item 5'
            , id: 105
        }, {
            title: 'menu item 6'
            , id: 106
        }]
        , className: 'site-dropdown-demo'
        , ready: function (elemPanel, elem) {
            layer.msg('定义了一个 className');
        }
    });

    //重定义内容
    dropdown.render({
        elem: '#demo9'
        , content: ['<div class="layui-tab layui-tab-brief">'
            , '<ul class="layui-tab-title">'
            , '<li class="layui-this">Tab header 1</li>'
            , '<li>Tab header 2</li>'
            , '<li>Tab header 3</li>'
            , '</ul>'
            , '<div class="layui-tab-content">'
            , '<div class="layui-tab-item layui-text layui-show"><p style="padding-bottom: 10px;">在 content 参数中插入任意的 html 内容，可替代默认的下拉菜单。 从而实现更多有趣的弹出内容。</p><p> 是否发现，dropdown 组件不仅仅只是一个下拉菜单或者右键菜单，它能被赋予许多的想象可能。</p></div>'
            , '<div class="layui-tab-item">Tab body 2</div>'
            , '<div class="layui-tab-item">Tab body 3</div>'
            , '</div>'
            , '</div>'].join('')
        , style: 'width: 370px; height: 200px; padding: 0 15px; box-shadow: 1px 1px 30px rgb(0 0 0 / 12%);'
        , ready: function () {
            layui.use('element', function (element) {
                element.render('tab');
            });
        }
    });

    var form = layui.form
        , layer = layui.layer
        , layedit = layui.layedit
        , laydate = layui.laydate;

    //日期
    laydate.render({
        elem: '#date'
    });
    laydate.render({
        elem: '#date1'
    });

    //创建一个编辑器
    var editIndex = layedit.build('LAY_demo_editor');

    //自定义验证规则
    form.verify({
        title: function (value) {
            if (value.length < 5) {
                return '标题至少得5个字符啊';
            }
        }
        , pass: [
            /^[\S]{6,12}$/
            , '密码必须6到12位，且不能出现空格'
        ]
        , content: function (value) {
            layedit.sync(editIndex);
        }
    });

    //监听指定开关
    form.on('switch(switchTest)', function (data) {
        layer.msg('开关checked：' + (this.checked ? 'true' : 'false'), {
            offset: '6px'
        });
        layer.tips('温馨提示：请注意开关状态的文字可以随意定义，而不仅仅是ON|OFF', data.othis)
    });

    //监听提交
    form.on('submit(demo1)', function (data) {
        layer.alert(JSON.stringify(data.field), {
            title: '最终的提交信息'
        })
        return false;
    });

    //表单赋值
    layui.$('#LAY-component-form-setval').on('click', function () {
        form.val('example', {
            "username": "贤心" // "name": "value"
            , "password": "123456"
            , "interest": 1
            , "like[write]": true //复选框选中状态
            , "close": true //开关状态
            , "sex": "女"
            , "desc": "我爱 layui"
        });
    });

    //表单取值
    layui.$('#LAY-component-form-getval').on('click', function () {
        var data = form.val('example');
        alert(JSON.stringify(data));
    });


    //其他操作
    util.event('lay-demoactive', {
        //全局右键菜单
        rightclick: function (othis) {
            if (!othis.data('open')) {
                dropdown.reload('test777', {
                    elem: document //将事件直接绑定到 document
                });
                layer.msg('已开启全局右键菜单，请尝试在页面任意处单击右键。')
                othis.html('取消全局右键菜单');
                othis.data('open', true);
            } else {
                dropdown.reload('test777', {
                    elem: '#demo7' //重新绑定到指定元素上
                });
                layer.msg('已取消全局右键菜单，恢复默认右键菜单')
                othis.html('开启全局右键菜单');
                othis.data('open', false);
            }
        }
    })
});