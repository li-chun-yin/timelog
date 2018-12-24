var checkAjaxResponse	= function(json){
	if(json.status == 'success'){
		return true;
	}
	alert(json.message);
	return false;
}

/**
 * 遮罩层
 */
jQuery.fn.extend({'mask' : function(){
	var overflow	= jQuery(this).css('overflow');
	jQuery(this).css('overflow', 'hidden');
	jQuery(this).data('overflow', overflow);
	jQuery(this).append('<div class="overlay mask-overlay"><i class="fa fa-refresh fa-spin"></i></div>');
	jQuery(this).addClass('overlay-wrapper');
},'unmask': function(){
	var overflow	= jQuery(this).data('overflow');
	jQuery(this).css('overflow', overflow);
	jQuery(this).find('.mask-overlay').detach();
	jQuery(this).removeClass('overlay-wrapper');
}});


/**
 * 分页查询
 * option用于覆盖默认属性和方法。
 */
jQuery.fn.extend({'pager' : function( option ){
	/**
	 * default
	 */
	var option				= option || {};
	var _self				= this;		
	this.autoload			= jQuery.type(option.autoload) == 'undefined' ? true : option.autoload;		// 是否默认加载第一页.
	this.form				= jQuery( this );															// 分页查询表单
	this.search_btn			= option.search_btn || jQuery( this ).find(':submit');						// 触发列表加载的按钮
	this.list_size			= option.list_size || jQuery( this ).data('list_size') || 15;				// 每页显示行记录
	this.page_size			= option.page_size || jQuery( this ).data('page_size') || 10;				// 页码最多显示几个
	this.container			= option.container || jQuery(this).data('container');						// 内容容器
	this.page_area			= option.page_area || jQuery(this).data('pagebar');							// 分页标签容器
	this.checkall_tag		= option.checkall_tag || jQuery(this).data('checkall');						// 列表全选/取消全选控制框
	this.checkall_item_tag	= option.checkall_tag || jQuery(this).data('checkall_item');				// 列表全选/取消全选控制框
	
	jQuery(this.form).append('<input type="hidden" name="page_no" value="1" />');
	jQuery(this.form).append('<input type="hidden" name="list_size" value="' + this.list_size + '" />');
	this.page_no_tag	= jQuery(this.form).find('[name="page_no"]'); 	

	/*
	 * 列表加载
	 */
	this.load			= function(){
		jQuery(_self.container).mask();
		jQuery(_self.search_btn).prop('disabled', true);
		jQuery.get(jQuery(_self.form).prop('action'), jQuery(_self.form).serialize(),function(json){
		jQuery(_self.search_btn).prop('disabled', false);
		jQuery(_self.container).unmask();
			if(checkAjaxResponse(json)){
				_self.makeList( json );
				_self.pageBar( json );
			}
		},'json');
	}
	
	/*
	 * 全选/取消全选 复选框
	 */
	jQuery(_self.checkall_tag).click(function(){
		var checkbox_checked	= $(this).prop('checked');
		jQuery(_self.container).find(_self.checkall_item_tag).prop('checked', checkbox_checked);
	});
	
	/*
	 * 查询结果填充到内容容器的默认方法
	 */
	this.makeList	= function( json ){
		jQuery(_self.container).html( json.data.html );
	};

	/*
	 * 分页容器填充默认方法
	 */
	this.pageBar	= function( json ){
		var cur_page_no		= parseInt(jQuery(_self.page_no_tag).val(), 10);
		var lists_total 	= parseInt(json.data.total, 10);
		var list_size		= parseInt(_self.list_size, 10);
		var page_size		= parseInt(_self.page_size, 10);
		var total_page		= Math.ceil(lists_total / list_size);
		var start_page		= (Math.ceil(cur_page_no / page_size) - 1) * page_size + 1;
		var end_page		= (start_page + page_size - 1) > total_page ? total_page : start_page + page_size - 1;
		var page_html_tags	= [];

		page_html_tags.push('<div class="nav nav-page">');
		page_html_tags.push('<div class="total">共<span class="result-total">'+json.data.total+'</span>条记录/共<span class="page-total">'+total_page+'</span>页</div>');
		page_html_tags.push('<ul class="pagination">');
		page_html_tags.push('<li class="first-page '+(cur_page_no <= 1 ?　'disabled'　:　'')+'"><a href="javascript:void(0)" title="第一页">&lt;&lt;</a></li>');
		page_html_tags.push('<li class="prev-page '+(cur_page_no <= 1 ?　'disabled'　:　'')+'"><a href="javascript:void(0)"　title="上一页">&lt;</a></li>');
		for( var i = start_page ; i <= end_page; i++ ){
			page_html_tags.push('<li class="'+(cur_page_no == i ? 'active' : '')+'"><a href="javascript:void(0)">'+i+'</a></li>');			
		}
		page_html_tags.push('<li class="next-page '+(cur_page_no >= total_page ?　'disabled'　:　'')+'"><a href="javascript:void(0)"　title="下一页">&gt;</a></li>');
		page_html_tags.push('<li class="last-page '+(cur_page_no >= total_page ?　'disabled'　:　'')+'"><a href="javascript:void(0)"　title="最后一页">&gt;&gt;</a></li>');
		page_html_tags.push('<li>');
		page_html_tags.push('<div class="quick">');
		page_html_tags.push('<label>跳转到<input type="number" name="page_no" value="'+cur_page_no+'" min="1" max="'+total_page+'" /></label>');
		page_html_tags.push('<button type="button" class="btn btn-default">跳转</button>');
		page_html_tags.push('</div>');
		page_html_tags.push('</li>');
		page_html_tags.push('</ul>');
		page_html_tags.push('</div>');		

		jQuery(_self.page_area).html(page_html_tags.join('')).find('.nav .pagination a,.nav .pagination button').click(function(){
			if(jQuery(this).parent().hasClass('disabled') || jQuery(this).parent().hasClass('active')){
				return;
			}			
			var go_to_page = cur_page_no;			
			if(jQuery.isNumeric(jQuery(this).html())){
				go_to_page	= jQuery(this).html();
			}else if(jQuery(this).parent().hasClass('first-page')){
				go_to_page	= 1;
			}else if(jQuery(this).parent().hasClass('prev-page')){
				go_to_page	= go_to_page - 1;
			}else if(jQuery(this).parent().hasClass('next-page')){
				go_to_page	= go_to_page + 1;				
			}else if(jQuery(this).parent().hasClass('last-page')){
				go_to_page	= total_page;								
			}else if(jQuery(this).parent().hasClass('quick')){
				go_to_page	= jQuery(this).parent().find('[name="page_no"]').val();
			}
			
			go_to_page	= go_to_page > total_page ? total_page : go_to_page;
			go_to_page	= go_to_page < 1 ? 1 : go_to_page;

			jQuery(_self.page_no_tag).val(go_to_page);
			_self.load();
		});
	};
	
	jQuery(_self).submit(function(){
		_self.load();
		return false;
	});
	
	/**
	 * do search
	 */
	jQuery(_self.search_btn).click(function(){
		jQuery(_self.page_no_tag).val(1);
		jQuery(_self.checkall_tag).prop('checked',false);
	});

	/**
	 * init auto load
	 */
	if(_self.autoload == true){
		jQuery(_self.page_no_tag).val(1);
		_self.load();
	}
	
	return _self;
}});