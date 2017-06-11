#coding:utf-8

def pagination_data(page_number, page_range, total_pages, is_paginated):
        """
        page_number:当前页码号.
        page_range:整个分页页码列表,是一个生成器.
        total_page:分页的总数.
        is_paginated:是一个布尔变量,用于指示是否已分页.
        分页的规则如下:
        1.第1页页码,这一页需要始终显示.
        2.第1页页码后面的省略号部分.但要注意如果第1页的页码号后面紧跟着页码号2,那么省略号就不应该显示.
        3.当前页码的左边部分,比如5-6.
        4.当前页码,假设是7.
        5.当前页码的右边部分,比如8-9.
        6.最后一页页码前面的省略号部分.但要注意如果最后一页的页码号前面跟着的页码号是连续的,那么省略号就不应该显示.
        7.最后一页的页码号。
        """
        if not is_paginated:
            # 不需要分页,则无需显示分页导航条,不用任何分页导航条的数据,因此返回一个空的字典
            return {}
        # 当前页面左边连续的页码号,初始值为空
        left = []
        # 当前页面右边连续的页码号,初始值为空
        right = []
        # 标示第一页页码后是否需要显示省略号
        left_has_more = False
        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False
        # 标示是否需要显示第1页的页码号.
        # 因为如果当前页左边的连续页码号中已经含有第1页的页码号,此时就无需再显示第1页的页码号.
        # 其它情况下第一页的页码是始终需要显示的.
        # 初始值为False
        # 举例子:假设当前页面为3,左边显示4个页面,第1,2,3页都会在左边的连续页码号中,
        # 这个情况下第1页包含进去了,因此无需显示第1页的页码号.
        first = False
        # 标示是否需要显示最后一页的页码号
        last = False
        if page_number == 1:
            if total_pages == 2:
                right.append(page_range[1])
            else:     
                # 用户请求的是第一页的数据
                # 页码的右边部分为[2,3],左边和右边的连续页码都是加2
                right.append(page_range[1])
                right.append(page_range[2])
            # 最右边的页码号比最后一页的页码号减去1还要小,说明需要显示省略号
            if right[-1] < total_pages-1:
                right_has_more = True
            # 如果最右边的页码号比最后一页的页码号小,说明当前页右边的连续页码号中不包含最后一页的页码
            if right[-1] < total_pages:
                last = True
            # 下一页的页码为2,没有上一页,指向了第一页
            next_page = page_number+1
            previous_page = page_number
        elif page_number == total_pages:
            if total_pages == 2:
                left.append(page_range[-2])
            else:
                # 用户请求的是最后一页的数据
                left.append(page_range[-3])
                left.append(page_range[-2])
            if left[0] > 2:
                left_has_more = True
            # 如果最左边的页码号比第一页码号大,说明当前页左边的连续页码号中不包含第一页的页码
            if left[0] > 1:
                first = True
            # 上一页的页码为倒数第二页的页码,没有下一页,指向了最后一页
            next_page = page_number
            previous_page = page_number-1
        else:
            # 获取到左边的连续两个页面码号
            if page_number-3 < 0:
                left.append(page_range[0])
            else:
                left.append(page_range[page_number-3])
                left.append(page_range[page_number-2])
            if page_number+2 > total_pages:
                right.append(page_range[-1])
            else:
                right.append(page_range[page_number])
                right.append(page_range[page_number+1])
            # 判断是否要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages-1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            # 判断是否要显示第一页和第一页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            # 给上一页和下一页赋值
            next_page = page_number+1
            previous_page = page_number-1
        data = {
            "left":left,
            "right":right,
            "left_has_more":left_has_more,
            "right_has_more":right_has_more,
            "first":first,
            "last":last,
            "next_page":next_page,
            "previous_page":previous_page,
        }
        return data